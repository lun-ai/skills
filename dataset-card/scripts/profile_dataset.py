#!/usr/bin/env python3
"""Profile a tabular dataset for a dataset card.

Computes the universal statistics a card needs — scale, schema, missingness,
duplicates and label contradictions, candidate group keys, target distributions,
label-noise ceiling, multi-target coupling, stratum shift and leakage candidates —
and writes both machine-readable JSON and ready-to-paste Markdown tables.

Only the aspects the data supports are emitted. A section that does not apply is
absent rather than filled with placeholders, matching the card convention that a
blank means "does not apply".

Usage
-----
    python profile_dataset.py DATA [DATA ...] \
        --target gfp_rate --target growth_rate \
        --se gfp_rate=gfp_rate_se \
        --group source_doi --stratum split \
        --input-cols p1,p2,p3,p4,p5 \
        --out profile/

Accepts CSV, TSV, Parquet, JSON Lines and Excel. A directory is expanded to the
tabular files directly inside it.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

# Deliberately excludes a bare "-": it is a real value in genomics (strand), chemistry
# (charge) and any dash-coded category, and treating it as missing silently turns a balanced
# two-level factor into a half-empty constant.
SENTINELS = {"", "na", "n/a", "nan", "none", "null", "unknown", "--", "?", "-999", "-9999"}
SENTINEL_WARN_FRACTION = 0.2
TABULAR_SUFFIXES = {".csv", ".tsv", ".txt", ".parquet", ".jsonl", ".ndjson", ".xlsx", ".xls"}


# --------------------------------------------------------------------------- load


def is_textual(series: pd.Series) -> bool:
    """True for text-like columns under both legacy object and modern string dtypes.

    pandas 3 reports string columns as StringDtype rather than object, so a bare
    ``dtype == object`` test silently skips every text column.
    """
    return bool(
        pd.api.types.is_object_dtype(series)
        or pd.api.types.is_string_dtype(series)
        or isinstance(series.dtype, pd.CategoricalDtype)
    )


def expand_paths(raw: list[str]) -> list[Path]:
    paths: list[Path] = []
    for item in raw:
        path = Path(item)
        if path.is_dir():
            paths += sorted(p for p in path.iterdir() if p.suffix.lower() in TABULAR_SUFFIXES)
        else:
            paths.append(path)
    missing = [str(p) for p in paths if not p.exists()]
    if missing:
        raise SystemExit(f"no such file: {', '.join(missing)}")
    if not paths:
        raise SystemExit("no tabular files found")
    return paths


def read_one(path: Path, sheet: str | int | None, header_row: int) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in {".csv", ".txt"}:
        return pd.read_csv(path, header=header_row, low_memory=False)
    if suffix == ".tsv":
        return pd.read_csv(path, sep="\t", header=header_row, low_memory=False)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix in {".jsonl", ".ndjson"}:
        return pd.read_json(path, lines=True)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path, sheet_name=0 if sheet is None else sheet, header=header_row)
    raise SystemExit(f"unsupported file type: {path.suffix}")


def load(paths: list[Path], sheet, header_row: int) -> tuple[pd.DataFrame, list[dict]]:
    frames, provenance = [], []
    for path in paths:
        frame = read_one(path, sheet, header_row)
        provenance.append(
            {
                "file": str(path),
                "bytes": path.stat().st_size,
                "rows_as_read": int(len(frame)),
                "columns_as_read": int(frame.shape[1]),
            }
        )
        frames.append(frame)
    if len(frames) > 1:
        # Without this column the file a row came from is unrecoverable, and that is
        # very often the dataset's most important group key (one file per species,
        # subject, site or batch).
        for frame, meta in zip(frames, provenance):
            frame["source_file"] = Path(meta["file"]).name
        combined = pd.concat(frames, ignore_index=True)
    else:
        combined = frames[0]
    return combined, provenance


def normalise_missing(frame: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    """Treat whitespace and common sentinel strings as missing, which loaders do not.

    Returns the frame plus a warning per column where sentinel matching removed a large
    share of the values. Such a column is usually a real category that happens to use a
    sentinel-looking token, and silently blanking it produces a false finding rather than
    an error, so it has to be surfaced.
    """
    out = frame.copy()
    warnings: list[dict] = []
    for col in out.columns:
        if not is_textual(out[col]):
            continue
        stripped = out[col].astype(str).str.strip()
        hit = stripped.str.lower().isin(SENTINELS) & out[col].notna()
        out[col] = stripped.where(~stripped.str.lower().isin(SENTINELS), other=np.nan)
        share = float(hit.sum()) / max(len(out), 1)
        if share >= SENTINEL_WARN_FRACTION:
            warnings.append(
                {
                    "field": str(col),
                    "values_treated_as_missing": int(hit.sum()),
                    "fraction": round(share, 4),
                    "note": "check these are truly missing; a sentinel-looking token may be a real level",
                }
            )
    return out, warnings


# ---------------------------------------------------------------------- statistics


def blank_rows(frame: pd.DataFrame) -> int:
    return int(frame.isna().all(axis=1).sum())


def schema(frame: pd.DataFrame) -> list[dict]:
    n = len(frame)
    rows = []
    for col in frame.columns:
        series = frame[col]
        present = series.dropna()
        example = present.iloc[0] if len(present) else None
        rows.append(
            {
                "field": str(col),
                "dtype": str(series.dtype),
                "missing": int(series.isna().sum()),
                "missing_pct": round(100 * series.isna().sum() / n, 3) if n else None,
                "distinct": int(series.nunique(dropna=True)),
                "constant": bool(series.nunique(dropna=True) <= 1),
                "example": None
                if example is None
                else (str(example)[:60] + "…" if len(str(example)) > 60 else str(example)),
            }
        )
    return rows


def numeric_summary(series: pd.Series) -> dict:
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return {}
    mean = float(values.mean())
    sd = float(values.std())
    return {
        "n": int(values.size),
        "missing": int(series.isna().sum()),
        "mean": mean,
        "sd": sd,
        "min": float(values.min()),
        "median": float(values.median()),
        "max": float(values.max()),
        "skew": float(values.skew()),
        "excess_kurtosis": float(values.kurtosis()),
        "coefficient_of_variation": (sd / mean) if mean else None,
        "variance": float(values.var()),
    }


def categorical_summary(series: pd.Series) -> dict:
    counts = series.value_counts(dropna=True)
    if counts.empty:
        return {}
    return {
        "n": int(series.notna().sum()),
        "missing": int(series.isna().sum()),
        "classes": int(counts.size),
        "per_class": {str(k): int(v) for k, v in counts.items()},
        "largest_class": int(counts.iloc[0]),
        "rarest_class": int(counts.iloc[-1]),
        "imbalance_ratio": float(counts.iloc[0] / counts.iloc[-1]),
    }


def is_numeric(series: pd.Series) -> bool:
    if pd.api.types.is_numeric_dtype(series):
        return True
    coerced = pd.to_numeric(series, errors="coerce")
    return coerced.notna().sum() >= 0.95 * max(series.notna().sum(), 1)


def noise_ceiling(frame: pd.DataFrame, target: str, se_col: str) -> dict:
    values = pd.to_numeric(frame[target], errors="coerce")
    errors = pd.to_numeric(frame[se_col], errors="coerce")
    paired = pd.concat([values, errors], axis=1).dropna()
    if paired.empty or paired.iloc[:, 0].var() == 0:
        return {}
    mean_se = float(paired.iloc[:, 1].mean())
    variance = float(paired.iloc[:, 0].var())
    fraction = (mean_se**2) / variance
    return {
        "standard_error_column": se_col,
        "mean_standard_error": mean_se,
        "median_standard_error": float(paired.iloc[:, 1].median()),
        "target_variance": variance,
        "noise_variance_fraction": fraction,
        "implied_ceiling_r2": 1 - fraction,
        "formula": "noise fraction = (mean standard error)^2 / var(target); ceiling = 1 - fraction",
    }


def replicate_reliability(frame: pd.DataFrame, input_cols: list[str], target: str) -> dict:
    """Variance decomposition over repeated identical inputs (ICC)."""
    key = row_key(frame, input_cols)
    values = pd.to_numeric(frame[target], errors="coerce")
    table = pd.DataFrame({"key": key, "value": values}).dropna()
    sizes = table.groupby("key")["value"].size()
    repeated = sizes[sizes > 1]
    if repeated.empty:
        return {}
    grouped = table[table.key.isin(repeated.index)].groupby("key")["value"]
    within = float(grouped.var(ddof=1).mean())
    between = float(table.groupby("key")["value"].mean().var(ddof=1))
    spread = grouped.apply(lambda s: float(s.max() - s.min()))
    total = between + within
    return {
        "replicated_inputs": int(repeated.size),
        "instances_involved": int(repeated.sum()),
        "within_group_variance": within,
        "between_group_variance": between,
        "reliability_icc": (between / total) if total else None,
        "within_group_range_min": float(spread.min()),
        "within_group_range_median": float(spread.median()),
        "within_group_range_max": float(spread.max()),
        "formula": "ICC = between / (between + within); it bounds achievable squared correlation",
    }


def row_key(frame: pd.DataFrame, cols: list[str]) -> pd.Series:
    """A single hashable key per row over `cols`.

    Missing values become an explicit token: under modern pandas, ``astype(str)`` leaves
    NaN as a float rather than the string "nan", so joining raw converted columns raises.
    Two rows missing the same field are treated as matching, which is what a duplicate
    check should do.
    """
    sub = frame[cols].astype(object)
    sub = sub.where(sub.notna(), "<missing>")
    return sub.astype(str).agg("|".join, axis=1)


def duplicate_report(frame: pd.DataFrame, input_cols: list[str], targets: list[str]) -> dict:
    out = {"exact_duplicate_instances": int(frame.duplicated().sum())}
    if not input_cols:
        return out
    key = row_key(frame, input_cols)
    sizes = key.value_counts()
    repeated = sizes[sizes > 1]
    out |= {
        "input_columns": input_cols,
        "distinct_inputs": int(sizes.size),
        "repeated_inputs": int(repeated.size),
        "instances_in_repeated_inputs": int(repeated.sum()),
    }
    for target in targets:
        if target not in frame.columns:
            continue
        table = pd.DataFrame({"key": key, "value": frame[target]})
        sub = table[table.key.isin(repeated.index)]
        agreeing = sub.groupby("key")["value"].nunique(dropna=False)
        out[f"repeated_inputs_identical_{target}"] = int((agreeing <= 1).sum())
        out[f"repeated_inputs_differing_{target}"] = int((agreeing > 1).sum())
    return out


def group_candidates(
    frame: pd.DataFrame,
    explicit: list[str],
    targets: list[str],
    input_cols: list[str] | None = None,
    exclude_inputs: bool = False,
) -> list[dict]:
    """Fields along which instances repeat, which decide whether a random split is safe.

    Detection is automatic, because the group key you have not thought of is exactly the
    one that invalidates a random split. Model-input columns are excluded only when the
    caller actually named them (--input-cols): a declared feature with few levels repeats
    by design, so proposing it as a group key is noise. Columns named explicitly with
    --group are always kept, even if they are also inputs.
    """
    n = len(frame)
    exclude = set(targets)
    if exclude_inputs:
        exclude |= set(input_cols or [])
    considered = list(explicit)
    for col in frame.columns:
        if col in considered or col in exclude:
            continue
        distinct = frame[col].nunique(dropna=True)
        if 1 < distinct < 0.9 * n and is_textual(frame[col]):
            considered.append(col)
    rows = []
    for col in considered:
        if col not in frame.columns:
            continue
        sizes = frame.groupby(col, dropna=True).size()
        if sizes.empty:
            continue
        in_multi = int(sizes[sizes > 1].sum())
        rows.append(
            {
                "field": str(col),
                "groups": int(sizes.size),
                "median_per_group": float(sizes.median()),
                "max_per_group": int(sizes.max()),
                "instances_in_groups_above_one": in_multi,
                "fraction_in_groups_above_one": round(in_multi / n, 4) if n else None,
                "random_split_over_instances_safe": bool(sizes.max() <= 1),
            }
        )
    return sorted(rows, key=lambda r: -r["instances_in_groups_above_one"])


def level_balance(frame: pd.DataFrame, factors: list[str]) -> list[dict]:
    rows = []
    for col in factors:
        counts = frame[col].value_counts(dropna=True)
        if counts.empty:
            continue
        rows.append(
            {
                "factor": str(col),
                "levels": int(counts.size),
                "min_per_level": int(counts.min()),
                "median_per_level": float(counts.median()),
                "max_per_level": int(counts.max()),
            }
        )
    return rows


def design_space(frame: pd.DataFrame, factors: list[str]) -> dict:
    if not factors:
        return {}
    sizes = [int(frame[c].nunique(dropna=True)) for c in factors]
    space = math.prod(sizes)
    distinct = int(row_key(frame, factors).nunique())
    return {
        "factors": factors,
        "levels_per_factor": sizes,
        "design_space_size": space,
        "distinct_designs_observed": distinct,
        "covered_fraction_pct": round(100 * distinct / space, 4) if space else None,
    }


def target_coupling(frame: pd.DataFrame, targets: list[str]) -> dict:
    numeric = [t for t in targets if t in frame.columns and is_numeric(frame[t])]
    if len(numeric) < 2:
        return {}
    values = frame[numeric].apply(pd.to_numeric, errors="coerce")
    pearson = values.corr()
    spearman = values.corr(method="spearman")
    pairs = []
    for i, a in enumerate(numeric):
        for b in numeric[i + 1 :]:
            r = float(pearson.loc[a, b])
            pairs.append(
                {
                    "pair": [a, b],
                    "pearson_r": r,
                    "spearman_rho": float(spearman.loc[a, b]),
                    "shared_variance_r2": r**2,
                }
            )
    return {"pairs": pairs}


def stratum_shift(frame: pd.DataFrame, stratum: str, targets: list[str]) -> dict:
    if stratum not in frame.columns:
        return {}
    out: dict = {"field": stratum, "strata": {}}
    counts = frame[stratum].value_counts(dropna=True)
    reference = str(counts.index[0])
    out["reference_stratum"] = reference
    for target in targets:
        if target not in frame.columns or not is_numeric(frame[target]):
            continue
        per: dict = {}
        values = pd.to_numeric(frame[target], errors="coerce")
        ref = values[frame[stratum].astype(str) == reference].dropna()
        for level, _ in counts.items():
            sub = values[frame[stratum].astype(str) == str(level)].dropna()
            if sub.empty:
                continue
            entry = {
                "n": int(sub.size),
                "mean": float(sub.mean()),
                "sd": float(sub.std()),
                "min": float(sub.min()),
                "max": float(sub.max()),
            }
            if str(level) != reference and len(ref) > 1 and len(sub) > 1:
                pooled = math.sqrt((ref.var() + sub.var()) / 2)
                if pooled:
                    entry["standardised_mean_difference_vs_reference"] = float(
                        (sub.mean() - ref.mean()) / pooled
                    )
            per[str(level)] = entry
        out["strata"][target] = per
    return out


def leakage_candidates(frame: pd.DataFrame, targets: list[str], threshold: float) -> list[dict]:
    rows = []
    numeric_targets = [t for t in targets if t in frame.columns and is_numeric(frame[t])]
    numeric_cols = [
        c for c in frame.columns if c not in targets and is_numeric(frame[c])
    ]
    for target in numeric_targets:
        y = pd.to_numeric(frame[target], errors="coerce")
        for col in numeric_cols:
            x = pd.to_numeric(frame[col], errors="coerce")
            paired = pd.concat([x, y], axis=1).dropna()
            if len(paired) < 3 or paired.iloc[:, 0].std() == 0:
                continue
            r = float(paired.iloc[:, 0].corr(paired.iloc[:, 1]))
            if abs(r) >= threshold:
                rows.append({"field": str(col), "target": target, "pearson_r": r})
    return rows


def collinear_pairs(frame: pd.DataFrame, threshold: float = 0.999) -> list[dict]:
    numeric = frame.select_dtypes(include=[np.number])
    if numeric.shape[1] < 2:
        return []
    corr = numeric.corr().abs()
    rows = []
    cols = list(corr.columns)
    for i, a in enumerate(cols):
        for b in cols[i + 1 :]:
            value = corr.loc[a, b]
            if pd.notna(value) and value >= threshold:
                rows.append({"pair": [str(a), str(b)], "abs_pearson_r": float(value)})
    return rows


# ------------------------------------------------------------------------ markdown


def md_table(rows: list[dict], columns: list[str] | None = None) -> str:
    if not rows:
        return "_none_\n"
    columns = columns or list(rows[0].keys())
    head = "| " + " | ".join(columns) + " |\n"
    rule = "|" + "|".join("---" for _ in columns) + "|\n"
    body = ""
    for row in rows:
        cells = []
        for col in columns:
            value = row.get(col)
            if isinstance(value, float):
                cells.append(f"{value:.4g}")
            elif isinstance(value, list):
                cells.append(", ".join(str(v) for v in value))
            elif value is None:
                cells.append("")
            else:
                cells.append(str(value))
        body += "| " + " | ".join(cells) + " |\n"
    return head + rule + body


def to_markdown(report: dict) -> str:
    out = ["# Dataset profile\n"]
    if report.get("sentinel_warnings"):
        out.append(
            "\n> **Check before using:** sentinel-looking tokens were treated as missing in the "
            "fields below. Confirm they are genuinely missing rather than real levels.\n\n"
        )
        out.append(md_table(report["sentinel_warnings"]))
    out.append("## Provenance and scale\n")
    out.append(md_table(report["files"]))
    scale = report["scale"]
    out.append(
        f"\nInstances: **{scale['instances']}** · fields: **{scale['fields']}** · "
        f"wholly blank rows dropped: **{scale['blank_rows_dropped']}** · "
        f"rows as read: **{scale['rows_as_read']}**\n"
    )
    out.append("\n## Schema and missingness\n")
    out.append(
        md_table(
            report["schema"],
            ["field", "dtype", "missing", "missing_pct", "distinct", "constant", "example"],
        )
    )
    for name, key in [
        ("Target statistics (numeric)", "targets_numeric"),
        ("Target statistics (categorical)", "targets_categorical"),
    ]:
        if report.get(key):
            out.append(f"\n## {name}\n")
            rows = [{"target": t, **v} for t, v in report[key].items()]
            out.append(md_table(rows))
    if report.get("label_noise"):
        out.append("\n## Label noise and achievable ceiling\n")
        rows = [{"target": t, **v} for t, v in report["label_noise"].items()]
        out.append(md_table(rows))
    if report.get("replicate_reliability"):
        out.append("\n## Replicate reliability\n")
        rows = [{"target": t, **v} for t, v in report["replicate_reliability"].items()]
        out.append(md_table(rows))
    if report.get("target_coupling"):
        out.append("\n## Multi-target coupling\n")
        out.append(md_table(report["target_coupling"]["pairs"]))
    out.append("\n## Duplicates and contradictions\n")
    out.append(md_table([{"check": k, "value": v} for k, v in report["duplicates"].items()]))
    if report.get("group_candidates"):
        out.append("\n## Candidate group keys\n")
        out.append(md_table(report["group_candidates"]))
    if report.get("design_space"):
        out.append("\n## Design space\n")
        out.append(md_table([{"check": k, "value": v} for k, v in report["design_space"].items()]))
    if report.get("level_balance"):
        out.append("\n## Per-factor level balance\n")
        out.append(md_table(report["level_balance"]))
    if report.get("stratum_shift", {}).get("strata"):
        out.append("\n## Stratum shift\n")
        for target, per in report["stratum_shift"]["strata"].items():
            out.append(f"\n**{target}** (reference: {report['stratum_shift']['reference_stratum']})\n")
            out.append(md_table([{"stratum": k, **v} for k, v in per.items()]))
    if report.get("leakage_candidates"):
        out.append("\n## Leakage candidates\n")
        out.append(md_table(report["leakage_candidates"]))
    if report.get("collinear_pairs"):
        out.append("\n## Collinear field pairs\n")
        out.append(md_table(report["collinear_pairs"]))
    if report.get("constant_fields"):
        out.append("\n## Constant fields\n")
        out.append(", ".join(report["constant_fields"]) + "\n")
    return "".join(out)


# ---------------------------------------------------------------------------- main


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("data", nargs="+", help="data file(s) or a directory of them")
    parser.add_argument("--target", action="append", default=[], help="label column; repeatable")
    parser.add_argument("--se", action="append", default=[], help="target=standard_error_column; repeatable")
    parser.add_argument("--group", action="append", default=[], help="known group key; repeatable")
    parser.add_argument("--stratum", help="column holding predefined strata or splits")
    parser.add_argument("--input-cols", help="comma-separated model-input columns (default: all non-target)")
    parser.add_argument("--factors", help="comma-separated design factors for design-space coverage")
    parser.add_argument("--sheet", help="Excel sheet name or index")
    parser.add_argument("--header-row", type=int, default=0, help="0-based header row (default 0)")
    parser.add_argument("--leakage-threshold", type=float, default=0.95)
    parser.add_argument("--keep-blank-rows", action="store_true", help="do not drop wholly blank rows")
    parser.add_argument("--out", default="dataset_profile", help="output directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = expand_paths(args.data)
    sheet = args.sheet
    if sheet is not None and str(sheet).isdigit():
        sheet = int(sheet)

    frame, files = load(paths, sheet, args.header_row)
    rows_as_read = len(frame)
    frame, sentinel_warnings = normalise_missing(frame)
    dropped = blank_rows(frame)
    if not args.keep_blank_rows and dropped:
        frame = frame[~frame.isna().all(axis=1)].reset_index(drop=True)

    targets = [t for t in args.target if t in frame.columns]
    unknown = [t for t in args.target if t not in frame.columns]
    factors = [c for c in (args.factors.split(",") if args.factors else []) if c in frame.columns]
    if args.input_cols:
        input_cols = [c for c in args.input_cols.split(",") if c in frame.columns]
    else:
        input_cols = [c for c in frame.columns if c not in targets]

    se_map: dict[str, str] = {}
    for item in args.se:
        if "=" in item:
            key, value = item.split("=", 1)
            if key in frame.columns and value in frame.columns:
                se_map[key] = value

    report: dict = {
        "files": files,
        "scale": {
            "instances": int(len(frame)),
            "fields": int(frame.shape[1]),
            "rows_as_read": int(rows_as_read),
            "blank_rows_dropped": int(0 if args.keep_blank_rows else dropped),
        },
        "schema": schema(frame),
        "targets_numeric": {},
        "targets_categorical": {},
        "label_noise": {},
        "replicate_reliability": {},
        "duplicates": duplicate_report(frame, input_cols, targets),
        "group_candidates": group_candidates(
            frame, args.group, targets, input_cols, exclude_inputs=bool(args.input_cols)
        ),
        "constant_fields": [r["field"] for r in schema(frame) if r["constant"]],
        "collinear_pairs": collinear_pairs(frame),
        "unknown_targets": unknown,
        "sentinel_warnings": sentinel_warnings,
    }

    for target in targets:
        if is_numeric(frame[target]):
            report["targets_numeric"][target] = numeric_summary(frame[target])
            if target in se_map:
                ceiling = noise_ceiling(frame, target, se_map[target])
                if ceiling:
                    report["label_noise"][target] = ceiling
            reliability = replicate_reliability(frame, input_cols, target)
            if reliability:
                report["replicate_reliability"][target] = reliability
        else:
            report["targets_categorical"][target] = categorical_summary(frame[target])

    coupling = target_coupling(frame, targets)
    if coupling:
        report["target_coupling"] = coupling
    if factors:
        report["design_space"] = design_space(frame, factors)
        report["level_balance"] = level_balance(frame, factors)
    if args.stratum:
        shift = stratum_shift(frame, args.stratum, targets)
        if shift:
            report["stratum_shift"] = shift
    if targets:
        report["leakage_candidates"] = leakage_candidates(frame, targets, args.leakage_threshold)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "profile.json").write_text(json.dumps(report, indent=2, default=str))
    (out_dir / "profile.md").write_text(to_markdown(report))

    print(f"instances={report['scale']['instances']} fields={report['scale']['fields']}")
    if report["scale"]["blank_rows_dropped"]:
        print(f"dropped {report['scale']['blank_rows_dropped']} wholly blank rows")
    if unknown:
        print(f"WARNING: target column(s) not found: {', '.join(unknown)}")
    for warning in sentinel_warnings:
        print(
            f"WARNING: {warning['field']}: {warning['values_treated_as_missing']} values "
            f"({warning['fraction']:.1%}) treated as missing -- check they are not a real level"
        )
    if len(paths) > 1:
        print("note: added a source_file column so the originating file stays recoverable")
    print(f"wrote {out_dir/'profile.json'} and {out_dir/'profile.md'}")


if __name__ == "__main__":
    main()
