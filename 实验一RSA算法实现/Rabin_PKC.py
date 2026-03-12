def decrypt(c,p,q):
    #m^2=c mod p*q
    #m^2=c mod p ,m^c mod q
    m_1=c**((p-1)/4)
    m_2=p-m_1
    m_3=c**((q-1)/4)
    m_4=q-m_3
    m=chinese_remainder(p,q,m_1,m_3)
    m=chinese_remainder(p,q,m_2,m_4)


def chinses_remainder(p,q,r_1,r_2):
    q_inverse,p_inverse=exgcd(q,p)[1],exgcd(q,p)[2]
    mod_product=p*q
    m=q_inverse*q*r_1+p_inverse*p*r_2
    m=m%mod_product
    return m
    
