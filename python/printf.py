# check: https://rules.sonarsource.com/java/RSPEC-2275
import re

import utils

import bblfsh

if __name__ == '__main__':
    client = bblfsh.BblfshClient("0.0.0.0:9432")

    uast = client.parse("../java/printf.java").uast

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
            print("Format string at line {} doesn't match number of args"
                    .format(format_str.start_position.line))

        # Validate type of args (for %d it should have the NumberLiteral role)
        for arg in args[1:]:
            froles = filter(lambda x: x == bblfsh.role_id('NUMBER'), arg.roles)
            if len(list(froles)) == 0:
                print("Format string argument (line {} col {}) is not numeric"
                        .format(arg.start_position.line, arg.start_position.col))
