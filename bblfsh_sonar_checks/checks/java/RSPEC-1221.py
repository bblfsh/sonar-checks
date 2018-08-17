import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    bad_methods = (
            ('hashcode', 'int', 'hashCode'),
            ('tostring', 'String', 'toString'),
            ('equal', 'boolean', 'equals'),
    )

    for method in utils.get_methods(uast):
        if "public" not in method.modifiers:
            continue

        for tup in bad_methods:
            if method.name == tup[0] and method.return_ and method.return_.type_name == tup[1]:
                findings.append({"msg": "Probably misnamed method '{}' instead of '{}'"
                                    .format(method.name, tup[2]),
                                 "pos": method.node.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
