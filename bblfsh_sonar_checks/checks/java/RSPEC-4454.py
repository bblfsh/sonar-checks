import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    eq_methods = bblfsh.filter(uast, "//MethodDeclaration/Identifier[@Name='equals']/parent::MethodDeclaration")

    for m in eq_methods:
        for c in m.children:
            if c.properties["internalRole"] == 'parameters':
                ann = bblfsh.filter(c, '//MarkerAnnotation//Identifier')
                ann_qualified = '.'.join([i.properties["Name"] for i in ann])

                if ann_qualified == "javax.annotation.Nonnull":
                    findings.append({"msg": "Don't use Nonnull annotation on equals methods",
                        "pos": c.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
