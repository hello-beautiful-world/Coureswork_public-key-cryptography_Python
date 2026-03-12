a=-1
b=188
x=0
y=376
p=751
j_a=121
j_b=203
#求椭圆曲线群上的点
#通过表达式生成z
def generate_z(p):
    z_0=[]
    for x in range(0,p):
        z=(pow(x,3)-4)%p
        z_0.append(z)
    return z_0
z_0=generate_z(751)
def main1(p):
    i=0
    i_0=[]
    y_0=[]
    for z in z_0:
        for y in range(1,p):
            if (y*y)%p==z:
                i_0.append(i)
                y_0.append(y)
        i=i+1
    return i_0,y_0
i_0,y_0=main1(751)
print("群的阶为{}".format(len(i_0)+1))
#求逆元
def mod_inverse(m,n):
    for i in range(1,n):
        if (i*m)%n==1:
            break
    return i
#模运算
def mod(p,q):
    if p>=0:
        return p%q
    else:
        return q-((q-p)%q)
def same(a,b,x,y):
    if y==0:
        return(0,0)
    else:
        ni=mod_inverse(2*y,p)
        numta=mod((3*(x*x)+a)*ni,p)
        x_3=mod(numta*numta-2*x,p)
        y_3=mod(numta*(x-x_3)-y,p)
        return x_3,y_3
r,s=same(a,b,x,y)
c,d=same(a,b,x,y)
def diff(r,s,x,y):
    ni=mod_inverse(x-r,p)
    numta=mod((y-s)*ni,p)
    u=mod(numta*numta-r-x,p)
    v=mod(numta*(r-u)-s,p)
    return u,v
def main2(r,s,n,x,y):
    if n==2:
        r,s=same(a,b,x,y)
        return r,s
    else:
        if x==0 and y==0:
            return r,s
        elif r==0 and s==0:
            return x,y
        elif r==x and s==-y:
            return 0,0
        elif r==x and s==y:
            r,s=same(a,b,x,y)
            return r,s
        elif r==x:
            return 0,0
        else:
            r,s=diff(r,s,x,y)
            return r,s
def change(a):
    length=(a.bit_length()+7)//8
    a_1=a.to_bytes(length,'big')
    return a_1
def main3(r,s,n,x,y):
    for i in range(1,n-1):
        r,s=main2(r,s,n,x,y)
    return r,s
r,s=main3(r,s,j_a,x,y)
print('A的公开钥为({},{})'.format(change(r),change(s)))
c,d=main3(c,d,j_b,x,y)
print('B的公开钥为({},{})'.format(change(c),change(d)))
c,d=same(a,b,r,s)
c,d=main3(c,d,j_b,r,s)
print('共享密钥为({},{})'.format(change(c),change(d)))








