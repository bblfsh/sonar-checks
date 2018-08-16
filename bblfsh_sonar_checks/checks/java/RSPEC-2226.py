import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    classes = []
    parent2children = {}
    name2class = {}

    cl_nodes = bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")

    for cl in cl_nodes:
        jc = utils.JClass(cl)

        if jc.parent == 'HttpServlet':
            for f in jc.fields:
                if "static" not in f.modifiers and "final" not in f.modifiers:
                    findings.append({"msg": "Servlet fields should be static or final",
                                     "pos": f.node.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
