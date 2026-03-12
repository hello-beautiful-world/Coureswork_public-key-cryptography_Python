import hashlib
from math import ceil,gcd,log
import random
p=0xfffffffeffffffffffffffffffffffffffffffff00000000ffffffffffffffff
a=0xfffffffeffffffffffffffffffffffffffffffff00000000fffffffffffffffc
b=0x28e9fa9e9d9f5e344d5a9e4bcf6509a7f39789f515ab8f92ddbcbd414d940e93
n=0xfffffffeffffffffffffffffffffffff7203df6b21c6052b53bbf40939d54123
G_x=0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7
G_y=0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0
G=(G_x,G_y)
h=1
'''
函数名：inverse
功能：返回M模m的逆
传递参数：M-int类型 m--int类型-模数
'''
def inverse(M, m):
    if gcd(M, m) != 1:
        return None
    u1, u2, u3 = 1, 0, M
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m
'''
函数名：frac_to_int
功能：输入 up/down mod m, 返回该分式在模m意义下的整数
传递参数：up-int类型 down--int类型-模数 m--int类型-模数
'''
def frac_to_int(up, down, m):
    num = gcd(up, down)
    up //= num
    down //= num         # 分子分母约分
    return up * inverse(down, m) % m
'''
函数名：add_point
功能：椭圆曲线上的点加运算
传递参数：P-元组类型 Q-元组类型 m--int类型-模数
'''
def add_point(P, Q, m):
    if P == 0:
        return Q
    if Q == 0:
        return P
    x1, y1, x2, y2 = P[0], P[1], Q[0], Q[1]
    e = frac_to_int(y2 - y1, x2 - x1, m)        # e是λ     
    x3 = (e*e - x1 - x2) % m           # 注意此处也要取模
    y3 = (e * (x1 - x3) - y1) % m
    ans = (x3, y3)
    return ans
'''
函数名：double_point
功能：二倍点算法
传递参数：P-元组类型 a-int类型-椭圆曲线参数a m--int类型-模数
返回值：P的二倍点
'''
def double_point(P, m, a):
    if P == 0:
        return P
    x1, y1 = P[0], P[1]
    e = frac_to_int(3 * x1 * x1 + a, 2 * y1, m)         # e是λ
    x3 = (e * e - 2 * x1) % m         # 取模！！！！！
    y3 = (e * (x1 - x3) - y1) % m
    Q = (x3, y3)
    return Q

'''
函数名：mult_point
功能：多倍点算法
传递参数：P-元组类型 a-int类型-椭圆曲线参数a m--int类型-模数 k-int类型-倍数
返回值：P的二倍点
'''
def mult_point(P, k, m, a):
    s = bin(k)[2:]          # s是k的二进制串形式
    Q = 0
    for i in s:
        Q = double_point(Q, m, a)
        if i == '1':
            Q = add_point(P, Q, m)
    return Q
'''
函数名：bits_to_bytes
功能：二进制字符串转换为bytes类型
传递参数：s-str型-二进制串
返回值：M-bytes类型
'''
def bits_to_bytes(s):           
    k = ceil(len(s)/8)          
    s = s.rjust(k*8, '0') # 左填充至长度为8的倍数
    M = b''         # M存储要返回的字节串
    for i in range(k):
        M = M + bytes([eval('0b' + s[i*8: i*8+8])])
    return M
# 字节串到比特串的转换。接收长度为k的字节串M，返回长度为m的比特串s，其中m = 8k。字节串逐位处理即可。
def bytes_to_bits(M):           # 整体思路是把每个字节变为8位比特串，用列表存储，最后连接起来
    s_list = []
    for i in M:
        s_list.append(bin(i)[2:].rjust(8, '0'))         # 每次循环存储1个字节。左填充补0
    s = ''.join(s_list)
    return s

'''
函数名：hex_to_bits
功能：十六进制字符串转换为比特串
传递参数：h-str型-十六进制串
返回值：m-str类型
'''
def hex_to_bits(h):
    m_list = []
    for i in h:
        m = bin(eval('0x' + i))[2:].rjust(4, '0')           
        m_list.append(m)
    m = ''.join(m_list)
    return m

# 字节串到十六进制串
def bytes_to_hex(m):
    h_list = []         # h_list存储十六进制串中的每一部分
    for i in m:
        e = hex(i)[2:].rjust(2, '0')            # 不能把0丢掉
        h_list.append(e)
    h = ''.join(h_list)
    return h


# 比特串到十六进制
def bits_to_hex(s):
    s_bytes = bits_to_bytes(s)
    s_hex = bytes_to_hex(s_bytes)
    return s_hex

# 十六进制到字节串
def hex_to_bytes(h):
    h_bits = hex_to_bits(h)
    h_bytes = bits_to_bytes(h_bits)
    return h_bytes
# 域元素到十六进制串
def fielde_to_hex(e):
    h_bytes = fielde_to_bytes(e)
    h = bytes_to_hex(h_bytes)
    return h
'''
函数名：int_to_bits
功能：整数（可以是各种进制）转比特串
传递参数：x-int型
返回值：x_bits-str类型-整数的比特串形式
'''
def int_to_bits(x):
    x_bits = bin(x)[2:]#去掉0b，只保留比特串
    k = ceil(len(x_bits)/8)         # 8位1组，k是组数
    x_bits = x_bits.rjust(k*8, '0')#使用rjust右对齐，用0填充
    return x_bits

