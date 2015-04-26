#!/usr/bin/env python
# encoding: utf-8

import os
import logging
logger = logging.getLogger(__name__)

from jinja2 import Environment, FileSystemLoader


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="TODO: description of the utility")
    parser.add_argument("-v", "--verbose", action="count", help="the logging verbosity (more gives more detail)")
    parser.add_argument("-t", "--template_dir", default="templates", help="Location of the template directory (default: %(default)s)")
    parser.add_argument("-o", "--output_dir", default="html", help="Location of the output directory (default: %(default)s)")
    args = parser.parse_args()

    if args.verbose == 1:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(format="%(levelname)s %(asctime)s: %(message)s")
    logger.setLevel(level)

    return args


def main():
    args = get_args()
    env = Environment(loader=FileSystemLoader(args.template_dir))

    try:
        os.makedirs(args.output_dir)
    except FileExistsError:
        pass

    for dirpath, dirnames, filenames in os.walk(args.template_dir):
        for filename in filenames:
            if not filename.endswith(".html"):
                continue
            input_path = filename
            template = env.get_template(input_path)
            result = template.render()
            path = os.path.join(args.output_dir, input_path)
            with open(path, "w") as of:
                of.write(result)


if __name__ == '__main__':
    main()
