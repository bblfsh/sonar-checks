import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    # cl_nodes = bblfsh.filter(uast, "//Identifier[@Name='equals' and @roleCall]//"
            # "Identifier[@Name='getName' or @Name='getSimpleName' and @roleCall]")

    nodes = bblfsh.filter(uast, "//Identifier[@Name='equals' and @roleCall]/parent::*//"
            "Identifier[@Name='getName' or @Name='getSimpleName' and @roleCall]")

    for node in nodes:
        findings.append({"msg": "Don't compare classes by name, line {}",
                         "pos": node.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
