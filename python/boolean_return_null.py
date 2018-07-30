import utils

import bblfsh

if __name__ == '__main__':
    client = bblfsh.BblfshClient("0.0.0.0:9432")

    uast = client.parse("../java/boolean_return_null.java").uast
    methods = utils.get_methods(uast)

    for m in methods:
        print('XXX type :')
        print(m.return_.type_.roles)
