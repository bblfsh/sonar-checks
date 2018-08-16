import bblfsh_sonar_checks.utils as utils

import bblfsh

import re

def check(uast):
    findings = []


    format_calls = bblfsh.filter(uast, "//MethodInvocation/"
            "Identifier[@roleCall and @roleReceiver and @Name='String']/parent::MethodInvocation/"
            "Identifier[@roleCall and @roleCallee and @Name='format']/parent::MethodInvocation")

    for fcall in format_calls:
        args = list(bblfsh.filter(fcall, "//*[@internalRole='arguments']"))
        if len(args) == 0:
            continue

        format_str = args[0]
        if format_str.internal_type != 'String':
            # Validating format strings assigned elsewhere on the same file is possible,
            # but won't be doing it here for brevity sake
            continue


        # For the reason stated above, we only validate %d
        str_val = format_str.properties["Value"]
        re_res = re.findall(r'[^%]%d', str_val)

        # Validate number of args
        if len(re_res) != len(args[1:]):
            findings.append({"msg": "Format string doesn't match number of args",
                             "pos": format_str.start_position})

        # Validate type of args (for %d it should have the NumberLiteral role)
        for arg in args[1:]:
            froles = filter(lambda x: x == bblfsh.role_id('NUMBER'), arg.roles)
            if len(list(froles)) == 0:
                findings.append({"msg": "Format string argument is not numeric",
                                 "pos": arg.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
