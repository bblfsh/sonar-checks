import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    cl_nodes = bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")

    getters = {}
    setters = {}
    classes = []

    def add_dict(dict_, key, value):
        if key in dict_:
            dict_[key].append(value)
        else:
            dict_[key] = [value]


    for cl in cl_nodes:
        jc = utils.JClass(cl)

        for method in jc.methods:
            if 'public' in method.modifiers:
                if len(method.name) > 0:
                    if method.name.startswith("get"):
                        getters[method.name[3:]] = method
                    elif method.name.startswith("set"):
                        setters[method.name[3:]] = method

        for property_, getter in getters.items():
            try:
                setter = setters[property_]
            except KeyError:
                continue

            sync = 'synchronized'
            if sync in getter.modifiers and sync not in setter.modifiers or\
                    sync in setter.modifiers and sync not in getter.modifiers:
                findings.append({"msg": "Getter and setter for '%s' should both or none be synchronized" % property_})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
