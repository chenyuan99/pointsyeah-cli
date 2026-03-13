# pointsyeah-cli

A small CLI that generates **PointsYeah** search URLs for **flights** and **hotels**.

- No scraping.
- No API keys.
- Works by producing a best-effort URL with readable query parameters.

## Install

### One-off (recommended)

```bash
uvx --from pointsyeah-cli pointsyeah --help
```

### Local dev install

```bash
cd projects/pointsyeah-cli
uv tool install -e .
pointsyeah --help
```

## Usage

### Flights

```bash
pointsyeah flights JFK LAX --date 2026-04-10
pointsyeah flights JFK LAX --date 2026-04-10 --return 2026-04-15 --adults 2 --cabin business
pointsyeah flights JFK LAX --date 2026-04-10 --json
pointsyeah flights JFK LAX --date 2026-04-10 --open
```

### Hotels

```bash
pointsyeah hotels "Jersey City" --checkin 2026-04-10 --checkout 2026-04-12
pointsyeah hotels "Boston" --checkin 2026-05-01 --checkout 2026-05-05 --guests 2 --rooms 1 --open
```

## Notes

PointsYeah does not provide a stable, documented deep-link format. This CLI outputs a URL like:

```
https://www.pointsyeah.com/?type=flights&origin=JFK&destination=LAX&date=2026-04-10&return=&adults=1&cabin=economy
```

If PointsYeah changes their UI, you can still use the parameters as a reference when searching manually.
