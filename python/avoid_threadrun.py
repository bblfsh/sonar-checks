# check: https://rules.sonarsource.com/java/RSPEC-1217
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/avoid_threadrun.java").uast

# Note: this will find variables instanced from Thread but not assigns to other
# variables from these or returned values.
instance_vars = bblfsh.filter(uast, "//VariableDeclarationFragment/ClassInstanceCreation"
        "/SimpleType/Identifier[@Name='Thread']/ancestor::VariableDeclarationFragment"
        "/Identifier")

thread_vars = [i.properties["Name"] for i in instance_vars]

for tv in thread_vars:
    run_calls = bblfsh.filter(uast, "//*[@roleCall and @roleReceiver and @Name='%s']/" % tv +
            "parent::*/Identifier[@roleCall and @roleCallee and @Name='run']")

    for rc in run_calls:
        print("Don't call run on Thread instances, use start() instead, line: {}".format(
            rc.start_position.line))
