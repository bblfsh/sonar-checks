import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    fin_calls = bblfsh.filter(uast, "//MethodInvocation//"
            "Identifier[@roleCall and @roleReceiver and @Name='System']/parent::MethodInvocation/"
            "Identifier[@roleCall and @roleCallee and @Name='gc']/parent::MethodInvocation")

    if len(list(fin_calls)):
        findings.append({"msg": "Don't use System.gc()", "pos": None})

    fin_calls = bblfsh.filter(uast, "//MethodInvocation//"
            "Identifier[@roleCall and @roleReceiver and @Name='Runtime']/parent::MethodInvocation//"
            "Identifier[@roleCall and @roleCallee and @Name='getRuntime']/parent::MethodInvocation/parent::MethodInvocation//"
            "Identifier[@roleCall and @roleCallee and @Name='gc']/parent::MethodInvocation")

    if len(list(fin_calls)):
        findings.append({"msg": "Don't use Runtime.getRuntime().gc(})", "pos": None})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
