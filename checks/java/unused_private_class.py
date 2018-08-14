# check: https://rules.sonarsource.c../../java/RSPEC-3985
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/unused_private_class.java").uast

for cl in [utils.JClass(i) for i in bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")]:
    instance_creations = bblfsh.filter(cl.node, "//ClassInstanceCreation/SimpleType/Identifier")
    all_creations = {i.properties["Name"] for i in instance_creations}

    for cls in [utils.JClass(i) for i in
            bblfsh.filter(cl.node, "//TypeDeclaration//TypeDeclaration")]:
        for child in cls.node.children:
            if child.internal_type == "Modifier" and child.token == "private" and\
                cls.name not in all_creations:
                print("Private class {} defined but not used, remove it, line: {}"
                        .format(cls.name, cls.node.start_position.line))
