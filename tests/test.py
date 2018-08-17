import importlib
import os
from typing import Dict, Any, List
import unittest

from bblfsh_sonar_checks.utils import (
        get_checks_dir, get_languages, run_default_fixture, get_fixtures_dir,
        list_checks, run_check
)

import bblfsh


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

    def setUp(self):
        self.languages = get_languages()
        self.check_funcs: Dict[str, Dict[str, Any]] = {}
        self.fixtures: Dict[str, List[str]] = {}

        fixtures_dir = get_fixtures_dir()

        for lang in self.languages:
            self.check_funcs[lang] = {path: module.check for (module, path) in _get_check_modules(lang)}
            self.fixtures[lang] = [os.path.join(fixtures_dir, lang, i)
                                   for i in os.listdir(os.path.join(fixtures_dir, lang))]

        self.client = bblfsh.BblfshClient("0.0.0.0:9432")
        # FIXME XXX: call bblfsh.ensure_bblfsh_is_running


    def test_10_own_fixtures(self):
        for lang, checks in self.check_funcs.items():
            for check_path, check_func in checks.items():
                res = run_default_fixture(check_path, check_func, silent=True)
                self.assertGreater(len(res), 0)

    def test_20_other_fixtures(self):
        for lang in self.fixtures:
            for check_code in list_checks(lang):
                for fixture in self.fixtures[lang]:
                    if check_code in fixture:
                        continue

                    resp = self.client.parse(fixture)
                    self.assertEqual(resp.status, 0)
                    run_check(check_code, lang, resp.uast)