'''
函数名：keyDerivation
功能：SM2密钥派生
传递参数：Z-比特串 klen--int类型-密钥长度
'''
def keyDerivation(Z, klen):
    v=512
    if klen >= (pow(2, 32) - 1) * v:#密钥长度要小于(2**32-1)*v
        raise Exception("密钥长度klen有误！")
    Ct = 0x00000001
    j=ceil(klen/v)#SHA512的杂凑长度为512比特
    H = []
    for i in range(j):    
        s = Z + int_to_bits(Ct).rjust(32, '0') # s存储 Z || Ct 的比特串形式 # 注意:Ct要填充为32位
        s_bytes = bits_to_bytes(s)          # s_bytes存储字节串形式
        hash_object=hashlib.sha512()
        hash_object.update(s_bytes)
        hash_hex=hash_object.hexdigest()
        hash_bin = hex_to_bits(hash_hex)
        H.append(hash_bin)
        Ct += 1
    if klen % v != 0:
        H[-1] = H[-1][:klen - v*(klen//v)]
    k = ''.join(H)
    return k
'''
函数名：generate_key
功能：密钥生成
返回值：Pb-元组-公钥
'''
def  generate_key():
    d=random.randint(1,n-1)
    print(f"d={d}")
    Pb=mult_point(G,d,int(p), int(a))
    print(Pb)
    return Pb
'''
函数名：int_to_bytes
功能：整数到字节串的转换
传递参数：x-int  k-int类型-字节串的目标长度-k满足2^8k > x
返回值：M-长为k的字节串
'''
def int_to_bytes(x, k):        
    if pow(256, k) <= x:
        raise Exception("无法实现整数到字节串的转换，目标字节串长度过短！")
    s = hex(x)[2:].rjust(k*2, '0')          
    M = b''
    for i in range(k):
        M = M + bytes([eval('0x' + s[i*2:i*2+2])])
    return M

'''
函数名：fielde_to_bytes
功能：域元素到字节串的转换
传递参数：e-域元素
返回值：字节串

函数名：fielde_to_bytes
功能：域元素到字节串的转换
传递参数：e-域元素
返回值：字节串
'''
def fielde_to_bytes(e):
    t = ceil(log(p, 2))#计算坐标的字节串长度
    L= ceil(t / 8)
    return int_to_bytes(e,L)

# 域元素到比特串
def fielde_to_bits(m):
    m_bytes = fielde_to_bytes(m)
    m_bits = bytes_to_bits(m_bytes)
    return m_bits

'''
函数名：point_to_bytes
功能：点到字节串的转换
传递参数：P-元组-椭圆曲线上的点
返回值：S-字节串-选用未压缩表示形式
'''
def point_to_bytes(P):
    xp, yp = P[0], P[1]
    x = fielde_to_bytes(xp)
    y = fielde_to_bytes(yp)
    PC = bytes([0x04])
    s = PC + x + y
    return s
# 点到比特串
def point_to_bits(P):
    p_bytes = point_to_bytes(P)
    p_bits = bytes_to_bits(p_bytes)
    return p_bits
'''
函数名：encry_sm2
功能：SM2加密算法
传递参数：Pb-B的公钥，M-十六进制串-明文
返回值：C_hex-十六进制串-密文
'''
def encry_sm2(Pb, M):
    plaintext = bytes.fromhex(M)
    k = random.randint(1,n-1)
    k_hex = hex(k)[2:]          
    print("生成的随机数k是：", k_hex)
    C1 = mult_point(G, k, p, a)
    print("椭圆曲线点C1=[k]G=(x1,y1)的坐标是:", tuple(map(hex, C1)))
    C1_bits = point_to_bits(C1)
    print("C1的比特串形式是:", C1_bits)
    S = mult_point(Pb, h, p, a)
    if S == 0:
        raise Exception("S是无穷远点,有误！！！")
    print("S = [h]Pb=", tuple(map(hex, S)))
    x2, y2 = mult_point(Pb,k,p,a)
    print("[k]PB=(x2,y2)=", tuple(map(hex, (x2, y2))))
    x2_bits = fielde_to_bits(x2)
    print("x2的比特串形式是：", x2_bits)
    y2_bits = fielde_to_bits(y2)
    print("y2的比特串形式是：", y2_bits)
    M_hex = bytes_to_hex(plaintext)
    klen = 4 * len(M_hex)
    print("明文消息的比特串长度klen是：", klen)
    t = keyDerivation(x2_bits + y2_bits, klen)
    print("密钥派生所得t=", t)
    if eval('0b' + t) == 0:
        raise Exception("k选取有误！")
    t_hex = bits_to_hex(t)
    print("t的十六进制表示形式是：", t_hex)
    C2 = eval('0x' + M_hex + '^' + '0b' + t)#M异或t
    print("C2=", hex(C2)[2:])
    x2_bytes = bits_to_bytes(x2_bits)
    y2_bytes = bits_to_bytes(y2_bits)
    hash_l = x2_bytes + plaintext + y2_bytes
    hash_object=hashlib.sha512()
    hash_object.update(hash_l)
    C3=hash_object.hexdigest()
    print("C3 = Hash(x2 ∥ M ∥ y2)=", C3)
    C1_hex = bits_to_hex(C1_bits)
    C2_hex = hex(C2)[2:]
    C3_hex = C3
    C_hex = C1_hex + C2_hex + C3_hex
    print("\n密文C = C1 ∥ C2 ∥ C3=", C_hex)
    return C_hex

def main():
    M='74657374736d34'
    Pb=generate_key()
    encry_sm2(Pb, M)
main()