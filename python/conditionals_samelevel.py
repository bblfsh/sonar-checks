import utils

import bblfsh

if __name__ == '__main__':
    client = bblfsh.BblfshClient("0.0.0.0:9432")

    uast = client.parse("../java/conditionals_samelevel.java").uast
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
                print("First statement after If in line {} not indented".format(
                      if_stmt.start_position.line))
