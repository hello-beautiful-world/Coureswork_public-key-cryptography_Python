import os
import random
import math
from ctypes import CDLL, c_void_p, byref, c_ubyte
from hggm.SM3 import digest as sm3
 
SM2_p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
SM2_a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
SM2_b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
SM2_n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
SM2_Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
SM2_Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
SM2_G = (SM2_Gx, SM2_Gy)
PARA_SIZE = 32  # 参数长度（字节）
HASH_SIZE = 32  # sm3输出256位（32字节）
KEY_LEN = 128  # 默认密钥位数
 
 
# 转换为bytes，第二参数为字节数（可不填）
def to_byte(x, size=None):
    if isinstance(x, int):
        if size is None:  # 计算合适的字节数
            size, tmp = 0, x >> 64
            while tmp:
                size += 8
                tmp >>= 64
            tmp = x >> (size << 3)
            while tmp:
                size += 1
                tmp >>= 8
        elif x >> (size << 3):  # 指定的字节数不够则截取低位
            x &= (1 << (size << 3)) - 1
        return x.to_bytes(size, byteorder='big')
    elif isinstance(x, str):
        x = x.encode()
        if size is not None and len(x) > size:  # 超过指定长度
            x = x[:size]  # 截取左侧字符
        return x
    elif isinstance(x, bytes):
        if size is not None and len(x) > size:  # 超过指定长度
            x = x[:size]  # 截取左侧字节
        return x
    elif isinstance(x, tuple):  # 如坐标形式(x, y)
        return b''.join(to_byte(i, size) for i in x)
    return bytes(x)
 
 
# 将列表元素转换为bytes并连接
def join_bytes(*data_list):
    return b''.join(to_byte(i) for i in data_list)
 
 
# 计算比特位数
def get_bit_num(x):
    if isinstance(x, int):
        num, tmp = 0, x >> 64
        while tmp:
            num += 64
            tmp >>= 64
        tmp = x >> num >> 8
        while tmp:
            num += 8
            tmp >>= 8
        x >>= num
        while x:
            num += 1
            x >>= 1
        return num
    elif isinstance(x, str):
        return len(x.encode()) << 3
    elif isinstance(x, bytes):
        return len(x) << 3
    return 0
 
 
# 将字节转换为int
def to_int(byte):
    return int.from_bytes(byte, byteorder='big')
 
 
# 求最大公约数
def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)
 
 
# 求乘法逆元过程中的辅助递归函数
def get_(a, b):
    if b == 0:
        return 1, 0
    x1, y1 = get_(b, a % b)
    x, y = y1, x1 - a // b * y1
    return x, y
 
 
# 求乘法逆元
def get_inverse(a, p):
    # return pow(a, p-2, p) # 效率较低、n倍点的时候两种计算方法结果会有不同
    if gcd(a, p) == 1:
        x, y = get_(a, p)
        return x % p
    return 1
 
 
# 密钥派生函数（从一个共享的秘密比特串中派生出密钥数据）
# SM2第3部分 5.4.3
# Z为bytes类型
# klen表示要获得的密钥数据的比特长度（8的倍数），int类型
# 输出为bytes类型
def KDF(Z, klen=KEY_LEN):
    ksize, K = klen >> 3, bytearray()
    for ct in range(1, math.ceil(ksize / HASH_SIZE) + 1):
        K.extend(sm3(Z + to_byte(ct, 4)))
    return K[:ksize]
 
 
