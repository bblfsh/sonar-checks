# check: https://rules.sonarsource.com/java/RSPEC-1217
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/avoid_threadrun.java").uast

usages = utils.instanced_calls(uast, "Thread", "run")
for u in usages:
    print("Don't call run on Thread instances, use start() instead, line: {}".format(
        u.start_position.line))
