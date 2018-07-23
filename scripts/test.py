#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rsa, sys, base64

privkey = '''
-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCs/K7jMZgZDDIqqa5yQy+aC6MoQdAPZW03Bm8u7xrFCtZIOAi/7ncbjPwj8sUQXrdPtdHwVmu+7TTwbFsSAPsyOYM3nD5LpIWQeq8woDO5GDYTffKuXs0wmZhnDjZIcaAaxcXFgWOOWJsb+i9iylBN6trZOQcOYvKIO3jYz0C/wQIDAQABAoGAVPQPC0Ja2Mo1hOAp7LF0Ginm6alQfY8pEKHXTmxccDI/Q95I5cE9u0kEtr7N6pkpWzsGrAo1BeHGYuBD5VaYBaYrFB5kBnvAm8fpFPgAFSfEr7EDzTSXLYIfKTjYEsT15WRrKLg3G0RGmqtZEs62IpIRcfpso0L68GgX8ZcWqqUCQQDhd77u/IPYf/YRaTOsdzPJU7sAtZbQ0cdEwLeFhu2ek/b+3dfRZ6nUBniO5WkAbfxjxTixYCCIp/egIJu+Xr3nAkEAxGmY0LLrXHM+uqbqrFEf1wa/Xmu9lWh32mKXhU1bPuYJhrZyCAU4CDJd7uXty7CoyBev0YxFDjzC9qNZz77QFwJAHOtVDCZLavuOvlD2Fcr8U3hv5flkrMgbfRAS+geCdvKXnb0qr2tSdyWVVQ7L1whEdS+Yw/eGdMDGnD1SfKp+RQJAXBKsYlkdYA9ePp10sSauaFxvZVHYY6u/U46YPRMQTSIFITNxrTTVGXKS+iSrHqtH09TWxMKetJfjRT86INrwLQJBAINFTZXu4qss/B8+rPzCrWdcHxhYDdtr7SqLtI/ogwuxcPuQY4aQb5W9YEkKJ3rHrNJUqoT2pwWtoHX4XUsnsZg=
-----END RSA PRIVATE KEY-----
'''

# 生成密钥
pubkey = '''-----BEGIN PUBLIC KEY-----
		MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCs/K7jMZgZDDIqqa5yQy+aC6MoQdAPZW03Bm8u7xrFCtZIOAi/7ncbjPwj8sUQXrdPtdHwVmu+7TTwbFsSAPsyOYM3nD5LpIWQeq8woDO5GDYTffKuXs0wmZhnDjZIcaAaxcXFgWOOWJsb+i9iylBN6trZOQcOYvKIO3jYz0C/wQIDAQAB
		-----END PUBLIC KEY-----'''
# 明文
message = 'Le5JOI8&(*%dsf6`fkj!@3jkl237NgInX@!#qxmmp716'

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