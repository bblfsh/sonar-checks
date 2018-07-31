# check: https://rules.sonarsource.com/java/RSPEC-4524
import utils
import re

import bblfsh

if __name__ == '__main__':
    client = bblfsh.BblfshClient("0.0.0.0:9432")

    uast = client.parse("../java/switch_default_nofinal.java").uast

    switches = bblfsh.filter(uast, "//SwitchStatement")
    for i in switches:
        cases = list(bblfsh.filter(i, "//SwitchCase"))
        if not cases:
            continue

        for r in range(len(cases)):
            c = cases[r]
            if bblfsh.role_id('DEFAULT') in c.roles and r != (len(cases)-1):
                    print("'default' should be the line switch case (line {})"
                        .format(c.start_position.line))
