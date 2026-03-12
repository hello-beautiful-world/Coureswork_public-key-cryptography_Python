import RSA_encryption
import RSA_encryption
import math
def RSA_low_encryption_exponent_attack(c,e,n):
    #快速模幂运算
    c_e=RSA_encryption.fast_mod(c,e,n)
    if c_e < n:
        return math.floor(math.pow(c_e, 1 / e))
    else:
        # 如果 c^e > n，尝试对 k 进行爆破
        for k in range(1, n // e + 1):
            t = (k * n + c) % e
            if t == 0:
                return (k * n + c) // e
    return None



c = 65537  # 密文
e= 3  # 公钥的加密指数
n= 1594323  # 模数


m2= RSA_low_encryption_exponent_attack(c, e, n)
if m2 is not None:
    print("解密成功,获得明文:", m2)
else:
    print("解密失败")

