# Agent notes

- fhadmin 3.0 is an admin theme (plan: ~/journal/Admin Theme.md, section 4).
  `fhadmin/static/fhadmin/theme.css` sets Django's admin variables (light,
  dark via prefers-color-scheme and html[data-theme="dark"]) and component
  rules; `fhadmin.css` holds the dashboard groups and quickpanel.
- Both stylesheets are linked at the start of `extrahead`, before
  `{{ block.super }}`, so environment overrides of --primary/--secondary/
  --accent in a project's admin/base.html win. Brand colours are set under
  `html[data-theme="light"], :root` like Django's base.css (a plain `:root`
  loses against Django's blue in explicit light mode), and
  `--secondary`/`--accent` never in the dark blocks. `test_brand_colours` and
  `test_environment_colours` check this.
- Only target class names Django's templates use. Django 5.2/6.0 have no
  `.titles-and-tools`; theme.css pins `.object-tools` to the title there.
- Tests: `tox` (pytest + Playwright). Screenshots go to
  `tests/screenshots/django-X.Y/` (gitignored); look at them after changes.
  For quick runs: `uv venv .venv-theme` and install `-e .[tests]`.
- Add user-visible changes to the "Next version" section of `CHANGELOG.rst`
  in the same commit as the change.
- Git: commit directly on `main`, and don't add attribution lines
  (no `Co-Authored-By`, no "Generated with" footer) to commits.
