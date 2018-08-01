# check: https://rules.sonarsource.com/java/RSPEC-131
import utils
import re

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/switch_nodefault.java").uast

switches = bblfsh.filter(uast, "//SwitchStatement")
for i in switches:
    cases = bblfsh.filter(i, "//SwitchCase")

    for c in cases:
        if bblfsh.role_id("DEFAULT") in c.roles:
            break
    else:
        print("Switch without default case at line {}".format(i.start_position.line))
