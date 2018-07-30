import utils

import bblfsh

if __name__ == '__main__':
    client = bblfsh.BblfshClient("0.0.0.0:9432")

    uast = client.parse("../java/classname_noshadow.java").uast

    cl_nodes = bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")

    for cl in cl_nodes:
        jc = utils.JClass(cl)
        if jc.parent.split('.')[-1] == jc.name:
            print('Class has same name as parent')

        for impl in jc.implements:
            if impl.split('.')[-1] == jc.name:
                print('Class has same name as interface')

