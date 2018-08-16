import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    for usage in utils.instanced_calls(uast, "File", "delete"):
        findings.append({"msg": "Don't call delete() on java.io.File instances, use java.nio.File.delete()",
            "pos": usage.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
