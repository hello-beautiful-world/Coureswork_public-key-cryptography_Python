import random 
from sympy import  randprime
'''
函数名：miller_rabin(n,k=5)
功能：使用miller_rabin算法进行素性检测
参数传递：n——待检测的数,k——检测次数
返回值：若检测结果为素数返回True,反之返回False
'''
def miller_rabin(n, k=10):  # 进行k测素性检测，提高准确性
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # 将n-1写为2^r * d的形式
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    # 执行k次测试
    for _ in range(10):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

'''
函数名：gcd(a, b)
功能：欧几里得算法求两个数的最大公约数
参数传递：a、b——待求公约数的两个整数
返回值：a、b的最大公约数
'''
def gcd(a, b):
    """计算两个正整数 a 和 b 的最大公约数。"""
    while b:
        a, b = b, a % b
    return a
'''
函数名：extended_gcd(a, b)
功能：扩展欧几里得算法计算a、b的最大公约数和等式中的系数
参数传递：a、b——待求公约数的两个整数
返回值：gcd-最大公约数，x、y-系数
'''
def extended_gcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y

'''
函数名：mod_inverse(a, m):
功能：计算a在模m下的逆元
参数传递：a-待求逆元的整数,m——模数
返回值：a在模 m下的逆元
'''
def mod_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise Exception('模逆元不存在')
    else:
        return x % m
    
'''
函数名：key_generation()
功能：RSA密钥生成，p、q长度均为512比特
'''
def key_generation():
    # 生成一个512比特长的随机整数
    p = randprime(2**511, 2**512)#randprime函数生成的素数是素数,减少运行时间
    q = randprime(2**511, 2**512)
    print(f"p={p} ")
    print(f"q={q} ")
    if miller_rabin(p):
        print("经过miller_rabin素性检测，p 是素数。")
    else:
        print("经过miller_rabin素性检测，p不是素数。")
    if miller_rabin(q):
        print("经过miller_rabin素性检测，q 是素数。")
    else:
        print("经过miller_rabin素性检测，q不是素数。")
    n=p*q
    print(f"n={n} ")
   # 计算 φ(n) = (p-1) * (q-1)
    euler=(p-1)*(q-1)
    #生成公钥e
    e=random.randint(2,euler-1)
    while gcd(e, euler)!=1:
        e=random.randint(2,euler-1)
    print(f"公钥e1={e} ")
    #计算私钥d,使得 (d * e) % φ(n) = 1
    d=mod_inverse(e,euler)
    print(f"私钥d1={d}")
    return p,q,n,e,d

