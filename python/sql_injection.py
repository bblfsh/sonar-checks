# check: https://rules.sonarsource.com/java/RSPEC-3649
import utils
import re

import bblfsh

if __name__ == '__main__':
    client = bblfsh.BblfshClient("0.0.0.0:9432")

    uast = client.parse("../java/sql_injection.java").uast

    sql_commands = set({"SELECT", "UPDATE", "DELETE", "INSERT",
                        "CREATE", "ALTER", "DROP"})

    infixes = bblfsh.filter(uast, "//InfixExpression[@roleAdd and @roleBinary and @roleOperator]")
    for i in infixes:
        strs = bblfsh.filter(i, "//String[@internalRole='leftOperand']")
        for s in strs:
            first_word = s.properties["Value"].split()[0]
            if first_word in sql_commands:
                print("Potential SQL injection vulnerability at line {}"
                        .format(s.start_position.line))
