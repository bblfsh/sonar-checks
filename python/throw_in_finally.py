# check: https://rules.sonarsource.com/java/RSPEC-1143
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/throw_in_finally.java").uast
fnls = bblfsh.filter(uast, "//*[@roleFinally]")

for f in fnls:
    throws = bblfsh.filter(uast, "//*[@roleThrow or @roleReturn]")

    for t in throws:
        print("Don't throw or return inside a finally (line {})".format(t.start_position.line))
