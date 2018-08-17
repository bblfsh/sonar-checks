import importlib
import os
import traceback
from typing import Dict, Any, List
import unittest

from bblfsh_sonar_checks.utils import (
        get_checks_dir, get_languages, run_default_fixture, get_fixtures_dir,
        list_checks, run_check, get_check_description, get_methods, Method, JClass,
        JClassField, Argument, hash_node, run_checks
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


class Test_10_Utils(unittest.TestCase):

    def _parse_source(self, code):
        self.client = bblfsh.BblfshClient("0.0.0.0:9432")
        path = "../bblfsh_sonar_checks/fixtures/java/%s.java" % code
        return self.client.parse(path).uast

    def test_0010_getlanguages(self):
        self.assertListEqual(get_languages(), ["java"])

    def test_0020_getchecksdir(self):
        # /home/juanjux/pyenv/versions/3.6.6/lib/python3.6/site-packages/bblfsh_sonar_checks/checks/java
        jcheck_dir = get_checks_dir("java")
        self.assertTrue(jcheck_dir.endswith("checks/java"))

    def test_0030_runchecks(self):
        uast = self._parse_source("RSPEC-1764")
        checks = ["RSPEC-1764", "RSPEC-2447"]
        results = run_checks(checks, "java", uast)
        self.assertEqual(len(results), len(checks))
        self.assertEqual(len(results["RSPEC-1764"]), 5)
        self.assertEqual(len(results["RSPEC-2447"]), 0)

    def test_0040_hashnode(self):
        uast = self._parse_source("RSPEC-1764")
        self.assertEqual(hash_node(uast).hexdigest(), "e3e8c1738c6a6d94276080d3c5322647")
        self.assertEqual(hash_node(uast, ignore_sideness=False).hexdigest(), "63c68a8dfbb7c5c5c14efc3c0a2c65d9")

    def test_0060_getmethods(self):
        uast = self._parse_source("RSPEC-2447")
        methods = get_methods(uast)
        self.assertEqual(len(methods), 1)
        self.assertIsInstance(methods[0], Method)
        self.assertEqual(methods[0].name, "test")
        self.assertListEqual(methods[0].modifiers, [])
        self.assertListEqual(methods[0].modifiers, [])
        self.assertIsNotNone(methods[0].return_)
        self.assertIsInstance(methods[0].return_, Argument)
        self.assertIsNotNone(methods[0].body)
        self.assertIsNotNone(methods[0].node)

    def test_0070_listchecks(self):
        for c in list_checks("java"):
            self.assertTrue(c.startswith("RSPEC-"))
            self.assertTrue(c[6:].isdigit())

    def test_0080_getcheckdescription(self):
        url = get_check_description("RSPEC-1143", "java")
        self.assertEqual(url , "https://rules.sonarsource.com/java/RSPEC-1143")


class Test_20_Checks(unittest.TestCase):

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

    def test_1000_own_fixtures(self):
        for lang, checks in self.check_funcs.items():
            for check_path, check_func in checks.items():
                res = run_default_fixture(check_path, check_func, silent=True)
                self.assertGreater(len(res), 0)

    def test_2000_other_fixtures(self):
        for lang in self.fixtures:
            for check_code in list_checks(lang):
                for fixture in self.fixtures[lang]:
                    if check_code in fixture:
                        continue

                    resp = self.client.parse(fixture)
                    self.assertEqual(resp.status, 0)
                    try:
                        run_check(check_code, lang, resp.uast)
                    except Exception:
                        self.fail("Check for code {} ({}) raised a Exception:".format(
                            check_code, lang, traceback.format_exc()))
