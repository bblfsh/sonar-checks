# check: https://rules.sonarsource.com/java/RSPEC-2446
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/transactional_private.java").uast
methods = utils.get_methods(uast)

for m in methods:
    if "public" not in m.modifiers:
        ann_trans = bblfsh.filter(m.node, "//*[@roleAnnotation]/Identifier[@Name='Transactional']")
        for ann in ann_trans:
            print("@Transactional methods should be public, line: {}"
                    .format(ann.start_position.line))
