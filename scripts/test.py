#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rsa, sys, base64

privkey = '''
-----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQCzO/6ENl6VofRXCPjCx5KBWXQmIkma25Izttu8rZ4kfSsfs9zJlqhWBEb/Vbqc7RQk/aaaLrCkLeFeew4g6kflxd7MQORMtTEck1k5jstrn9YsAs2xuvFSSNxX5BGUM9X8NFGzkbxzkiRkgCHRaxHZFSmudKoakpp9j3XscxTBSwIDAQABAoGBAJWGjXSbLxlB/WfGslE80XpbuEw/+ovYdgXynSqw5OeoDJvsH1uF9nWcJ+bIDGDyYAXkHmMuZGrzY7rAii7nhIZEfVgn2VQV55bCtMU/nDkfuWPU0qva6kjBy/woOGYxAwcPCgwKIQttUvnY++zXG6iIws5p9ReQHSzBU3oP5TsRAkEA3nslOj5PdNhlgxzzXhwH0MhoRIHsIl5URWEac/WKVyfoZLFDvLSNwxPfv1H9YOGCS76Woz7f+BYfNhNGPS5BbQJBAM483uFVOEx5qBjv9liIsSHtlKEJ44SPt1ausHZaZTwz2a9GtaddLuNwpAMroVgqXbbx8A/O4T2urt98PHfskpcCQQDCk4cCgl5xfZSCb/50ryUytyNhzxMbF86yAvPkuLlt8kwwTExGrM5S732/UNC+O1v+LMiIK0QsMATKAV9rwJmdAkBDNhc0vD8ivSsJJXrVE4cWlYSwjrZ1BxkqyLd9eqwvWH6C3rpolrenK5hn6Bomz3fHHUWtATDqlzkqYCScuJ51AkEA12mcC8Vjjzo/9K4+YUoGSzSXaPcZxO/Ck5e7ohpPjYPVlScUYhImUiCTVsr0V0azOUaBlinC6NWcZkujuOEYGA==
-----END RSA PRIVATE KEY-----
'''

# 生成密钥
pubkey = '''
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCzO/6ENl6VofRXCPjCx5KBWXQmIkma25Izttu8rZ4kfSsfs9zJlqhWBEb/Vbqc7RQk/aaaLrCkLeFeew4g6kflxd7MQORMtTEck1k5jstrn9YsAs2xuvFSSNxX5BGUM9X8NFGzkbxzkiRkgCHRaxHZFSmudKoakpp9j3XscxTBSwIDAQAB
-----END PUBLIC KEY-----
'''
# 明文
message = '+bIDGDyYAXkHmMuZGrzY7rAi'

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