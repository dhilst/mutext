#!/usr/bin/env python3
"""Thin shim: see zebra_checker/cli.py and docs/sat-checker.md."""

import sys

from zebra_checker.cli import main

if __name__ == "__main__":
    sys.exit(main())
