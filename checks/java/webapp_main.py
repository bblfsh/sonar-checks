# check: https://rules.sonarsource.c../../java/RSPEC-2653
import utils
import re

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/webapp_main.java").uast

cl_nodes = bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")
jclasses = [utils.JClass(i) for i in cl_nodes]

for jc in jclasses:
    if jc.parent == 'HttpServlet':
        mains = bblfsh.filter(uast, "//FunctionGroup//Alias/Identifier[@Name='main']")
        for m in mains:
            print("Don't use a main() function on HttpServlet derived classes "
                  "(line {})".format(m.start_position.line))
