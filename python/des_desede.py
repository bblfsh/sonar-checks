import utils

import bblfsh

if __name__ == '__main__':
    client = bblfsh.BblfshClient("0.0.0.0:9432")

    uast = client.parse("../java/des_desede.java").uast
    crypt_calls = bblfsh.filter(uast, "//MethodInvocation/String[@internalRole='arguments'"
            " and @Value='DESede/ECB/PKCS5Padding']/parent::MethodInvocation/"
            "Identifier[@roleCall and @roleReceiver and @Name='Cipher']/parent::MethodInvocation/"
            "Identifier[@roleCall and @roleCallee and @Name='getInstance']/parent::MethodInvocation")

    for c in crypt_calls:
        print("Don't use DESese cypher, use 'AES/GCM/NoPadding'")
