import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    calls = bblfsh.filter(uast, "//MethodInvocation/Identifier"
            "[@roleCall and @roleCallee and (@Name='indexOf' or "
            "@Name='lastIndexOf' or @Name='startsWith')]/parent::MethodInvocation")

    for c in calls:
        substr_calls = bblfsh.filter(c, "//MethodInvocation/Identifier[@roleCall "
                "and @roleCallee and @Name='substring']")

        for sc in substr_calls:
            findings.append({"msg": "Don't use indexOf, lastIndexOf or startsWith chainged with substring",
                "pos": sc.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
