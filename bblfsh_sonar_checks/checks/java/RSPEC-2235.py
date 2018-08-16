import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    catchs = bblfsh.filter(uast, "//CatchClause//SimpleType//Identifier[@Name='IllegalMonitorStateException']")

    for c in catchs:
        findings.append({"msg": "Don't catch IllegalMonitorStateException",
                         "pos": c.start_position.line})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
