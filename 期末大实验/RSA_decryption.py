import RSA_encryption
import RSA_key_generation
def RSA_decryption(c,d,p,q,n):
    d_p=d%(p-1)
    d_q=d%(q-1)
    #计算q在模p意义下的乘法逆元
    q_inv=RSA_key_generation.mod_inverse(q, p)
    #对密文分别进行模p和模q的解密计算
    m_p= RSA_encryption.fast_mod(c, d_p, p)
    m_q= RSA_encryption.fast_mod(c, d_q, q)
    #使用中国剩余定理从m_p和m_q中恢复明文
    h = (q_inv * (m_p- m_q)) % p
    plaintext = (m_p+h * q)%n
    print(f"使用中国剩余定理解密获得的明文为{plaintext}")
    return plaintext
'''
p,q,n,e,d=RSA_key_generation.key_generation()
c=RSA_encryption.RSA_encryption(n,e)
plaintext=RSA_decryption(c,d,p,q,n)'''