from __future__ import annotations

import argparse
import json
import sys
import webbrowser

from .urlgen import FlightsQuery, HotelsQuery, build_flights_url, build_hotels_url

CABINS = ["economy", "premium-economy", "business", "first"]


def _positive_int(value: str) -> int:
    try:
        n = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be an integer")
    if n <= 0:
        raise argparse.ArgumentTypeError("must be > 0")
    return n


def cmd_flights(args: argparse.Namespace) -> int:
    q = FlightsQuery(
        origin=args.origin,
        destination=args.destination,
        date=args.date,
        return_date=args.return_date,
        adults=args.adults,
        cabin=args.cabin,
    )
    url = build_flights_url(q)
    if args.json:
        print(json.dumps({"kind": "flights", **q.__dict__, "url": url}, ensure_ascii=False))
    else:
        print(url)
    if args.open:
        webbrowser.open(url)
    return 0


def cmd_hotels(args: argparse.Namespace) -> int:
    q = HotelsQuery(
        location=args.location,
        checkin=args.checkin,
        checkout=args.checkout,
        guests=args.guests,
        rooms=args.rooms,
    )
    url = build_hotels_url(q)
    if args.json:
        print(json.dumps({"kind": "hotels", **q.__dict__, "url": url}, ensure_ascii=False))
    else:
        print(url)
    if args.open:
        webbrowser.open(url)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pointsyeah", description="Generate PointsYeah search URLs for flights and hotels")
    sub = p.add_subparsers(dest="command", required=True)

    pf = sub.add_parser("flights", help="Generate a PointsYeah flight search URL")
    pf.add_argument("origin", help="Origin airport code (e.g., JFK)")
    pf.add_argument("destination", help="Destination airport code (e.g., LAX)")
    pf.add_argument("--date", required=True, help="Departure date (YYYY-MM-DD)")
    pf.add_argument("--return", dest="return_date", help="Return date (YYYY-MM-DD)")
    pf.add_argument("--adults", type=_positive_int, default=1)
    pf.add_argument("--cabin", choices=CABINS, default="economy")
    pf.add_argument("--open", action="store_true", help="Open the URL in your browser")
    pf.add_argument("--json", action="store_true", help="Output as JSON")
    pf.set_defaults(func=cmd_flights)

    ph = sub.add_parser("hotels", help="Generate a PointsYeah hotel search URL")
    ph.add_argument("location", help="City/area or hotel keyword")
    ph.add_argument("--checkin", required=True, help="Check-in date (YYYY-MM-DD)")
    ph.add_argument("--checkout", required=True, help="Check-out date (YYYY-MM-DD)")
    ph.add_argument("--guests", type=_positive_int, default=1)
    ph.add_argument("--rooms", type=_positive_int, default=1)
    ph.add_argument("--open", action="store_true", help="Open the URL in your browser")
    ph.add_argument("--json", action="store_true", help="Output as JSON")
    ph.set_defaults(func=cmd_hotels)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
