#!/usr/bin/env python3
"""Build site/plugins.json from the awesome-polars README (+ GitHub stars)."""
import json, os, re, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

README = "https://raw.githubusercontent.com/ddotta/awesome-polars/main/README.md"
OUT = Path(__file__).resolve().parent.parent / "site" / "plugins.json"
TOKEN = os.environ.get("GITHUB_TOKEN")
GH = re.compile(r"github\.com/([\w.-]+)/([\w.-]+)")
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
ITEM = re.compile(r"^(?:[-*]\s+)?\[([^\]]+)\]\(([^)]+)\)\s*[-–]?\s*(.*)$")


def get(url, accept=None):
    h = {"User-Agent": "polars-plugins-site"}
    if TOKEN and "api.github.com" in url:
        h["Authorization"] = f"Bearer {TOKEN}"
    if accept:
        h["Accept"] = accept
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
        return r.read().decode()


def parse(md):
    sec = md.split("### Polars plugins", 1)[1]
    sec = re.split(r"\n### (?!#)", sec, maxsplit=1)[0]
    items, cat = [], None
    for line in sec.splitlines():
        if line.startswith("#### "):
            cat = line[5:].strip()
            continue
        m = ITEM.match(line.strip())
        if not cat or not m:
            continue
        name, url, rest = m.groups()
        gh = GH.search(url) or GH.search(line)
        desc = LINK.sub(r"\1", rest)
        desc = re.sub(r"\s+by\s+@[\w.-]+\.?", "", desc).strip(" .")
        items.append({
            "name": name, "url": url, "category": cat, "desc": desc,
            "repo": f"{gh.group(1)}/{gh.group(2)}" if gh else None,
            "author": gh.group(1) if gh else re.sub(r"^www\.", "", url.split("/")[2]),
            "stars": None,
        })
    return items


def stars(repo):
    try:
        data = get(f"https://api.github.com/repos/{repo}", "application/vnd.github+json")
        return json.loads(data)["stargazers_count"]
    except Exception as e:
        print(f"! stars {repo}: {e}", file=sys.stderr)
        return None


def main():
    items = parse(get(README))
    if not os.environ.get("SKIP_STARS"):
        cache = {}
        for it in items:
            if it["repo"]:
                if it["repo"] not in cache:
                    cache[it["repo"]] = stars(it["repo"])
                it["stars"] = cache[it["repo"]]
    OUT.write_text(json.dumps({
        "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "plugins": items,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(items)} plugins -> {OUT}")


if __name__ == "__main__":
    main()
