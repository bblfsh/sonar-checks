# check: https://rules.sonarsource.com/java/RSPEC-128
import utils
import re

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/switch_nobreak.java").uast

switches = bblfsh.filter(uast, "//SwitchStatement")
for i in switches:
    cases = bblfsh.filter(i, "//SwitchCase")

    for c in cases:
        breaks = bblfsh.filter(c, "//*[@roleCase and @roleBreak]")
        if len(list(breaks)) == 0:
            print("Switch without break at line {}".format(c.start_position.line))
