#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rsa, sys, base64

privkey = '''
-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCfTF/IdsIzqZLciDkpBPI4d2PAP5CXYWyAtWn5CIjRLc7t/7xs+cbpJ25bDISRedsnvqSZViSIcCP3DFcRFgwD8yPJ8RvOAMpPlg+bYDDne2ysx1i7SU0h5G/y1lX5abtAgA7V5jYkJnkFcXF0yBzw2G3aUxGrwxWp8YxuBJRXOwIDAQABAoGAb9C6QwopUv4qmiX8iXBxXXVgTWfQ5JF8CfRNSILXFo1i/OhPqObC2pHVApAM1diFHqbQ/tjal/KvLBA7ZUDmeRvAxLRLc59fiaaoIXyD91UyorhaDtdMb7FbAHCijtjeXJOle5rb4kfBlx7mXPUNWSFjssoCpp8isFypGBGq/MECQQDM1HnfX87N6CwB47P8f/JmqZct7NkoN930zyb6p+PDo/PGoHll4T5/08+lMqRAasC0K1RQV3j0PbwyemK8sGHxAkEAxxgBaHJqz0ZkUhVDxooUzl2DTT5jeVYi50yOC13GEqVVBB+1y4RtP8h3Bxp54CIIK31d1Ulv+ri5Hc/IjXJf6wJBAJ7nvADSWCMgGnwAxhJ+xHRm3zUuyS3NYbFZwDi3ZRjTKf0PY/7o5s7OaQoVJp4e848TCl8l7V02Q7m5fr457FECQF3TNU6opSdbcAmy1cbp6dY7AZbUcQKMklRYopQ+tAqzebZAz2bC2M13RojFdGwo/ZqpMSBDxI7uoOaotkXagdMCQEK4I0IzVEcYWtfp3+9DYFXhZhH4sVxXN/5E2iBhA6A5IY5PXJmTg/TU3HEdnQ4+A3dMthOnIxg93fyPIBwLP+w=
-----END RSA PRIVATE KEY-----
'''

# 生成密钥
pubkey = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCfTF/IdsIzqZLciDkpBPI4d2PAP5CXYWyAtWn5CIjRLc7t/7xs+cbpJ25bDISRedsnvqSZViSIcCP3DFcRFgwD8yPJ8RvOAMpPlg+bYDDne2ysx1i7SU0h5G/y1lX5abtAgA7V5jYkJnkFcXF0yBzw2G3aUxGrwxWp8YxuBJRXOwIDAQAB
-----END PUBLIC KEY-----'''
# 明文
message = 'Le5JOI8&(*%dtestfkj!@3jkl237jihakdflakdfjk'

public_key = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey)
private_key = rsa.PrivateKey.load_pkcs1(privkey)


# 公钥加密
crypto = rsa.encrypt(message.encode(), public_key)

#a = base64.encodestring(crypto)
#b = base64.encodestring(a)
print base64.encodestring(crypto)

# 私钥解密
message = rsa.decrypt(crypto, private_key).decode()
print(message)

sys.exit()

# 私钥签名
signature = rsa.sign(message.encode(), privkey, 'SHA-1')
print signature
# 公钥验证
rsa.verify(message.encode(), signature, pubkey)