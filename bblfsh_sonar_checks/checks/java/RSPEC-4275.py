import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    cl_nodes = bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")
    classes = []
    lowered_field_names = set()

    for cl in cl_nodes:
        jc = utils.JClass(cl)

        for field in [i.name for i in jc.fields]:
            lowered_field_names.add(field.lower())

        for method in jc.methods:
            # Avoid complex getters/setters
            if len(list(method.body.children)) > 1:
                continue

            m_name = method.name.lower()

            if m_name.startswith("get"):
                should_return = m_name[3:]
                returns = bblfsh.filter(method.body, "//*[@roleReturn]//Identifier")
                for r in returns:
                    returned_var = r.properties["Name"]

                    if returned_var and returned_var.lower() != should_return.lower():
                        findings.append({"msg": "Getter '{}' probably should return '{}' instead of '{}'"
                                          .format(method.name, should_return, returned_var),
                                          "pos": r.start_position})


            elif m_name.startswith("set"):
                should_assign = m_name[3:]
                assgns = bblfsh.filter(method.body, "//Assignment//Identifier[@roleLeft]|"
                                                    "//Assignment//*[@roleLeft]//Identifier")

                for a in assgns:
                    assigned_var = a.properties["Name"]

                    if assigned_var and assigned_var.lower() != should_assign.lower():
                        findings.append({"msg": "Setter '{}' probably should assign to '{}' instead of '{}'"
                                  .format(method.name, should_assign, assigned_var),
                                  "pos": a.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
