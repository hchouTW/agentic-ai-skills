import argparse


def main():
    ap = argparse.ArgumentParser(prog="shop")
    ap.add_argument("command", choices=["reindex", "purge-cache"])
    args = ap.parse_args()
    print(f"running {args.command}")


if __name__ == "__main__":
    main()
