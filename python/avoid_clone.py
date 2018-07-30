import utils

import bblfsh

if __name__ == '__main__':
    client = bblfsh.BblfshClient("0.0.0.0:9432")
    uast = client.parse("../java/avoid_clone.java").uast

    if any(filter(lambda m: m.name == "clone" and "public" in m.modifiers and
        m.return_.type_name == "Object", utils.get_methods(uast))):

        print("Don't use clone")
