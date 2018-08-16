# check: https://rules.sonarsource.c../../java/RSPEC-2447
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/boolean_return_null.java").uast
methods = utils.get_methods(uast)

for m in methods:
    # Should look at the roles to filter by Boolean but there is a bug in the
    # Java driver https://github.com/bblf../../java-driver/issues/83 so we check the token
    if m.return_.type_name == 'boolean':
        if any(list(bblfsh.filter(m.body, "//*[@roleReturn]//*[@roleNull]"))):
            print("Don't return Null on Boolean-return methods")
