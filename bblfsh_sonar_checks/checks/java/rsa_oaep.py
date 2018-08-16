# check: https://rules.sonarsource.c../../java/RSPEC-2277
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/rsa_oaep.java").uast
crypt_calls = bblfsh.filter(uast, "//MethodInvocation/String[@internalRole='arguments'"
        " and @Value='RSA/NONE/NoPadding']/parent::MethodInvocation/"
        "Identifier[@roleCall and @roleReceiver and @Name='Cipher']/parent::MethodInvocation/"
        "Identifier[@roleCall and @roleCallee and @Name='getInstance']/parent::MethodInvocation")

for c in crypt_calls:
    print("Don't use 'RSA/NONE/NoPadding,' use 'RSA/ECB/OAEPWITHSHA-256ANDMGF1PADDING' instead"
          " (line {})".format(c.start_position.line))
