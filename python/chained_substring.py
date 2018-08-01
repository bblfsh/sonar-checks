# check: https://rules.sonarsource.com/java/RSPEC-4635
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/chained_substring.java").uast

calls = bblfsh.filter(uast, "//MethodInvocation/Identifier"
        "[@roleCall and @roleCallee and (@Name='indexOf' or "
        "@Name='lastIndexOf' or @Name='startsWith')]/parent::MethodInvocation")

for c in calls:
    substr_calls = bblfsh.filter(c, "//MethodInvocation/Identifier[@roleCall "
            "and @roleCallee and @Name='substring']")

    for sc in substr_calls:
        print("Don't use indexOf, lastIndexOf or startsWith chainged with "
                "substring (line {})".format(sc.start_position.line))
