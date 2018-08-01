# check: https://rules.sonarsource.com/java/RSPEC-1862
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/elif_repeated_condition.java").uast

if_nodes = bblfsh.filter(uast, "//*[@roleIf and @roleStatement and not(@roleElse)]")

def hash_condition(if_node):
    for child in if_node.children:
        if bblfsh.role_id("CONDITION") in child.roles:
            return utils.hash_node(child).hexdigest()
    raise Exception("Could not hash node")

for if_node in if_nodes:
    condition_hashes = set()
    condition_hashes.add(hash_condition(if_node))

    for else_node in bblfsh.filter(if_node, "//*[@roleElse and @roleIf and @roleStatement]"):
        h = hash_condition(else_node)
        if h in condition_hashes:
            print("Else condition in line {} repeated".format(else_node.start_position.line))
        else:
            condition_hashes.add(h)
