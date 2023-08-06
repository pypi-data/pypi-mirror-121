import argparse
import json
import os
import pprint
import sys
import warnings

import jmespath

__version__ = "0.2.0"
__description__ = "A python implementation of the jp CLI for JMESPath"



# This 2 space indent matches https://github.com/jmespath/jp behavior.
JP_COMPAT_DUMP_KWARGS = (
    ("indent", 2),
    ("ensure_ascii", False),
)


def jp_main(argv=None):
    argv = sys.argv if argv is None else argv
    prog = os.path.basename(argv[0])

    if "jpipe" == prog:
        warnings.warn("The 'jpipe' command in its current form is deprecated (change is planned). Please use jp or jpp instead (for a stable interface).", UserWarning)

    parser = argparse.ArgumentParser(prog=prog)
    parser.add_argument("expression", nargs="?", default=None)
    parser.add_argument(
        "-c",
        "--compact",
        action="store_true",
        dest="compact",
        default=False,
        help=("Produce compact JSON output that omits nonessential whitespace."),
    )
    parser.add_argument(
        "-e",
        "--expr-file",
        dest="expr_file",
        default=None,
        help=("Read JMESPath expression from the specified file."),
    )
    parser.add_argument(
        "-f",
        "--filename",
        dest="filename",
        default=None,
        help=(
            "The filename containing the input data. "
            "If a filename is not given then data is "
            "read from stdin."
        ),
    )
    parser.add_argument(
        "-u",
        "--unquoted",
        action="store_false",
        dest="quoted",
        default=True,
        help=("If the final result is a string, it will be printed without quotes."),
    )
    parser.add_argument(
        "--ast",
        action="store_true",
        help=(
            "Only print the AST of the parsed expression.  Do not rely on this output, only useful for debugging purposes."
        ),
    )
    parser.usage = "{}\n  {}".format(
        parser.format_usage().partition("usage: ")[-1], __description__
    )

    args = parser.parse_args(argv[1:])
    expression = args.expression
    if expression == "help":
        parser.print_help()
        return 1

    if expression and args.expr_file:
        parser.error("Only use one of the expression or --expr-file arguments.")

    if args.expr_file:
        with open(args.expr_file, "rt") as f:
            expression = f.read()

    if args.ast:
        # Only print the AST
        expression = jmespath.compile(args.expression)
        sys.stdout.write(pprint.pformat(expression.parsed))
        sys.stdout.write("\n")
        return 0
    if args.filename:
        with open(args.filename, "rt") as f:
            data = json.load(f)
    else:
        data = sys.stdin.read()
        data = json.loads(data)

    result = jmespath.search(expression, data)

    dump_kwargs = dict(JP_COMPAT_DUMP_KWARGS)
    if args.compact:
        dump_kwargs.pop("indent", None)
        dump_kwargs["separators"] = (",", ":")

    output_result(args, dump_kwargs, result)
    return 0

jp_main.__description__ = __description__


def output_result(args, dump_kwargs, result):
    if args.quoted or not isinstance(result, str):
        result = json.dumps(result, **dump_kwargs)

    sys.stdout.write(result)

    if args.quoted or (
        not args.quoted and isinstance(result, str) and result[-1:] != "\n"
    ):
        sys.stdout.write("\n")


if __name__ == "__main__":
    sys.exit(jp_main(argv=sys.argv))
