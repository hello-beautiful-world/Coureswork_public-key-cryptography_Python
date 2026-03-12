import RSA_encryption
import RSA_key_generation
import random

'''
函数名：RSA_common_mode_attack(n,e1,e2,c1,c2)
功能：RSA的共模攻击
参数传递：n_共享的模数，e1_公钥1,e2_公钥2,c1_e1加密相同明文所得密文,c2_e2所得密文
返回值：攻击获得的明文
'''
def RSA_common_mode_attack(n,e1,e2,c1,c2,p,q):
    #扩展欧几里得计算系数s1、s2，使得e1 * s1 + e2 * s2 = 1
    gcd,s1, s2 = RSA_key_generation.extended_gcd(e1,e2)
    if s1 < 0:
        s1 = s1+(p-1)*(q-1)
    if s2 < 0:
        s2 = s2+(p-1)*(q-1)
    m = (pow(c1, s1, n) * pow(c2, s2, n)) % n
    return m   
'''
函数名：key_generation2(p,q,n,e1)
功能：求满足共模攻击的密钥
参数传递：n_共享的模数,e1_已知的公钥
返回值：e2_满足要求的公钥（gcd(e1,e2)=1），d2_e2对应私钥
'''
def key_generation2(p,q,n,e1):
   # 计算 φ(n) = (p-1) * (q-1)
    euler=(p-1)*(q-1)
    #生成公钥e
    e2=random.randint(2,euler-1)
    while  RSA_key_generation.gcd(e2, euler)!=1 or RSA_key_generation.gcd(e2,e1)!=1:
        e2=random.randint(2,euler-1)
        
    print(f"公钥e2={e2} ")
    #计算私钥d,使得 (d * e) % φ(n) = 1
    d2= RSA_key_generation.mod_inverse(e2,euler)
    print(f"私钥d2={d2}")
    return e2,d2

p,q,n,e1,d1=RSA_key_generation.key_generation()
e2,d2=key_generation2(p,q,n,e1)
c1=RSA_encryption.RSA_encryption(n,e1)
print(f"使用公钥e1加密获得的密文为c1={c1}")
c2=RSA_encryption.RSA_encryption(n,e2)
print(f"使用公钥e2加密获得的密文为c2={c2}")
m=RSA_common_mode_attack(n,e1,e2,c1,c2,p,q)
print(f"共模攻击获得的明文为{m}")
