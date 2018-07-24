#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rsa, sys, base64

privkey = '''
-----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQC2dqZVOoy8FSSkz9q/uCE4171KsKTS2Sm1i5AsOZXXJOe6NfsS1cNtnEQt1bLsRy/4FK1s2U4gTkZnk7Lum1S6RX6yaGTalNJTFSAFHT69ksD9DvcnTlX/0ExE4qRGosJ3ABNkOEHVfecfWHKbVdV7XUM4DNOiyOe9gGVyp1y7vwIDAQABAoGAQd6lf4Eqiz+qweDTnICxZZ7klBEe/4ssNoDSpFSJlmiZSyzvncYTzf8q0c0i0Y+Fbq6wSOpN/PWlDwFQCDmFJTi4ISWYC6CnbGLtwn2em1pCozLh/mfRuXwr9DNzrCs5T1CDfRd3X3E1Kc6A+PjGmlBboJ6kQfC6aJ+wNZ1pqKECQQDw5CQuB6UYGDAav12Fs8EOz25nMWxN3we6DTPzfVK5x5A1I6QNh1DjrTaa19I1kAs0HH/KERnQgSSp6TQOqSxPAkEAwehd15UgW7Physbp7YKOvmrLgPJZyFD0Jj63QtarYcuqJXDHBwx2P5D4UJdnj6k+nVHcaKpE9ta/KaRXd0NtkQJBAJfrGVIaKikm3/eOZjmy4ncnpHXZ+nalyGayeuf9SlW1oKGSp5yMkRv1GjHPGFgFTrt/mavi2wfe2jN5ygXQ9QsCQQC8rfgyP79eu+gnQep526I+Evi2HhvS2ULYvAnilbPp0x1alSR07WFadRvKf6ibl5l/xxnrFlNIxKj6QhmByTChAkEArZ5ah6gGMRvRASr8yYdCndYxATaECaPO6LgbJWImf+Tz8mDVzTq74d0I0r2wjXFmiOt4hgp1GSjYzOU61YD8WQ==
-----END RSA PRIVATE KEY-----
'''

# 生成密钥
pubkey = '''-----BEGIN PUBLIC KEY-----
		MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC2dqZVOoy8FSSkz9q/uCE4171KsKTS2Sm1i5AsOZXXJOe6NfsS1cNtnEQt1bLsRy/4FK1s2U4gTkZnk7Lum1S6RX6yaGTalNJTFSAFHT69ksD9DvcnTlX/0ExE4qRGosJ3ABNkOEHVfecfWHKbVdV7XUM4DNOiyOe9gGVyp1y7vwIDAQAB
		-----END PUBLIC KEY-----'''
# 明文
message = 'dLLAeY1T8xo5fboUV9dDoMKD$JWM5P@Y018'

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