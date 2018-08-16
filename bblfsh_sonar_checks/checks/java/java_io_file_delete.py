# check: https://rules.sonarsource.c../../java/RSPEC-4042
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/java_io_file_delete.java").uast

for usage in utils.instanced_calls(uast, "File", "delete"):
    print("Don't call delete() on java.io.File instances, use java.nio.File.delete(), "
          "line: {}".format(usage.start_position.line))
