import math
'''
函数名：int_byte
功能:将整数转换为字节串
传递参数：num-int类型的十进制数
'''
def int_byte(num):
    i=1
    while True:
        if(num>2**i-1):
            i+=1
        else: break
    byte_data=num.to_bytes(math.ceil(i/8),'big')
    print(byte_data)
    return byte_data
'''
函数名：byte_int
功能:将字节串转换为整数
传递参数：bys-bytes类型
'''
def byte_int(bys):
    byte_data=int.from_bytes(bys,'big')
    print(byte_data)

bys=int_byte(4665)
byte_int(bys)

