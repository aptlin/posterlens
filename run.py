# Copyright (c) 2021 Sasha Aptlin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from argparse import ArgumentParser

from posterlens import PosterLens


def collect():
    parser = ArgumentParser()
    parser.add_argument("--size", default="25M", type=str.lower)
    args = parser.parse_args()
    posterlens_client = PosterLens(args.size)
    posterlens_client.collect()


if __name__ == "__main__":
    collect()
