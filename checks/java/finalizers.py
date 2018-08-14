# check: https://rules.sonarsource.c../../java/RSPEC-2151
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/finalizers.java").uast
fin_calls = bblfsh.filter(uast, "//MethodInvocation/BooleanLiteral[@internalRole='arguments'"
        " and @booleanValue='true']/parent::MethodInvocation/"
        "Identifier[@roleCall and @roleReceiver and @Name='System']/parent::MethodInvocation/"
        "Identifier[@roleCall and @roleCallee and @Name='runFinalizersOnExit']/parent::MethodInvocation")

if len(list(fin_calls)):
    print("Don't use System.runFinalizersOnExit")


methods = utils.get_methods(uast)
for m in methods:
    if m.return_ is None and m.name == "finalize":
        print("Don't override finalize()")
