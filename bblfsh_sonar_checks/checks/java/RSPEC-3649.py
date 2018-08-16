import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    sql_commands = set({"SELECT", "UPDATE", "DELETE", "INSERT",
                        "CREATE", "ALTER", "DROP"})

    infixes = bblfsh.filter(uast, "//InfixExpression[@roleAdd and @roleBinary and @roleOperator]")
    for i in infixes:
        strs = bblfsh.filter(i, "//String[@internalRole='leftOperand']")
        for s in strs:
            first_word = s.properties["Value"].split()[0]
            if first_word in sql_commands:
                findings.append({"msg": "Potential SQL injection vulnerability",
                    "pos": s.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
