# check: https://rules.sonarsource.c../../java/RSPEC-3067
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/synchonized_getclass.java").uast

cl_nodes = bblfsh.filter(uast, "//SynchronizedStatement/MethodInvocation"
        "/ThisExpression/parent::MethodInvocation/Identifier[@Name='getClass']")

for node in cl_nodes:
    print("Don't use this.getClass() to synchronize, use MyClass.class (line {})"
            .format(node.start_position.line))
