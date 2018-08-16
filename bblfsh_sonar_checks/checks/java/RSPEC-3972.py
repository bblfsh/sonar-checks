import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    cl_nodes = bblfsh.filter(uast, "//IfStatement")

    for if_stmt in cl_nodes:
        if_col = if_stmt.start_position.col

        for c in if_stmt.children:
            then = bblfsh.filter(c, "//*[@roleBody and @roleThen]")

            for then_stmt in then:
                first_col = then_stmt.start_position.col
                break
            else:
                continue

            if if_stmt.start_position.col == first_col:
                findings.append({"msg": "First statement after If not indented",
                    "pos": if_stmt.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
