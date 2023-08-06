import argparse
import shlex

import pytest
from koalak import ArgparseSubcmdHelper


def test_simple():
    class GitCommand(ArgparseSubcmdHelper):
        name = "git"

        # push
        def parser_push(self, parser):
            pass

        def run_push(self, args):
            pass

        # pull
        def parser_pull(self, parser):
            pass

        def run_pull(self, args):
            pass

    git_cmd = GitCommand()

    git_cmd.main(shlex.split("push"))
    git_cmd.main(shlex.split("pull"))
