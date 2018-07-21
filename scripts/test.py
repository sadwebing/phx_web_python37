#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rsa, sys
# 生成密钥
pubkey, privkey = rsa.newkeys(64)

print pubkey
print privkey
sys.exit()

# 明文
message = 'hello'
# 公钥加密
crypto = rsa.encrypt(message.encode(), pubkey)
# 私钥解密
message = rsa.decrypt(crypto, privkey).decode()
print(message)
# 私钥签名
signature = rsa.sign(message.encode(), privkey, 'SHA-1')
print signature
# 公钥验证
rsa.verify(message.encode(), signature, pubkey)