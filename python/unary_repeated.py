# check: https://rules.sonarsource.com/java/RSPEC-2761
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/unary_repeated.java").uast

unary_repeated = bblfsh.filter(uast, "//*[@roleUnary and @roleOperator]/*[@roleUnary and @roleOperator]")

processed_lines = set()

for ur in unary_repeated:
    line = ur.start_position.line

    if line in processed_lines:
        continue

    print("Don't repeat Unary operators, line {}".format(line))
    processed_lines.add(line)
