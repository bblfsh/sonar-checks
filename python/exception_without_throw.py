import utils

import bblfsh

if __name__ == '__main__':
    client = bblfsh.BblfshClient("0.0.0.0:9432")

    uast = client.parse("../java/exception_without_throw.java").uast
    instances = bblfsh.filter(uast, "//ClassInstanceCreation//Identifier"
            "[substring(@Name, string-length(@Name) - string-length('Exception') +1) = 'Exception']"
            "/parent::*/parent::*/parent::*")

    for i in instances:
        if i.internal_type != 'ThrowStatement':
            print('Probably exception creation without throw at line {}'.format(
                i.start_position.line
            ))

