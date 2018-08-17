import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    if any(filter(lambda m: m.name == "clone" and "public" in m.modifiers and
        m.return_ and m.return_.type_name == "Object", utils.get_methods(uast))):

        findings.append({"msg": "Don't use clone"})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
