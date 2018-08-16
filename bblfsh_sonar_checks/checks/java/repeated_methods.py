# check: https://rules.sonarsource.c../../java/RSPEC-4144
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/repeated_methods.java").uast

jclasses = [utils.JClass(i) for i in bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")]

for cl in jclasses:
    hash2methods = {}

    for m in cl.methods:
        body_hash = utils.hash_node(m.body).hexdigest()

        if body_hash in hash2methods:
            print("Method {m1_name} at line {m1_line} has the same implementation as "
                  "method {m2_name} at line {m2_line}".format(
                      m1_name = hash2methods[body_hash].name,
                      m1_line = hash2methods[body_hash].node.start_position.line,
                      m2_name = m.name,
                      m2_line = m.node.start_position.line))
        else:
            hash2methods[body_hash] = m
