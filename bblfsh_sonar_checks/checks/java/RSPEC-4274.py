import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    methods = utils.get_methods(uast)

    for m in methods:
        if "public" not in m.modifiers:
            continue

        for arg in m.arguments:
            for a in bblfsh.filter(m.node, "//AssertStatement//Identifier[@Name='%s']"
                                            % arg.name):
                findings.append({"msg": "Don't use asserts with public method parameters",
                    "pos": a.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
