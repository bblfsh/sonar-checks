import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    fin_calls = bblfsh.filter(uast, "//MethodInvocation/BooleanLiteral[@internalRole='arguments'"
            " and @booleanValue='true']/parent::MethodInvocation/"
            "Identifier[@roleCall and @roleReceiver and @Name='System']/parent::MethodInvocation/"
            "Identifier[@roleCall and @roleCallee and @Name='runFinalizersOnExit']/parent::MethodInvocation")

    if len(list(fin_calls)):
        findings.append({"msg": "Don't use System.runFinalizersOnExit"})


    methods = utils.get_methods(uast)
    for m in methods:
        if m.return_ is None and m.name == "finalize":
            findings.append({"msg": "Don't override finalize()"})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
