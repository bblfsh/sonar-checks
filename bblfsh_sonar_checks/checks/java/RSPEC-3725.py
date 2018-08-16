import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    calls = bblfsh.filter(uast, "//MethodInvocation/"
            "Identifier[@roleCall and @roleReceiver and @Name='Files']/parent::MethodInvocation/"
            "Identifier[@roleCall and @roleCallee and @Name='exists' or @Name='notExists'"
            "or @Name='isDirectory' or @name='isRegularFile']/parent::MethodInvocation")

    for c in calls:
        findings.append({"msg": "Don't use slow Files.exist/notExists/isDirectory/isRegularFile",
            "pos": c.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