# 椭圆曲线点（参数xy可为int二元组或bytes）
class ECC_Point:
    def __init__(self, xy, ec_context, size):
        if isinstance(xy, c_void_p):  # 用于快速复制点
            self.ptr, self.size = xy, size
            return
        xb, yb = (xy[:size], xy[size:]) if isinstance(xy, bytes) else (to_byte(xy[0], size), to_byte(xy[1], size))
        self.ptr, self.size = c_void_p(), size
        res = _ec_lib.ec_ws_new_point(byref(self.ptr), xb, yb, size, ec_context)
        if res:
            raise ValueError("The EC point does not belong to the curve") if res == 15 \
                else ValueError("Error %d while instantiating an EC point" % res)
 
    @property
    def bin_xy(self):
        xb, yb, c_bytes = bytearray(self.size), bytearray(self.size), c_ubyte * self.size
        res = _ec_lib.ec_ws_get_xy(c_bytes.from_buffer(xb), c_bytes.from_buffer(yb), self.size, self.ptr)
        if res:
            raise ValueError("Error %d while encoding an EC point" % res)
        return xb, yb
 
    @property
    def x(self):
        return to_int(self.bin_xy[0])
 
    @property
    def y(self):
        return to_int(self.bin_xy[1])
 
    @property
    def xy(self):
        xb, yb = self.bin_xy
        return to_int(xb), to_int(yb)
 
    def __bytes__(self):
        xb, yb = self.bin_xy
        return bytes(xb + yb)
 
    def __repr__(self):
        xb, yb = self.bin_xy
        return '0x%s, 0x%s' % (xb.hex(), yb.hex())
 
    def is_point_at_infinity(self):
        return self.xy == (0, 0)
 
    def __eq__(self, P):
        return _ec_lib.ec_ws_cmp(self.ptr, P.ptr) == 0
 
    def copy(self):
        new_ptr = c_void_p()
        res = _ec_lib.ec_ws_clone(byref(new_ptr), self.ptr)
        if res:
            raise ValueError("Error %d while cloning an EC point" % res)
        return ECC_Point(new_ptr, None, self.size)
 
    def __neg__(self):
        new_P = self.copy()
        res = _ec_lib.ec_ws_neg(new_P.ptr)
        if res:
            raise ValueError("Error %d while inverting an EC point" % res)
        return new_P
 
    def double(self):
        res = _ec_lib.ec_ws_double(self.ptr)
        if res:
            raise ValueError("Error %d while doubling an EC point" % res)
        return self
 
    def __iadd__(self, P):
        res = _ec_lib.ec_ws_add(self.ptr, P.ptr)
        if res:
            raise ValueError("EC points are not on the same curve") if res == 16 \
                else ValueError("Error %d while adding two EC points" % res)
        return self
 
    def __add__(self, P):
        return self.copy().__iadd__(P)
 
    def __imul__(self, k):
        if k < 0:
            raise ValueError("Scalar multiplication is only defined for non-negative integers")
        k_byte = to_byte(k)
        res = _ec_lib.ec_ws_scalar(self.ptr, k_byte, len(k_byte), 0)
        if res:
            raise ValueError("Error %d during scalar multiplication" % res)
        return self
 
    def __mul__(self, k):
        return self.copy().__imul__(k)
 
    def __rmul__(self, k):
        return self.copy().__imul__(k)
 
 
# 椭圆曲线
class ECC_Curve:
    def __init__(self, p, a, b, n, G, size):
        self.context = c_void_p()
        res = _ec_lib.ec_ws_new_context(byref(self.context), to_byte(p, size), to_byte(b, size), to_byte(n, size), size)
        if res:
            raise ImportError("Error %d initializing ECC context" % res)
        self.G = ECC_Point(G, self.context, size)
        if n == SM2_n and os.path.exists(_SM2kG_file):
            with open(_SM2kG_file, 'rb') as f:
                bin_data = f.read()
                one_size, line_size = size << 1, 255 * (size << 1)  # 单个点坐标字节数、一行数据字节数
                self.kG_points = tuple(tuple(ECC_Point(bin_data[i + j: i + j + one_size], self.context, size) for j in
                                             range(0, line_size, one_size)) for i in
                                       range(0, size * line_size, line_size))
            self.kG = self.kG_fast
        else:  # 如果未采用标准SM2参数，则用普通点乘（启用预计算加速需要用到pre_kG函数的输出内容）
            self.kG = self.kG_normal
        # 预先计算用到的常数
        self.w_l_1 = math.ceil(math.ceil(math.log(n, 2)) / 2) - 1  # w * 2
        self.Z_tmp = to_byte((a, b, G[0], G[1]), size)  # Z值的中间部分
 
    # 采用预计算好的数据快速计算kG
    def kG_fast(self, k):
        P = None
        for i, byte in enumerate(k.to_bytes(32, byteorder='little')):
            if byte:
                if P is None:
                    P = self.kG_points[i][byte - 1].copy()
                else:
                    P += self.kG_points[i][byte - 1]
        return P
 
    def kG_normal(self, k):
        return self.G * k
 
 
