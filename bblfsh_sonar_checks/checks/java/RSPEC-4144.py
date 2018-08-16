import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    jclasses = [utils.JClass(i) for i in bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")]

    for cl in jclasses:
        hash2methods = {}

        for m in cl.methods:
            body_hash = utils.hash_node(m.body).hexdigest()

            if body_hash in hash2methods:
                findings.append({"msg": "Method {m1_name} has the same implementation as method {m2_name}".format(
                              m1_name = hash2methods[body_hash].name,
                              m2_name = m.name),
                          "pos": hash2methods[body_hash].node.start_position})
            else:
                hash2methods[body_hash] = m

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
