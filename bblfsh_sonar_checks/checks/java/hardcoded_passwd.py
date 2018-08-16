# check: https://rules.sonarsource.com/java/RSPEC-2068
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/hardcoded_passwd.java").uast
asgns = bblfsh.filter(uast, "//Assignment")

for a in asgns:
    ids = bblfsh.filter(a, "//Identifier[@internalRole='leftHandSide' and "
            "@Name='passwd' or @Name='pass' or @Name='password']")
    for i in ids:
        strs = bblfsh.filter(a, "//String[@internalRole='rightHandSide']")
        for s in strs:
            print("Hardcoded assignment to password at line {}".format(s.start_position.line))

inits = bblfsh.filter(uast, "//VariableDeclarationStatement")
for init in inits:
    ids = bblfsh.filter(init, "//Identifier[@internalRole='name' and @Name='passwd' "
            "or @Name='pass' or @Name='password']")
    for i in ids:
        type_ = bblfsh.filter(init, "//SimpleType/Identifier[@Name='String']")
        if len(list(type_)) > 0:
            print("Hardcoded initialization to password at line {}".format(i.start_position.line))
