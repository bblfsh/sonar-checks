# check: https://rules.sonarsource.com/java/RSPEC-1317
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/stringbuilder_char.java").uast
instances = bblfsh.filter(uast, "//*[@roleCall and @roleInstance]/*[@roleType]/Identifier"
       "[@Name='StringBuilder' or @Name='StringBuffer']/parent::*/parent::*/*[@roleArgument "
       "and @roleCharacter and @roleLiteral]")

for i in instances:
    print("Dangerous instantiation of StringBuffer or StringBuilder with character argument "
            "at line {}".format(i.start_position.line))
