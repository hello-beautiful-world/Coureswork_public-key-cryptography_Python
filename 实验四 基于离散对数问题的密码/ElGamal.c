#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>
#define  maxsize 100
int bin[maxsize];
int quickPow(int a,int m,int n);
int ifPrime(int p);
int primitiveRoot(int p,int *pr);
void main()
{
	int i,p,pr[maxsize],num,g,k,r,c,m,c2,m2,z,pk;
	srand(time(NULL));
	p=rand()%30+2;
	while(!ifPrime(p)||p==2)	p=rand()%30+2;
	num=primitiveRoot(p,pr);
	printf("%d的%d个本原根为：",p,num);
	for(i=0;i<num;i++) printf("%d ",pr[i]);
	g=pr[0];//取最小本原根作为公钥
	pk=1+rand()%(p-2);//私钥 aerfa
	z=quickPow(g,pk,p);//公钥 rou
	//加密
	k=1+rand()%(p-2); 
	r=quickPow(g,k,p);
	printf("\n公钥p:%d,g:%d,z:%d,生成的随机数k:%d;\n私钥pk:%d\n",p,g,z,k,pk);
	printf("r:%d\n",r);
	printf("请输入一个明文消息:");
	scanf("%d",&m);
	c=fmod(m*pow(z,k),p);
	printf("加密%d得到的密文为:%d\n",m,c);
	//解密 
	printf("请输入一个密文消息:");
	scanf("%d",&c2);
	printf("extended_euclidean(p,quickPow(r,pk,p)):%d\n",extended_euclidean(p,quickPow(r,pk,p)));
	m2=fmod(c2*extended_euclidean(p,quickPow(r,pk,p)),p);
	printf("解密%d得到的明文为%d：",c2,m2);
	
}
int quickPow(int a,int m,int n)
{
	int r,i,temp,count,temp2;
	r=m;
	for(i=0;r!=0;i++)
	{
		bin[i]=r%2;
		r/=2;
	}
	count=i;
	temp=1;
	for(i=count-1;i>=0;i--)
	{
		temp2=fmod(pow(temp,2)*pow(a,bin[i]),n);
		temp=temp2;
	}
	return temp;
}
//检测p是否为素数 
int ifPrime(int p)
{
	int i;
	if(p!=2)
	{
		for(i=2;i<=sqrt(p);i++)
		{
			if(p%i==0) return 0;
		}
	}
	return 1;
}
//求本原根
int primitiveRoot(int p,int *pr)
{
	int i,j=0,tmp,k=0,primeFactor[maxsize];
	//找出P-1的素因子，i从2开始计算 
	for(i=2;i<p-1;i++) if((p-1)%i==0&&ifPrime(i)) primeFactor[j++]=i;//循环结束时，j等于质因子个个数 
	//遍历2到p-1,找出本原根 
	for(tmp=2;tmp<p;tmp++)
	{
		for(i=0;i<j;i++)
		{
			if(quickPow(tmp,(p-1)/primeFactor[i],p)==1) break;
		}
		if(i==j) pr[k++]=tmp;
	}
	return k;//返回本原根的个数 
} 
//扩展的欧几里得算法 
int extended_euclidean(int a,int b)
{
	
	int temp,x1=1,x2=0,x3,y1=0,y2=1,y3,t1,t2,t3,Q;
	x3=a;
	y3=b;
	while(1)
	{
		if(y3==0) printf("无逆元"); 
		if(y3==1) break;
		Q=x3/y3;
		t1=x1-Q*y1;
		t2=x2-Q*y2;
		t3=x3-Q*y3;
		x1=y1;
		x2=y2;
		x3=y3;
		y1=t1;
		y2=t2;
		y3=t3;
	}
	if(y2<0) return y2+a;
	else return y2;
}
