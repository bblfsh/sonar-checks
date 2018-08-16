# check: https://rules.sonarsource.c../../java/RSPEC-3046

import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/multilocks_wait.java").uast

cl_nodes = bblfsh.filter(uast, "//SynchronizedStatement//SynchronizedStatement//"
                               "MethodInvocation//Identifier[@Name='wait']")

for node in cl_nodes:
    print("Don't call wait with more than one concurrent lock held, line {}".format(
          node.start_position.line))
