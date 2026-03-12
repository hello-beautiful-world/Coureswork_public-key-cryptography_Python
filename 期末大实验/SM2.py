import hashlib
import random
from math import log

def generatePrivateKey(n) :
    # 1 <= d_B <= n-1
    random.seed(256)
    return random.randint(1, n - 1)

def ExEuclid(f, d) : #扩展的欧几里得 求 d 模 p 的逆元
    x1 = 1
    x2 = 0
    x3 = f
    y1 = 0
    y2 = 1
    y3 = d
    while 1 :
        if y3 == 0 :
            return -1
        elif y3 == 1 :
            while y2 < 0 :
                y2 = y2 + f
            return y2
        q = x3 // y3
        t1 = x1 - q * y1
        t2 = x2 - q * y2
        t3 = x3 - q * y3
        x1 = y1
        x2 = y2
        x3 = y3
        y1 = t1
        y2 = t2
        y3 = t3
          
def addPoint(a, p, point1, point2) :
    if not point1 :
        return point2
    if not point2 :
        return point1
    
    if point1[0] == point2[0] and (point1[1] + point2[1]) % p == 0:
        return None
    
    if point1[0] == point2[0] : # P=Q aka (x1, y1) == (x2, y2)
        L = (3 * point1[0]**2 + a) * ExEuclid(p, 2 * point1[1]) % p
    else : # P!=Q
        L = (point2[1] - point1[1]) * ExEuclid(p,(point2[0] - point1[0]) % p) % p
        
    x3 = (L**2 - point1[0] -point2[0]) % p
    return [x3,(L * (point1[0] - x3) - point1[1]) % p]

def fastScalarMultiplication(a, p, n0, point) :
    if n0 < 0 :
        print('n不合法')
        return None
    elif n0 == 0 :
        return None
    elif n0 == 1 :
        return point
    else :
        n = n0
        point1 = point
        point2 = None
        while n > 0 :
            if n % 2 == 1 :
                point2 = addPoint(a, p, point2, point1)
            point1 = addPoint(a, p, point1, point1)
            n = n // 2
        return point2 
    
def generatePublicKey(a, p, h, d_B, G) :
    #P_B = d_B 倍点 G
    P_B = fastScalarMultiplication(a, p, d_B, G)

    if not fastScalarMultiplication(a, p, h, P_B) :
        print('运行错误！')
        return None
    else :
        return P_B

def deriveKey(initialKey, klen) : #返回字节串
    
    if klen % 64 :
        j = (klen // 64) + 1
    else :
        j = klen // 64
        
    Ct = 0x00000001
    H = bytes()
    for i in range(1,j + 1) :
        H_str_i = hashlib.sha512(initialKey + Ct.to_bytes(4, "big")).hexdigest()
        H_bytes_i = int(H_str_i,16).to_bytes(64, "big")
        H = H + H_bytes_i
        Ct += 1
    
    if klen % 64 :
        K = H[0:-(64 - (klen % 64))]
    else :
        K = H
    return K
    
def encipher(p, a, G, n, h, Seed, M, P_B) : #M为字节串
    #单坐标转换成字节串的长度 l
    if log(p, 2) % 8 :
        l = (log(p, 2) // 8) + 1
    else :
        l = log(p, 2) // 8
    l = int(l)
    
    #C1
    random.seed(Seed)
    while True :
        k = random.randint(1, n - 1)
        C1_point = fastScalarMultiplication(a, p, k, G)
        C1 = b'\x04' + int(C1_point[0]).to_bytes(l, "big") + int(C1_point[1]).to_bytes(l, "big") #C1_bytes
    
    
    #C2
        [x2, y2] = fastScalarMultiplication(a, p, k, P_B)
        x2_y2 = int(x2).to_bytes(l, "big") + int(y2).to_bytes(l, "big")
        klen = len(M) #密钥的字节长度klen
        t_bytes = deriveKey(x2_y2, klen)
        t_int = int.from_bytes(t_bytes, byteorder='big', signed=True)
        if t_int :
            break
    print('\n加密选择的随机数k:', k)
    M_int = int.from_bytes(M, byteorder='big', signed=True)
    if len(M) == len(t_bytes) :
        C2_int = M_int ^ t_int
        C2 = C2_int.to_bytes(klen, "big") #C2_bytes
    else:
        print("test0000000000000000000000000000000000")
    
    
    #C3
    x2_M_y2 = int(x2).to_bytes(l, "big") + M + int(y2).to_bytes(l, "big")
    C3_str = hashlib.sha512(x2_M_y2).hexdigest()
    C3 = int(C3_str,16).to_bytes(64, "big") #C3_bytes
    
    return C1 + C2 + C3

def decipher(p, a, C, Mlen, d_B) : #简单起见，省略其中检错退出的步骤
    # C =     C1 ||     C2 || C3
    #长度：2*l+1 || len(M) || 64
    
    if log(p, 2) % 8 :
        l = (log(p, 2) // 8) + 1
    else :
        l = log(p, 2) // 8
    l = int(l)
    
    C1 = C[0:2*l + 1]
    C1_x = int.from_bytes(C1[1:l + 1], byteorder='big', signed=False)       #经检查,C1_x错误！！！
    while C1_x < 0 :
        C1_x += p
    C1_y = int.from_bytes(C1[l + 1:], byteorder='big', signed=False)
    while C1_y < 0 :
        C1_y += p
    C1_point = [C1_x,C1_y]
    
    [x2, y2] = fastScalarMultiplication(a, p, d_B, C1_point)
    x2_y2 = int(x2).to_bytes(l, "big") + int(y2).to_bytes(l, "big")
    t_bytes = deriveKey(x2_y2, Mlen)
    t_int = int.from_bytes(t_bytes, byteorder='big', signed=False)
    
    C2 = C[2*l + 1:2*l + 1 + Mlen]
    C2_int = int.from_bytes(C2, byteorder='big', signed=False)
    
    M = C2_int ^ t_int
    return M
    
def main(Seed) :
    p = 0xfffffffeffffffffffffffffffffffffffffffff00000000ffffffffffffffff
    a = 0xfffffffeffffffffffffffffffffffffffffffff00000000fffffffffffffffc
    #b = 0x28e9fa9e9d9f5e344d5a9e4bcf6509a7f39789f515ab8f92ddbcbd414d940e93
    n = 0xfffffffeffffffffffffffffffffffff7203df6b21c6052b53bbf40939d54123
    G_x = 0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7
    G_y = 0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0
    h = 1

    M_text = "maxinyue" #字符串
    M = M_text.encode('utf-8')
    print('明文：\n', M)
    print(type(M))
    d_B = generatePrivateKey(n)
    P_B = generatePublicKey(a, p, h, d_B, [G_x, G_y])
    print('\nd_B     ', d_B, '\nP_B     ', P_B)
    C = encipher(p, a, [G_x, G_y], n, h, Seed, M, P_B)
    print('\n加密得：', C)
    
    m_int = decipher(p, a, C, len(M), d_B)
    len_m = m_int.bit_length() // 8 + 1
    m_bytes = m_int.to_bytes(len_m, "big")
    m = m_bytes.decode('utf-8', errors='ignore')
    print('\n再解密得：', m)
    return
    
Seed = 50
main(Seed)