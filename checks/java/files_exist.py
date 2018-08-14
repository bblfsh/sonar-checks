# check: https://rules.sonarsource.c../../java/RSPEC-3725
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/files_exist.java").uast
calls = bblfsh.filter(uast, "//MethodInvocation/"
        "Identifier[@roleCall and @roleReceiver and @Name='Files']/parent::MethodInvocation/"
        "Identifier[@roleCall and @roleCallee and @Name='exists' or @Name='notExists'"
        "or @Name='isDirectory' or @name='isRegularFile']/parent::MethodInvocation")

for c in calls:
    print("Don't use slow Files.exist/notExists/isDirectory/isRegularFile, line: {}"
            .format(c.start_position.line))
