import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    asgns = bblfsh.filter(uast, "//Assignment")

    for a in asgns:
        ids = bblfsh.filter(a, "//Identifier[@internalRole='leftHandSide' and "
                "@Name='passwd' or @Name='pass' or @Name='password']")
        for i in ids:
            strs = bblfsh.filter(a, "//String[@internalRole='rightHandSide']")
            for s in strs:
                findings.append({"msg": "Hardcoded assignment to password",
                                 "pos": s.start_position})

    inits = bblfsh.filter(uast, "//VariableDeclarationStatement")
    for init in inits:
        ids = bblfsh.filter(init, "//Identifier[@internalRole='name' and @Name='passwd' "
                "or @Name='pass' or @Name='password']")
        for i in ids:
            type_ = bblfsh.filter(init, "//SimpleType/Identifier[@Name='String']")
            if len(list(type_)) > 0:
                findings.append({"msg": "Hardcoded initialization to password",
                                 "pos": i.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
