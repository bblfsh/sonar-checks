import utils

import bblfsh

if __name__ == '__main__':
    client = bblfsh.BblfshClient("0.0.0.0:9432")

    uast = client.parse("../java/hardcoded_passwd.java").uast
    asgns = bblfsh.filter(uast, "//Assignment")

    for a in asgns:
        ids = bblfsh.filter(a, "//Identifier[@Name='passwd' or @Name='pass' or @Name='password']")
        for i in ids:
            if i.properties["internalRole"] == 'leftHandSide':
                strs = bblfsh.filter(a, "//String")
                for s in strs:
                    if s.properties["internalRole"] == 'rightHandSide':
                        print("Hardcoded assignment to password at line {}".format(s.start_position.line))

    inits = bblfsh.filter(uast, "//VariableDeclarationStatement")
    for init in inits:
        ids = bblfsh.filter(init, "//Identifier[@Name='passwd' or @Name='pass' or @Name='password']")
        for i in ids:
            if i.properties["internalRole"] == 'name':
                type_ = bblfsh.filter(init, "//SimpleType/Identifier[@Name='String']")
                if len(list(type_)) > 0:
                    print("Hardcoded initialization to password at line {}".format(i.start_position.line))






