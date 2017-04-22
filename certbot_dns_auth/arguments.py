"""Validates and Stores CLI Arguments."""

import argparse


class Arguments(object):
    """Parses and (potentially) Stores Passed Arguments."""

    def __init__(self, argv):
        argparse.ArgumentParser()
