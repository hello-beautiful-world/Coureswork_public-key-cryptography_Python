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
	int i,p,pr[maxsize],num,g,A,B,a,b,K_A,K_B;
	srand(time(NULL));
	p=rand()%30+2;
	while(!ifPrime(p))	p=rand()%30+2;
	if(p==2) 
	{
		pr[0]=1;
		num=1;
	}
	else num=primitiveRoot(p,pr);
	printf("%d的%d个本原根为：",p,num);
	for(i=0;i<num;i++) printf("%d ",pr[i]);
	g=pr[0];//取最小本原根作为共享参数
	a=1+rand()%(p-1);//a为Alice的私钥 ,a<p
	b=1+rand()%(p-1);//b为Bob的私钥 
	A=fmod(pow(g,a),p);//A为Alice的公钥 
	B=fmod(pow(g,b),p);//B为Bob的公钥 
	K_A=fmod(pow(B,a),p);//K_A为Alice计算所得的共享密钥 
	K_B=fmod(pow(A,b),p);//K_B为Bob计算所得的共享密钥 
	printf("\n共享参数p为%d,g为%d\n",p,g);
	printf("\nAlice的私钥为%d,计算所得公钥为%d,计算所得共享密钥为%d\n",a,A,K_A);
	printf("Bob的私钥为%d,计算所得公钥为%d,计算所得共享密钥为%d",b,B,K_B);
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
