import argparse

try:
    from .core import full_name
except Exception:
    from name_format.core import full_name  # type: ignore


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Format personal names (Irish O’/Ó, Mc/Mac, initials, particles)."
    )
    parser.add_argument("name", nargs="*", help="Full name as one or more tokens")
    parser.add_argument("-f", "--first", help="First name (requires --last)")
    parser.add_argument("-l", "--last", help="Last name (used with --first)")
    args = parser.parse_args()

    # Mode 1: explicit first + last
    if args.first is not None:
        if args.last is None:
            parser.error("--first requires --last")
        print(full_name(args.first, args.last))
        return

    # Mode 2: name provided as tokens
    if not args.name:
        parser.error("Provide either NAME tokens, or --first and --last.")
    print(full_name(" ".join(args.name)))


if __name__ == "__main__":
    main()
