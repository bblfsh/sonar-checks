import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    methods = utils.get_methods(uast)
    for m in methods:
        if m.return_ is None and m.name == "finalize" and 'public' in m.modifiers:
            findings.append({"msg": "Don't use a public finalize()",
                             "pos": m.node.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
