import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    cl_nodes = bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")
    jclasses = [utils.JClass(i) for i in cl_nodes]

    for jc in jclasses:
        if jc.parent == 'HttpServlet':
            mains = bblfsh.filter(uast, "//FunctionGroup//Alias/Identifier[@Name='main']")
            for m in mains:
                findings.append({"msg": "Don't use a main() function on HttpServlet derived classes",
                                 "pos": m.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
