import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    fnls = bblfsh.filter(uast, "//*[@roleFinally]")

    for f in fnls:
        throws = bblfsh.filter(f, "//*[@roleThrow or @roleReturn]")

        for t in throws:
            findings.append({
                "msg": "Don't throw or return inside a finally (line {})".format(
                        t.start_position.col),
                "pos": t.start_position
            })

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
