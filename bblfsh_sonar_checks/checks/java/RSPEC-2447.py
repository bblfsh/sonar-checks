import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    methods = utils.get_methods(uast)

    for m in methods:
        # Should look at the roles to filter by Boolean but there is a bug in the
        # Java driver https://github.com/bblf../../java-driver/issues/83 so we check the token
        if m.return_ and m.return_.type_name == 'boolean':
            if any(list(bblfsh.filter(m.body, "//*[@roleReturn]//*[@roleNull]"))):
                findings.append({"msg": "Don't return Null on Boolean-return methods"})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
