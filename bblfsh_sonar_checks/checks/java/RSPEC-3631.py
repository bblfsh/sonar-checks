import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    calls = bblfsh.filter(uast, "//MethodInvocation/"
            "Identifier[@roleCall and @roleReceiver and @Name='Arrays']/parent::MethodInvocation/"
            "Identifier[@roleCall and @roleCallee and @Name='asList']/parent::MethodInvocation")

    for c in calls:
        child_args = bblfsh.filter(c, "//*[@roleArgument and @roleLiteral]")
        if len(list(child_args)):
            findings.append({"msg": "Don't use slow Arrays.asList with primitives",
                "pos": c.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
