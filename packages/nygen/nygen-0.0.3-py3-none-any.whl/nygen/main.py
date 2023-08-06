import argparse

from nygen.lib.gen import gen_project

from nygen.conf import init_conf


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--author")
    init_parser.add_argument("--email")
    init_parser.add_argument("--github")
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("name", help="Package name")
    create_parser.add_argument("--author")
    create_parser.add_argument("--email")
    create_parser.add_argument("--github")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if args.command == "init":
        print("Creating conf file")
        confpath = init_conf(args.author, args.email, args.github)
        print(f"Created {confpath}")
    elif args.command == "create":
        print(f"Generating {args.name}")
        gen_project(args.name, args.author, args.email, args.github)
    else:
        print("Invalid Command")


if __name__ == "__main__":
    main()
