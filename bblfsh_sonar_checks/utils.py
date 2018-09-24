import glob
import hashlib
import importlib
import inspect
import json
import os
from typing import List, Dict, Any, Optional, Union, cast, Callable

import bblfsh

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
Check = Dict[str, Any]
Checks = List[Check]
CheckFnc = Callable[[bblfsh.Node], Checks]


class Argument:
    def __init__(self, node: bblfsh.Node) -> None:
        self.init = None
        self.type_ = None
        self.type_name = ''
        self.name = ''
        self.variadic = node.properties['Variadic'] == 'true'
        self.map_variadic = node.properties['MapVariadic'] == 'true'
        self.receiver = node.properties['Receiver'] == 'true'

        for c in node.children:
            if c.properties["internalRole"] == "Init":
                self.init = c
            elif c.properties["internalRole"] == "Type":
                self.type_ = c
                types = list(bblfsh.filter(node, "//Identifier"))
                if types:
                    self.type_name = types[0].properties['Name']
                else:
                    try:
                        self.type_name = node.children[0].token
                    except ValueError:
                        self.type_name = ''
            elif c.properties["internalRole"] == "Name":
                self.name = c.properties["Name"]


class Method:
    def __init__(self, node: bblfsh.Node) -> None:
        self.node = node
        self.modifiers: List[str] = []
        self.arguments: List[Argument] = []
        self.name = ''
        self.return_: Optional[Argument] = None
        self.body: bblfsh.Node = None

        for node in node.children:
            if node.internal_type == "Alias":

                for c in node.children:
                    if c.internal_type == "Identifier":
                        self.name = c.properties["Name"]

                    elif c.internal_type == "Function":
                        for fc in c.children:
                            if fc.internal_type == "FunctionType":

                                for ftc in fc.children:
                                    if ftc.properties["internalRole"] == "Returns":
                                        self.return_ = Argument(ftc)

                                    elif ftc.properties["internalRole"] == "Arguments":
                                        self.arguments.append(Argument(ftc))

                            elif fc.internal_type == "Block":
                                self.body = fc

            elif node.internal_type == "Modifier":
                self.modifiers.append(node.token)


class JClassField:
    def __init__(self, node: bblfsh.Node) -> None:
        self.name = ''
        self.node = node
        self.modifiers: List[str] = []
        self.type_name = ''

        name_node = list(bblfsh.filter(node, "//VariableDeclarationFragment/Identifier"))[0]
        self.name = name_node.properties["Name"]

        modifier_nodes = bblfsh.filter(node, "//Modifier")
        for m in modifier_nodes:
            self.modifiers.append(m.token)

        type_node = list(bblfsh.filter(node, "//*[@roleType]"))[0]
        if type_node.internal_type == "SimpleType":
            self.type_name = list(bblfsh.filter(type_node, "//Identifier"))[0].properties["Name"]


class JClass:
    def __init__(self, node: bblfsh.Node) -> None:
        self.name = ''
        self.methods: List[Method] = []
        self.parent = ''
        self.implements: List[str] = []
        self.node = node
        self.body_declarations: List[bblfsh.Node] = []

        fields = bblfsh.filter(node, "//FieldDeclaration")
        self.fields = [JClassField(i) for i in fields]

        for c in node.children:
            if c.properties["internalRole"] == "name":
                self.name = c.properties["Name"]

            elif c.properties["internalRole"] == "superclassType":
                names = bblfsh.filter(c, "//Identifier")
                self.parent = '.'.join([i.properties["Name"] for i in names])

            elif c.properties["internalRole"] == "superInterfaceTypes":
                for iface in c.children:
                    names = bblfsh.filter(iface, "//Identifier")
                    names_qualified = '.'.join([i.properties["Name"] for i in names])
                    self.implements.append(names_qualified)

            elif c.properties["internalRole"] == "bodyDeclarations":
                self.body_declarations.append(c)

        self.methods = get_methods(node)


def get_methods(node: bblfsh.Node) -> List[Method]:
    return [Method(i) for i in bblfsh.filter(node, "//TypeDeclaration//FunctionGroup")]


def hash_node(node: bblfsh.Node, ignore_sideness: bool=True) -> hashlib._hashlib.HASH:
    """ Hashes a node ignoring positional information """

    lroles = [str(i) for i in node.roles if i not in (bblfsh.role_id("LEFT"),
                                                      bblfsh.role_id("RIGHT"))]

    _hash = hashlib.md5()
    stuff = [node.internal_type, node.token] + lroles

    for prop, value in sorted(node.properties.items()):
        if ignore_sideness and 'left' in value.lower() or 'right' in value.lower():
            continue
        stuff.append(prop)
        stuff.append(value)

    child_hashes = []
    for child in node.children:
        child_hashes.append(hash_node(child, ignore_sideness)
                            .hexdigest().encode('utf-8'))

    stuff.extend(sorted(child_hashes))

    for s in stuff:
        _hash.update(str(s).encode('utf-8'))

    return _hash


