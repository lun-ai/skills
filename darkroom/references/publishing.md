# Printing and sharing

## Publishing

- Publish each `site/<part>/index.html` with the Artifact tool. Pass the figures it uses through
  `files` (published path `fig/name.png`, source path under the series folder). Use an icon such as
  `article`.
- **The first publish creates the link; every later publish of the same file path keeps it.** Write
  each link into `blog.toml` (`url = …`), rebuild so the series cards link to each other, and
  republish every post.
- When a title or the series name changes, republish every post: each one shows all the titles in
  its series cards.
- Record the links and the series folder in memory, so a later session can resume.

## The edit loop: dodge and burn

1. `git status` and `git diff` the post files. Commit the author's edits **on their own** before
   touching anything ("Blog part 2: user edits").
2. Read the diff. Check every changed number and every new factual claim against its source. Report
   mismatches with the numbers; fix a factual error in a separate commit the author can revert.
3. Apply only the requested changes, plus factual fixes. List every change, including typo fixes.
4. Build, read the checks, republish only the posts that changed (or all of them, see above).
   Commit the rebuilt pages.

## Where the sources live

- The pages are hosted on claude.ai and stay up if the machine or session that built them goes
  away. **The sources do not.** Keep the series folder in git and tell the author when the branch
  is unpushed or on a disk without backup.
- Use an extra branch or worktree only when the author asks for one.

## Before anyone else reads it

- **Sharing.** Pages are private until shared from each page's Share menu; Claude cannot change
  sharing. Share every post in a series, or the series links lead to a private page. Ask the author
  to open each link in a private window.
- **Leaks.** The build's check flags HTML comments, author notes and placeholders. Also read the
  posts for internal paths, internal set names and notes addressed to the author.
- **Double-blind review.** Flag any post that describes a paper under anonymous review.
- **Collaborators.** Flag unpublished results or data produced with others; sign-off is the
  author's call.
- **A personal website.** If the author wants the posts on their own site, ask the session working
  on that site how it takes posts (framework, front matter, asset folder), export to that format
  rather than dropping in standalone pages, strip HTML comments, and let the author merge and
  publish.
