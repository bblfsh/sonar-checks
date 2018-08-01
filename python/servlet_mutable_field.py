# check: https://rules.sonarsource.com/java/RSPEC-2226
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/servlet_mutable_field.java").uast
classes = []
parent2children = {}
name2class = {}

cl_nodes = bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")

for cl in cl_nodes:
    jc = utils.JClass(cl)

    if jc.parent == 'HttpServlet':
        for f in jc.fields:
            if "static" not in f.modifiers and "final" not in f.modifiers:
                print("Servlet fields should be static or final, line: {}"
                        .format(f.node.start_position.line))