def instanced_calls(root_node: bblfsh.Node, type_name: str, method_name: str) -> List[bblfsh.Node]:
    """
    Detect a call from a symbol previously instanced from a certain type. This is
    somewhat fuzzy because it will give false positives for another symbol with
    the same name declared from another type, an improvement would se
    """

    # key: class name, value: list of usage positions
    all_usages: List[bblfsh.Node] = []

    def search_usages(instance_node: bblfsh.Node, search_node: bblfsh.Node) -> List[bblfsh.Node]:
        these_usages = []

        instance_search_query = "//VariableDeclarationFragment/ClassInstanceCreation" + \
                                "/SimpleType/Identifier[@Name='%s']" % type_name + \
                                "/ancestor::VariableDeclarationFragment/Identifier"

        usage_search_query = "//*[@roleCall and @roleReceiver and @Name='%s']/" + \
                             "parent::*/Identifier[@roleCall and @roleCallee and " + \
                             "@Name='{}']".format(method_name)

        _vars = bblfsh.filter(instance_node, instance_search_query)

        for var in _vars:
            usages = bblfsh.filter(search_node, usage_search_query % var.properties["Name"])
            these_usages.extend(list(usages))

        return these_usages

    jclasses = [JClass(i) for i in bblfsh.filter(root_node, "//*[@roleType and @roleDeclaration]")]

    for jc in jclasses:
        # Get usages of the instance declarations in all the class
        for bd in jc.fields:
            all_usages.extend(search_usages(bd.node, jc.node))

        # Get the usages of the inside-method declarations inside their own methods
        for method in jc.methods:
            all_usages.extend(search_usages(method.body, method.body))

    return all_usages


def get_languages() -> List[str]:
    langs_dir = os.path.join(THIS_PATH, "checks")

    res = []
    for p in os.listdir(langs_dir):
        full_path = os.path.join(langs_dir, p)
        if not os.path.isdir(full_path) or p in ["__pycache__"]:
            continue
        res.append(p)
    return res


def get_fixtures_dir() -> str:
    return os.path.join(THIS_PATH, "fixtures")


def get_checks_dir(lang: str) -> str:
    return os.path.join(THIS_PATH, "checks", lang)


class RunCheckException(Exception):
    pass


def run_check(check_code: str, lang: str, uast: bblfsh.Node, json_result: bool = False) \
        -> Union[str, Checks]:

    check_code = check_code.upper()
    check_path = os.path.join(THIS_PATH, "checks", lang, check_code + ".py")

    if not os.path.exists(check_path):
        raise RunCheckException("Could not find check '{}' for language '{}'"
                                .format(check_code, lang))

    check_module = importlib.import_module("bblfsh_sonar_checks.checks.{}.{}".format(lang, check_code))
    checks: Checks = check_module.check(uast)

    for c in checks:
        if "pos" not in c:
            c["pos"] = None
        else:
            p = c["pos"]
            c["pos"] = {"line": p.line, "col": p.col, "offset": p.offset}

    if json_result:
        return json.dumps(checks)

    return checks


def run_checks(check_codes: List[str], lang: str, uast: bblfsh.Node, json_result: bool = False) \
        -> Union[str, Dict[str, Checks]]:

    res: Dict[str, Checks] = {}

    for code in check_codes:
        res[code] = cast(Checks, run_check(code, lang, uast))

    if json_result:
        return json.dumps(res)

    return res


def run_default_fixture(path: str, check_fnc: CheckFnc, conn_str: str = "0.0.0.0:9432", silent: bool=False) \
        -> Checks:

    from pprint import pprint

    client = bblfsh.BblfshClient(conn_str)
    language = os.path.normpath(os.path.abspath(inspect.getfile(check_fnc))).split(os.sep)[-2]
    fixture_path = os.path.join(THIS_PATH, "fixtures", language, os.path.split(path)[1][:-3] + ".java")
    res = check_fnc(client.parse(fixture_path).uast)
    if not silent:
        pprint(res)

    return res

def list_langs() -> List[str]:
    langs_path = os.path.join(THIS_PATH, "checks")
    return list(filter(lambda x: not x.startswith("_"), next(os.walk(langs_path))[1]))


def list_checks(lang: str) -> List[str]:
    checks_path = os.path.join(THIS_PATH, "checks", lang)
    return [i.split("/")[-1][:-3] for i in glob.glob(checks_path + "/RSPEC-*")]


def get_check_description(check: str, lang: str) -> str:
    # FIXME: Improve this so it returns the descriptive text inside the HTML
    return "https://rules.sonarsource.com/{}/{}".format(lang, check)
