import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    crypt_calls = bblfsh.filter(uast, "//MethodInvocation/String[@internalRole='arguments'"
            " and @Value='DESede/ECB/PKCS5Padding']/parent::MethodInvocation/"
            "Identifier[@roleCall and @roleReceiver and @Name='Cipher']/parent::MethodInvocation/"
            "Identifier[@roleCall and @roleCallee and @Name='getInstance']/parent::MethodInvocation")

    for c in crypt_calls:
        findings.append({"msg": "Don't use DESese cypher, use 'AES/GCM/NoPadding'"})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
