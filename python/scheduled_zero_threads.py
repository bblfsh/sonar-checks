# check: https://rules.sonarsource.com/java/RSPEC-2122
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/scheduled_zero_threads.java").uast
inst = bblfsh.filter(uast, "//ClassInstanceCreation/*[@internalRole='arguments'"
        " and @roleNumber and @token='0']/parent::*//Identifier/"
        "parent::SimpleType[@roleCall and @roleCallee and @roleType]")

for i in inst:
    print("Don't instantiate ScheduledThreadPoolExecutes with an argument of 0"
          " at line {}".format(i.start_position.line))
