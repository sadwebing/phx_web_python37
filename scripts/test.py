#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rsa, sys, base64

privkey = '''
-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQDOHF/idTvIic+t8yTAsIYVL3z0Sz/UmbVjHQeAT3GmqoQtlddDZe1E0Bgg09papMhrIM7K+POZp/0tFWviZs0C+9p3tK03s9o4e79NYFtnNp0LF7wMmzQmDVpWmUZprFxEc0pd2nwyGtiOD73jpi838nvG/5Uv+6FKNNVpaczv3wIDAQABAoGANc6YhZEfY1H+4qWIIbmzt1InZ8tBRao+/Tn13FxhCiaXzSLCCLlSQNWmhuNnrKQ6IiV1du2ZArMlWCCwgnFd8YJ5Xn5qEHWM6vakA/W83/pud/3a0LqiVqwlxpTGv5IjfsqjbbgbFjIo2Ql4YUK4xL3vDJEDo38uhLoqLMzGNqECQQDtKwKoomo/7EAA9wes8tlDJeQdUHi0ZGb9UQcvUodmZKPMq27RdIw4bqiL7u99L2qiuJcUUVF34+7PRGrlItNxAkEA3noOHt9DL8SbA1lQQNrj4NhMyNngGdGoMSwl2osfn3HBco/JM3uEHAj6n2x1BN0JSYqAEwDjPt2DfK99NbCwTwJBAIMxoKXiOj4kFP+zpwZPzEltw3NH2Y2IYMRON1hBIe9NSqLkTkgFXa+13vyRbt9kBGwBCmnN1fApISh8o1kfW7ECQADYY99YJ9AxpgkgOL7WVhFPoRMOSNywQDxXl5k5+BfJ/dsqkrAgYwMcQZ+DcPpgwJ1H6m6oDTT68HnzzLz8e98CQC2dY1lAijYWwe1gXDSr8dX7PpFs66lB72QRV5cpg0ku6pdt7uokl/Ymkv26gNtFCL67Nq0tDIgbLaEcxUY4Muo=
-----END RSA PRIVATE KEY-----
'''

# 生成密钥
pubkey = '''-----BEGIN PUBLIC KEY-----
		MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDOHF/idTvIic+t8yTAsIYVL3z0Sz/UmbVjHQeAT3GmqoQtlddDZe1E0Bgg09papMhrIM7K+POZp/0tFWviZs0C+9p3tK03s9o4e79NYFtnNp0LF7wMmzQmDVpWmUZprFxEc0pd2nwyGtiOD73jpi838nvG/5Uv+6FKNNVpaczv3wIDAQAB
		-----END PUBLIC KEY-----'''
# 明文
message = 'Br_DdR_bGpwDfFg8VwHe_z63HFIDh5J'

public_key = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey)
private_key = rsa.PrivateKey.load_pkcs1(privkey)

print public_key
print private_key

# 公钥加密
crypto = rsa.encrypt(message.encode(), public_key)
print len(crypto)
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