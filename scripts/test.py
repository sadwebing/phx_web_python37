#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rsa, sys, base64

privkey = '''
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCn0LalvH8ds3htfP7p7JOtXuF4tFIGLWjq8+EocNTnvyQBNy0Aw9MMLz/wv83u7vGEaGS+WmAckjYQ/Q9X4ZclAWk98FDpRFp8TvCnWNkQ0v3SAfachdA8yM7ZQBzQqfPTqAjatrkY3yv4/JQ5rHo8jmT625wbjFs6m/PIGfOYpQIDAQABAoGBAKbdhCA81HEmGeNU3Oyhjx5fL/ej5cO6t46YvhRGTY26pASJZrhR/7Mn8H5lWlHxSjoMy8/zcYo3YId3+h+6c1x+IBnzDaHT5xXt6MBLTVO3CMbIaMkOs5tle/ZxLUcHjMY/CdkWciKedTjU63ogKpyQgtfu11ISCoLCzGctzGWpAkEA1nqGTchaLw1K8ePd/vQYefY1gHAbJrIThwBXYYRUof5eqUj8nRb8qFQOHZfLUrB15A7dNSxeHzYQw/h6qzryCwJBAMhNkqfux/HzL3FHV8eyC7quQYrecP/3+fhfAsvLl7EcIReryvWs6sTJOlm3gbAXxqs3+6eeMafFUIKOrHPafg8CQFzNVTFwwHzdbpEtfI/lhHW5L7ssRsM+iC6A2k5KmOgjDUiIWS2LlbUr8ZOia4qS6d/NArAQS4WLukNhT4qpjbMCQA0NuSQGlLM45Pud6aOS/96voofZTUXxNDIyhu0fHIinS6TORlDSbw5aCtpz8hi2w/S+lkDrN1M2sbOAds6qC5MCQQCOa3hKJ6u8EPi/KGav7E5iM63CWaaYQadhRNSZBZlyCdNOYQeuH0oDwAu/O2sVnpQmVWLhO0xkGm/vL7lZgyKA
-----END RSA PRIVATE KEY-----
'''

# 生成密钥
pubkey = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCn0LalvH8ds3htfP7p7JOtXuF4tFIGLWjq8+EocNTnvyQBNy0Aw9MMLz/wv83u7vGEaGS+WmAckjYQ/Q9X4ZclAWk98FDpRFp8TvCnWNkQ0v3SAfachdA8yM7ZQBzQqfPTqAjatrkY3yv4/JQ5rHo8jmT625wbjFs6m/PIGfOYpQIDAQAB
-----END PUBLIC KEY-----'''
# 明文
message = 'Le5JOI8&(*%dsf68fkj!@3jkl3284JHKj016'

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