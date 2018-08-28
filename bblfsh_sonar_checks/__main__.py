#!/usr/bin/env python3

import argparse
import json
import sys
from typing import Set

from bblfsh_sonar_checks import (
        run_checks, list_checks, get_check_description
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--language", type=str, help="Language for the file or listings", required=True)
    parser.add_argument("-i", "--ip", type=str, help="Server IP", default="0.0.0.0")
    parser.add_argument("-p", "--port", type=str, help="Server port", default="9432")
    parser.add_argument("-d", "--disable", type=str, help="Disable specific checks")
    parser.add_argument("-e", "--enable", type=str, help="Enable only specific checks. If ommited, all will be run")
    parser.add_argument("-L", "--list", action="store_true", help="List all avaliable checks")
    parser.add_argument("file", type=str, nargs="?", help="Input file to parse")
    args = parser.parse_args()

    def _convert_checkname(check):
        ncheck = check

        if not check.startswith("RSPEC-"):
            if not check.isdigit():
                print("Wrong check format, use RSPEC-#### or just the number: ", check)
                parser.print_help()
                sys.exit(1)
            else:
                ncheck = "RSPEC-{}".format(check)

        return ncheck

    args.checks: Set[str] = set()

    if args.enable:
        args.checks = {_convert_checkname(i.strip()) for i in args.enable.split(",")}
    else:
        args.checks = list_checks(args.language)

    if args.disable:
        disabled = {_convert_checkname(i.strip()) for i in args.disable.split(",")}
        for disable in disabled:
            args.checks.remove(disable)

    args.checks = list(args.checks)

    if args.list:
        _list(args.language)
        sys.exit(0)

    return args


def _list(lang):
    for check in list_checks(lang):
        print("{} : {}".format(check, get_check_description(check, lang)))


def main() -> None:
    args = parse_arguments()

    import bblfsh

    client = bblfsh.BblfshClient(args.ip + ":" + args.port)
    parse_result = client.parse(args.file)
    if parse_result.status != 0:
        print(json.dumps(parse_result.errors))

    print(json.dumps(run_checks(args.checks, args.language, parse_result.uast, json_result=False)))


if __name__ == "__main__":
    main()
