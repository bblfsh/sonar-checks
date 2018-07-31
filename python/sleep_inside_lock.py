# check: https://rules.sonarsource.com/java/RSPEC-2276
import utils

import bblfsh

if __name__ == '__main__':
    client = bblfsh.BblfshClient("0.0.0.0:9432")

    uast = client.parse("../java/sleep_inside_lock.java").uast

    cl_nodes = bblfsh.filter(uast, "//SynchronizedStatement//"
                                   "MethodInvocation/Identifier[@Name='sleep' and @roleCallee]/"
                                   "parent::MethodInvocation/Identifier[@Name='Thread' and @roleReceiver]")

    for node in cl_nodes:
        print("Don't call Thread.sleep() inside synchonized blocks, use wait instead".format(
              node.start_position.line))
