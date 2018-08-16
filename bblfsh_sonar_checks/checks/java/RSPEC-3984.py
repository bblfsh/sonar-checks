import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    instances = bblfsh.filter(uast, "//ClassInstanceCreation//Identifier"
            "[substring(@Name, string-length(@Name) - string-length('Exception') +1) = 'Exception']"
            "/parent::*/parent::*/parent::*")

    for i in instances:
        if i.internal_type != 'ThrowStatement':
            findings.append({"msg": 'Probably exception creation without throw',
                "pos": i.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
