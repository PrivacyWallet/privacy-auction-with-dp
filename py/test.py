import base64
import Crypto.PublicKey.RSA
import Crypto.Cipher.PKCS1_v1_5
import Crypto.Random
import Crypto.Signature.PKCS1_v1_5
import Crypto.Hash
from time import time
data="blnwLEkVs9wTvn8+ufs7W4jS2zmR0xu9HqURXDU8bLVfZs3U8HJaABiu8N4gBgdGvq3qeczcuG2ICJEWL/PlO4hUq0kslYFhdUYKR5Gfxgkh9qX18WQ5aezt4yg4auDenH6DT6QSMmcNWDp2KJX81PbPIwja/y4cIbqx6OH5DQ+iajUwfW27FXRPeDIZkMEYeZCuHNbUoVUbLJKKra2yijZaG96asJCngDkgyaSgOlBEdBL6fd9QNDXOxbytoqqfyJI/sKgjojrOCoP2AvJKAi3P52jeSxt2fiyd1HiATofW0/KDCMM1d7F6Xmih/0C+pEDC87LTJ6XPP6j8gC6dOQ=="
encrypted_data=base64.b64decode(data)
# print(data)
with open("priv_mid.pem", "rb") as x:
    a = x.read()
    for i in range(10):
        start = time()
        for i in range(500):
            cipher_private = Crypto.Cipher.PKCS1_v1_5.new(Crypto.PublicKey.RSA.importKey(a))
            data = cipher_private.decrypt(encrypted_data, Crypto.Random.new().read)
            data = data.decode('utf-8')
            # print(data) 
        end = time()
        print(end-start)


