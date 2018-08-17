import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    methods = utils.get_methods(uast)

    for m in methods:
        if m.name == "equals" and m.return_ and m.return_.type_name == "boolean" and \
                "public" in m.modifiers:
            args = m.arguments
            if len(args) != 1:
                findings.append({"msg": "equals method should have only one Object argument",
                                 "pos": m.node.start_position})

            if args[0].type_name != "Object":
                findings.append({"msg": "equals should be declared with an argument of type Object",
                                 "pos": m.node.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
