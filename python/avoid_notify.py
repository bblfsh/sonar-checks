# check: https://rules.sonarsource.com/java/RSPEC-2446
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/avoid_notify.java").uast

cl_nodes = bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")

for cl in cl_nodes:
    jc = utils.JClass(cl)

    for method in jc.methods:
        if method.name == "run" and "public" in method.modifiers and not method.arguments:
            for notify_call in bblfsh.filter(method.node, "//MethodInvocation/Identifier"
                    "[@roleCall and @roleCallee and @Name='notify']"):
                print("Don't use notify(), use notifyAll(), line: {}"
                        .format(notify_call.start_position.line))
