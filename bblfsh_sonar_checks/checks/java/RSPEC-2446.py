import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    methods = utils.get_methods(uast)

    for m in methods:
        if "public" not in m.modifiers:
            ann_trans = bblfsh.filter(m.node, "//*[@roleAnnotation]/Identifier[@Name='Transactional']")
            for ann in ann_trans:
                findings.append({"msg": "@Transactional methods should be public",
                                 "pos": ann.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
