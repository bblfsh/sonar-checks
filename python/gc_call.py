# check: https://rules.sonarsource.com/java/RSPEC-1215
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/gc_call.java").uast
fin_calls = bblfsh.filter(uast, "//MethodInvocation//"
        "Identifier[@roleCall and @roleReceiver and @Name='System']/parent::MethodInvocation/"
        "Identifier[@roleCall and @roleCallee and @Name='gc']/parent::MethodInvocation")

if len(list(fin_calls)):
    print("Don't use System.gc()")

fin_calls = bblfsh.filter(uast, "//MethodInvocation//"
        "Identifier[@roleCall and @roleReceiver and @Name='Runtime']/parent::MethodInvocation//"
        "Identifier[@roleCall and @roleCallee and @Name='getRuntime']/parent::MethodInvocation/parent::MethodInvocation//"
        "Identifier[@roleCall and @roleCallee and @Name='gc']/parent::MethodInvocation")

if len(list(fin_calls)):
    print("Don't use Runtime.getRuntime().gc(})")
