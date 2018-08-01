#check: https://rules.sonarsource.com/java/RSPEC-1872
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/class_compare_name.java").uast
# cl_nodes = bblfsh.filter(uast, "//Identifier[@Name='equals' and @roleCall]//"
        # "Identifier[@Name='getName' or @Name='getSimpleName' and @roleCall]")

nodes = bblfsh.filter(uast, "//Identifier[@Name='equals' and @roleCall]/parent::*//"
        "Identifier[@Name='getName' or @Name='getSimpleName' and @roleCall]")

for node in nodes:
    print("Don't compare classes by name, line {}".format(node.start_position.line))
