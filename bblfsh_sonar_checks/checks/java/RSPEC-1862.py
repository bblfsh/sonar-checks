import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    if_nodes = bblfsh.filter(uast, "//*[@roleIf and @roleStatement and not(@roleElse)]")

    def hash_condition(if_node):
        for child in if_node.children:
            if bblfsh.role_id("CONDITION") in child.roles:
                return utils.hash_node(child).hexdigest()

        return None

    for if_node in if_nodes:
        condition_hashes = set()
        cond_hash = hash_condition(if_node)

        if not cond_hash:
            continue

        condition_hashes.add(cond_hash)

        for else_node in bblfsh.filter(if_node, "//*[@roleElse and @roleIf and @roleStatement]"):
            h = hash_condition(else_node)
            if h in condition_hashes:
                findings.append({"msg": "Else condition repeated",
                                 "pos": else_node.start_position})
            else:
                condition_hashes.add(h)

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
