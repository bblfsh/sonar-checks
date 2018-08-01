# check: https://rules.sonarsource.com/java/RSPEC-2387
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/field_shadow.java").uast
classes = []
name2class = {}

cl_nodes = bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")

for cl in cl_nodes:
    jc = utils.JClass(cl)
    name2class[jc.name] = jc

for clname, cl in name2class.items():
    if not cl.parent:
        continue

    parent = name2class[cl.parent]

    common = set([i.name for i in cl.fields]) & set([i.name for i in parent.fields])
    if len(common):
        print('Class {} uses field(s) with same name as parent {}: {}'.format(
            cl.name, parent.name, common))
