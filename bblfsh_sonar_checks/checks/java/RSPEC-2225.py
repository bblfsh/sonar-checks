import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    def returnsNull(node):
        return any(list(bblfsh.filter(node, "//*[@roleReturn]//*[@roleNull]")))

    methods = utils.get_methods(uast)

    for m in methods:
        if (m.name == "toString" and "public" in m.modifiers and m.return_ and m.return_.type_name == "String"
               and not m.arguments) or\
           (m.name == "clone" and "public" in m.modifiers and m.return_ and m.return_.type_name == "Object"
               and not m.arguments):
            if returnsNull(m.node):
                findings.append({"msg": "Don't return Null on toString or clone methods",
                                 "pos": m.node.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
