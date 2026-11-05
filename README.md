# Polars Plugins

A searchable, dark-themed catalog of Polars plugins, generated from
[ddotta/awesome-polars](https://github.com/ddotta/awesome-polars) with live GitHub star counts.

## How it works

- `scripts/build.py` downloads the awesome-polars README, parses the **Polars plugins** section
  and fetches each repository's stars from the GitHub API → `site/plugins.json`.
- `site/` is a static site (HTML/CSS/JS, no build step) that reads `plugins.json`.
- `.github/workflows/update.yml` rebuilds and deploys to GitHub Pages every day at 05:00 UTC,
  on each push to `main`, and on demand.

## Setup

1. Push this repository to GitHub.
2. **Settings → Pages → Source: GitHub Actions**.
3. Run the workflow once from the **Actions** tab (or push to `main`).

## Local preview

```bash
GITHUB_TOKEN=ghp_xxx python scripts/build.py   # SKIP_STARS=1 to skip the stars
python -m http.server -d site 8000
```

No dependency beyond Python 3.9+.
