from bblfsh_sonar_checks.utils import (
        get_checks_dir, get_languages, run_default_fixture
)

import importlib
import os
import unittest

# FIXME XXX: Write the tests:
"""
Test should do at a minimum:
    - Run each check with its default java file and check that there are results.
    - Run each check with all other others java files and check that it doesn't crash.
    - Run each class, method and function in the utils module
"""

def _get_check_modules(lang):
    checks_dir = get_checks_dir(lang)
    check_files = os.listdir(checks_dir)
    check_modules = []

    for f in check_files:
        if not f.startswith("RSPEC-") or not f.endswith(".py"):
            continue

        check_modules.append((
            importlib.import_module("bblfsh_sonar_checks.checks.{}.{}".format(lang, os.path.splitext(f)[0])),
            os.path.join(checks_dir, f)))

    return check_modules

# FIXME XXX: check also all the utils functions

class CheckTests(unittest.TestCase):

    def test_own_fixtures(self):
        for lang in get_languages():
            for module, path in _get_check_modules(lang):
                run_default_fixture(path, module.check)
