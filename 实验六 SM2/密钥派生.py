import hashlib
from math import ceil

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
'''
函数名：hex_to_bits
功能：十六进制字符串转换为比特串
传递参数：h-str型-十六进制串
返回值：b-str类型
'''
def hex_to_bits(h):
    b_list = []
    for i in h:
        b = bin(eval('0x' + i))[2:].rjust(4, '0')           
        b_list.append(b)
    b = ''.join(b_list)
    return b

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
x='000010000111001'
t=keyDerivation(x,1025)
print(t)





    
    
