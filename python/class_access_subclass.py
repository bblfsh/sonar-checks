# check: https://rules.sonarsource.com/java/RSPEC-2390
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/class_access_subclass.java").uast
classes = []
parent2children = {}
name2class = {}

cl_nodes = bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")

for cl in cl_nodes:
    jc = utils.JClass(cl)
    name2class[jc.name] = jc

    if jc.parent in parent2children:
        parent2children[jc.parent].append(jc.name)
    else:
        parent2children[jc.name] = [jc.parent]

    classes.append(jc)
    name2class[jc.name] = cl


for cl in parent2children:
    for child in parent2children[cl]:
        # Alternative: generate a string with all the child names in the Identifier selector
        calls = bblfsh.filter(name2class[cl],
                "(//MethodInvocation//Identifier[@roleCall and @roleReceiver and @Name='%s']|"
                "//QualifiedIdentifier//Identifier[@Name='%s'])" % (child, child))
        for call in calls:
            print("Call in class {} to subclass {} member (line {})".format(
                cl, child, call.start_position.line))
