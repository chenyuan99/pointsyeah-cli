# Skills — pointsyeah CLI

## Purpose

`pointsyeah` generates **PointsYeah** deep-link search URLs for flights and hotels.
It does **not** scrape the site or call a private API; it assembles a URL that can be opened in a browser or returned as structured JSON.

Use this tool whenever a user asks to:
- Search for award flights or hotel availability on PointsYeah
- Generate or share a PointsYeah search link
- Open a PointsYeah search in their browser

---

## Install

```bash
uv pip install --system -e .
```

Or as a standalone tool:

```bash
uv tool install -e .
```

---

## Commands

### `flights` — Generate a flight search URL

```
pointsyeah flights <ORIGIN> <DESTINATION> --date <YYYY-MM-DD> [OPTIONS]
```

| Argument / Option | Required | Default   | Description |
|-------------------|----------|-----------|-------------|
| `ORIGIN`          | yes      | —         | Origin airport IATA code (e.g. `JFK`) |
| `DESTINATION`     | yes      | —         | Destination airport IATA code (e.g. `LAX`) |
| `--date`          | yes      | —         | Departure date in `YYYY-MM-DD` format |
| `--return`        | no       | one-way   | Return date in `YYYY-MM-DD` format |
| `--adults`        | no       | `1`       | Number of adult passengers (positive integer) |
| `--cabin`         | no       | `economy` | Cabin class: `economy`, `premium-economy`, `business`, `first` |
| `--open`          | no       | false     | Open the generated URL in the default browser |
| `--json`          | no       | false     | Print result as JSON instead of a plain URL |

**Examples:**

```bash
# One-way, economy, 1 adult
pointsyeah flights JFK LAX --date 2026-04-10

# Round-trip, business, 2 adults
pointsyeah flights JFK LAX --date 2026-04-10 --return 2026-04-15 --adults 2 --cabin business

# Generate URL and open it immediately
pointsyeah flights SFO LHR --date 2026-06-01 --cabin first --open

# JSON output for programmatic use
pointsyeah flights JFK LAX --date 2026-04-10 --return 2026-04-15 --adults 2 --cabin business --json
```

**JSON output shape (`--json`):**

```json
{
  "kind": "flights",
  "origin": "JFK",
  "destination": "LAX",
  "date": "2026-04-10",
  "return_date": "2026-04-15",
  "adults": 2,
  "cabin": "business",
  "url": "https://www.pointsyeah.com/?type=flights&origin=JFK&destination=LAX&date=2026-04-10&return=2026-04-15&adults=2&cabin=business"
}
```

---

### `hotels` — Generate a hotel search URL

```
pointsyeah hotels <LOCATION> --checkin <YYYY-MM-DD> --checkout <YYYY-MM-DD> [OPTIONS]
```

| Argument / Option | Required | Default | Description |
|-------------------|----------|---------|-------------|
| `LOCATION`        | yes      | —       | City, area, or hotel keyword (free text) |
| `--checkin`       | yes      | —       | Check-in date in `YYYY-MM-DD` format |
| `--checkout`      | yes      | —       | Check-out date in `YYYY-MM-DD` format |
| `--guests`        | no       | `1`     | Number of guests (positive integer) |
| `--rooms`         | no       | `1`     | Number of rooms (positive integer) |
| `--open`          | no       | false   | Open the generated URL in the default browser |
| `--json`          | no       | false   | Print result as JSON instead of a plain URL |

**Examples:**

```bash
# Minimal hotel search
pointsyeah hotels "Jersey City" --checkin 2026-04-10 --checkout 2026-04-12

# Multi-guest, multi-room, open in browser
pointsyeah hotels "Boston" --checkin 2026-05-01 --checkout 2026-05-05 --guests 2 --rooms 1 --open

# JSON output
pointsyeah hotels "Tokyo" --checkin 2026-07-15 --checkout 2026-07-20 --guests 2 --json
```

**JSON output shape (`--json`):**

```json
{
  "kind": "hotels",
  "location": "Tokyo",
  "checkin": "2026-07-15",
  "checkout": "2026-07-20",
  "guests": 2,
  "rooms": 1,
  "url": "https://www.pointsyeah.com/?type=hotels&location=Tokyo&checkin=2026-07-15&checkout=2026-07-20&guests=2&rooms=1"
}
```

---

## Notes for AI agents

- **IATA codes are uppercased automatically.** Passing `jfk` is the same as `JFK`.
- **Location is free text.** Pass the city name as the user typed it; quoting is only needed for multi-word names in the shell.
- **`--json` is the preferred output mode** when you need to extract the URL programmatically or return structured data to a caller.
- **`--open` is a side-effect flag** — it calls the system browser. Only use it when the user explicitly asks to open the link.
- The URL format is best-effort. PointsYeah does not publish a stable deep-link spec.

---

## Development

```bash
# Install in editable mode
uv pip install --system -e .
uv pip install --system pytest

# Run tests
pytest -q
```
