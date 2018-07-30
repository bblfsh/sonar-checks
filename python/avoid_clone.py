import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")
uast = client.parse("../java/avoid_clone.java").uast
methods = bblfsh.filter(uast, "//TypeDeclaration//FunctionGroup")
for method_node in methods:
    m = utils.Method(method_node)
    if m.name == "clone" and "public" in m.modifiers and m.return_.type_name == "Object":
        print("Don't use clone")
