# check: https://rules.sonarsource.com/java/RSPEC-3631
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/arrays_aslist.java").uast
calls = bblfsh.filter(uast, "//MethodInvocation/"
        "Identifier[@roleCall and @roleReceiver and @Name='Arrays']/parent::MethodInvocation/"
        "Identifier[@roleCall and @roleCallee and @Name='asList']/parent::MethodInvocation")

for c in calls:
    child_args = bblfsh.filter(c, "//*[@roleArgument and @roleLiteral]")
    if len(list(child_args)):
        print("Don't use slow Arrays.asList with primitives, line: {}"
                .format(c.start_position.line))
