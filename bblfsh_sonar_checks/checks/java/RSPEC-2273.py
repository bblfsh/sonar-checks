import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    sync_wait_notify_calls = set()

    # Search for (correct) notify/wait/notifyAll calls inside a synchronized block
    waitCallMatch = "Identifier[@Name='wait' or @Name='notify' or @Name='notifyAll' and @roleCall]"

    nodes_stmt = bblfsh.filter(uast, "//SynchronizedStatement//%s" % waitCallMatch)

    for node in nodes_stmt:
        sync_wait_notify_calls.add((node.start_position.line, node.start_position.col))

    nodes_call = bblfsh.filter(uast, "//FunctionGroup")

    # Same for synchronized methods
    for node in nodes_call:
        method = utils.Method(node)

        if "synchronized" in method.modifiers:
            waits = bblfsh.filter(method.node, "//%s" % waitCallMatch)

            for wait in waits:
                sync_wait_notify_calls.add((wait.start_position.line, wait.start_position.col))

    # Now get all and check which are not in the two above
    nodes_all = bblfsh.filter(uast, "//%s" % waitCallMatch)

    for node in nodes_all:
        if (node.start_position.line, node.start_position.col) in sync_wait_notify_calls:
            continue

        findings.append({"msg": "wait()/notify()/notifyAll() calls not inside synchronized blocks or methods",
                         "pos": node.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
