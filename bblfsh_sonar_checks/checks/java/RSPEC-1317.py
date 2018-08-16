import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    instances = bblfsh.filter(uast, "//*[@roleCall and @roleInstance]/*[@roleType]/Identifier"
           "[@Name='StringBuilder' or @Name='StringBuffer']/parent::*/parent::*/*[@roleArgument "
           "and @roleCharacter and @roleLiteral]")

    for i in instances:
        findings.append({"msg": "Dangerous instantiation of StringBuffer or StringBuilder with character argument",
                         "pos": i.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