# SM2类继承了ECC_Curve的方法
class SM2:
    # 默认使用SM2推荐曲线参数
    def __init__(self, p=SM2_p, a=SM2_a, b=SM2_b, n=SM2_n, G=SM2_G, size=PARA_SIZE, h=1,  # 余因子h默认为1
                 ID=None, sk=None, pk=None, genkeypair=True):  # genkeypair表示是否自动生成公私钥对
        curve = _curves.setdefault(n, ECC_Curve(p, a, b, n, G, size))
        self.n, self.h, self.size, self.context, self.kG = n, h, size, curve.context, curve.kG
        # 除曲线外的其他参数
        self.ID = ID if type(ID) in (int, str) else ''  # 身份ID（数字或字符串）
        if sk and pk:  # 已提供公私钥对
            try:  # 验证该公私钥对
                if self.kG(sk) == ECC_Point(pk, self.context, size):  # 通过验证，即使genkeypair=True也不会重新生成
                    self.sk, self.pk = sk, pk  # 私钥（int [1,n-2]），公钥（x, y）
                else:  # 不合格则生成
                    self.sk, self.pk = self.gen_keypair()
            except ValueError:  # 不在曲线上会报错，重新生成
                self.sk, self.pk = self.gen_keypair()
        elif genkeypair:  # 自动生成合格的公私钥对
            self.sk, self.pk = self.gen_keypair()
 
        # 预先计算可能用到的常数
        self.w_l_1, self.Z_tmp = curve.w_l_1, curve.Z_tmp
        if hasattr(self, 'sk'):  # 签名时
            self.d_1 = get_inverse(1 + self.sk, n)
 
    # 判断是否在椭圆曲线上
    def on_curve(self, xy):
        try:
            return ECC_Point(xy, self.context, self.size)  # 不报错则返回ECC点对象
        except ValueError:  # 报错说明不在曲线上
            return False
 
    # 生成密钥对
    # 返回值：d为私钥，P为公钥
    # SM2第1部分 6.1
    def gen_keypair(self, toTuple=True):
        d = random.randint(1, self.n - 2)
        P = self.kG(d)
        return d, P.xy if toTuple else P
 
    # 计算Z
    # SM2第2部分 5.5
    # ID为数字或字符串，pk为公钥（不提供参数时返回自身Z值）
    def get_Z(self, ID=None, pk=None):
        save = False
        if pk is None:  # 不提供参数
            if hasattr(self, 'Z'):  # 再次计算，返回曾计算好的自身Z值
                return self.Z
            else:  # 首次计算自身Z值
                ID, pk, save = self.ID, self.pk, True
        entlen = get_bit_num(ID)
        ENTL = to_byte(entlen, 2)
        Z = sm3(join_bytes(ENTL, ID, self.Z_tmp, pk))
        if save:  # 保存自身Z值
            self.Z = Z
        return Z
 
    # 数字签名
    # SM2第2部分 6.1
    # 输入：待签名的消息M、随机数k（不填则自动生成）、输出类型（默认bytes）、对M是否hash（默认是）
    # 输出：r, s（int类型）或拼接后的bytes
    def sign(self, M, k=None, outbytes=True, dohash=True):
        if dohash:
            M_ = join_bytes(self.get_Z(), M)
            e = to_int(sm3(M_))
        else:
            e = to_int(to_byte(M))
        while True:
            if not k:
                k = random.randint(1, self.n - 1)
            x1 = self.kG(k).x
            r = (e + x1) % self.n
            if r == 0 or r + k == self.n:
                k = 0
                continue
            s = self.d_1 * (k - r * self.sk) % self.n
            if s:
                break
            k = 0
        return to_byte((r, s), self.size) if outbytes else (r, s)
 
    # 数字签名验证
    # SM2第2部分 7.1
    # 输入：收到的消息M′及其数字签名sig(r′, s′)、签名者的身份标识IDA及公钥PA、对M是否hash（默认是）
    # 输出：True or False
    def verify(self, M, sig, IDA, PA, dohash=True):
        PA_bytes = PA if isinstance(PA, bytes) else to_byte(PA, self.size)
        PA = self.on_curve(PA_bytes)
        if not PA:
            return False  # 对方公钥不在椭圆曲线上
        r, s = (to_int(sig[:self.size]), to_int(sig[self.size:])) if isinstance(sig, bytes) else sig
        if not 1 <= r <= self.n - 1 or not 1 <= s <= self.n - 1:
            return False
        if dohash:
            M_ = join_bytes(self.get_Z(IDA, PA_bytes), M)
            e = to_int(sm3(M_))
        else:
            e = to_int(to_byte(M))
        t = (r + s) % self.n
        if t == 0:
            return False
        PA *= t
        PA += self.kG(s)
        x1 = PA.x
        # x1 = int((kG(s) + t * PA).x)
        R = (e + x1) % self.n
        return R == r
 
    # A 发起协商
    # SM2第3部分 6.1 A1-A3
    # 返回rA、RA（当outbytes=True时RA为拼接后的bytes）
    def agreement_initiate(self, outbytes=True):
        rA, RA = self.gen_keypair(False)
        return rA, bytes(RA) if outbytes else RA.xy
 
    # B 响应协商（option=True时计算选项部分，outbytes=True时RB为拼接后的bytes）
    # SM2第3部分 6.1 B1-B9
    def agreement_response(self, RA, PA, IDA, option=False, rB=None, RB=None, klen=KEY_LEN, outbytes=True):
        # 参数准备
        PA_bytes = PA if isinstance(PA, bytes) else to_byte(PA, self.size)
        PA = self.on_curve(PA_bytes)
        if not PA:
            return False, '对方公钥不在椭圆曲线上'
        x1, RA_bytes = (to_int(RA[:self.size]), RA) if isinstance(RA, bytes) else (RA[0], to_byte(RA, self.size))
        RA = self.on_curve(RA_bytes)
        if not RA:
            return False, 'RA不在椭圆曲线上'
        if not hasattr(self, 'sk'):
            self.sk, self.pk = self.gen_keypair()
        ZA, ZB = self.get_Z(IDA, PA_bytes), self.get_Z()
        # B1-B7
        if not rB:
            rB, RB = self.agreement_initiate(outbytes)
        x2, RB_bytes = (to_int(RB[:self.size]), RB) if isinstance(RB, bytes) else (RB[0], to_byte(RB, self.size))
        x_2 = self.w_l_1 + (x2 & self.w_l_1 - 1)
        tB = (self.sk + x_2 * rB) % self.n
        x_1 = self.w_l_1 + (x1 & self.w_l_1 - 1)
        RA *= x_1
        RA += PA
        RA *= self.h * tB
        xVb, yVb = RA.bin_xy
        # V = (self.h * tB) * (x_1 * RA + PA)
        if (to_int(xVb), to_int(yVb)) == (0, 0):
            return False, 'V是无穷远点'
        KB = KDF(join_bytes(xVb, yVb, ZA, ZB), klen)
        if not outbytes and isinstance(RB, bytes):
            RB = (x2, to_int(RB[self.size:]))
        if not option:
            return True, (RB_bytes if outbytes else RB, KB)
        # B8、B10（可选部分）
        tmp = join_bytes(yVb, sm3(join_bytes(xVb, ZA, ZB, RA_bytes, RB_bytes)))
        SB, S2 = sm3(join_bytes(2, tmp)), sm3(join_bytes(3, tmp))
        return True, (RB_bytes if outbytes else RB, KB, SB, S2)
 
    # A 协商确认
    # SM2第3部分 6.1 A4-A10
    def agreement_confirm(self, rA, RA, RB, PB, IDB, SB=None, option=False, klen=KEY_LEN):
        # 参数准备
        PB_bytes = PB if isinstance(PB, bytes) else to_byte(PB, self.size)
        PB = self.on_curve(PB_bytes)
        if not PB:
            return False, '对方公钥不在椭圆曲线上'
        x2, RB_bytes = (to_int(RB[:self.size]), RB) if isinstance(RB, bytes) else (RB[0], to_byte(RB, self.size))
        RB = self.on_curve(RB_bytes)
        if not RB:
            return False, 'RB不在椭圆曲线上'
        if not hasattr(self, 'sk'):
            self.sk, self.pk = self.gen_keypair()
        ZA, ZB = self.get_Z(), self.get_Z(IDB, PB_bytes)
        # A4-A8
        x1, RA_bytes = (to_int(RA[:self.size]), RA) if isinstance(RA, bytes) else (RA[0], to_byte(RA, self.size))
        x_1 = self.w_l_1 + (x1 & self.w_l_1 - 1)
        tA = (self.sk + x_1 * rA) % self.n
        x_2 = self.w_l_1 + (x2 & self.w_l_1 - 1)
        RB *= x_2
        RB += PB
        RB *= self.h * tA
        xUb, yUb = RB.bin_xy
        # U = (self.h * tA) * (x_2 * RB + PB)
        if (to_int(xUb), to_int(yUb)) == (0, 0):
            return False, 'U是无穷远点'
        KA = KDF(join_bytes(xUb, yUb, ZA, ZB), klen)
        if not option or not SB:
            return True, KA
        # A9-A10（可选部分）
        tmp = join_bytes(yUb, sm3(join_bytes(xUb, ZA, ZB, RA_bytes, RB_bytes)))
        S1 = sm3(join_bytes(2, tmp))
        if S1 != SB:
            return False, 'S1 != SB'
        SA = sm3(join_bytes(3, tmp))
        return True, (KA, SA)
 
    # B 协商确认（可选部分）
    # SM2第3部分 6.1 B10
    def agreement_confirm2(self, S2, SA):
        return (True, '') if S2 == SA else (False, 'S2 != SA')
 
    # 加密
    # SM2第4部分 6.1
    # 输入：待加密的消息M（bytes或str类型）、对方的公钥PB、随机数k（不填则自动生成）
    # 输出(True, bytes类型密文)或(False, 错误信息)
    def encrypt(self, M, PB, k=None):
        PB = self.on_curve(PB)
        if not PB:
            return False, '对方公钥不在椭圆曲线上'
        M = to_byte(M)
        klen = get_bit_num(M)
        while True:
            if not k:
                k = random.randint(1, self.n - 1)
            PB *= k
            x2b, y2b = PB.bin_xy
            # x2, y2 = (k * PB).xy
            t = to_int(KDF(x2b + y2b, klen))
            if t:
                break
            k = 0  # 若t为全0比特串则继续循环
        C1, C2, C3 = bytes(self.kG(k)), to_byte(to_int(M) ^ t, len(M)), sm3(join_bytes(x2b, M, y2b))
        return True, join_bytes(C1, C2, C3)
 
    # 解密
    # SM2第4部分 7.1
    # 输入：密文C（bytes类型）
    # 输出(True, bytes类型明文)或(False, 错误信息)
    def decrypt(self, C):
        double_size = self.size << 1
        C1 = self.on_curve(C[:double_size])
        if not C1:
            return False, 'C1不满足椭圆曲线方程'
        C1 *= self.sk
        x2b, y2b = C1.bin_xy
        # x2, y2 = (self.sk * C1).xy
        klen = len(C) - double_size - HASH_SIZE << 3
        t = to_int(KDF(x2b + y2b, klen))
        if t == 0:
            return False, 't为全0比特串'
        C2, C3 = C[double_size:-HASH_SIZE], C[-HASH_SIZE:]
        M = to_byte(to_int(C2) ^ t, len(C2))
        u = sm3(join_bytes(x2b, M, y2b))
        return (True, M) if u == C3 else (False, 'u != C3')
 
 
# 预计算kG（将32行255列的椭圆曲线点矩阵输出为二进制文件）
def pre_kG():
    kG_points = [_curves[SM2_n].G * k for k in range(1, 256)]
    with open(_SM2kG_file, 'wb') as f:
        f.write(b''.join(map(bytes, kG_points)))
        for i in range(31):
            f.write(b''.join(map(bytes, map(lambda P: P.__imul__(256), kG_points))))
 
 
_ec_lib = CDLL('hggm/ecc.pyd')  # 读取用于ECC计算的C链接库（原文件为Crypto/PublicKey/_ec_ws.pyd）
_SM2kG_file = 'hggm/SM2_kG.bin'  # 预计算数据文件的位置
_curves = {SM2_n: ECC_Curve(SM2_p, SM2_a, SM2_b, SM2_n, SM2_G, PARA_SIZE)}  # 椭圆曲线对象字典（以参数n为键）
