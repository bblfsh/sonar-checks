import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    unary_repeated = bblfsh.filter(uast, "//*[@roleUnary and @roleOperator]/*[@roleUnary and @roleOperator]")

    processed_lines = set()

    for ur in unary_repeated:
        line = ur.start_position.line

        if line in processed_lines:
            continue

        findings.append({"msg": "Don't repeat Unary operators",
            "pos": ur.start_position})

        processed_lines.add(line)

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
