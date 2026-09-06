import argparse
from .seed import seed
from .refresh import refresh
from .validate import validate


def main():
    p = argparse.ArgumentParser(description="Beebe public-image pipeline")
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("seed")
    s.add_argument("--source")
    r = sub.add_parser("refresh")
    r.add_argument("--mode", choices=["fast", "images", "all"], default="fast")
    r.add_argument("--max-downloads", type=int, default=100)
    r.add_argument("--budget-seconds", type=int, default=1200)
    r.add_argument("--reconcile", action="store_true")
    sub.add_parser("validate")
    args = p.parse_args()
    if args.command == "seed":
        seed(args.source)
    elif args.command == "refresh":
        refresh(args.mode, args.max_downloads, args.budget_seconds, args.reconcile)
    validate()


if __name__ == "__main__":
    main()
