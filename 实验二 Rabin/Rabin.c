#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>
#define  maxsize 100

int miller_rabin(int p);
int quickPow(int a,int m,int n);
int chinese_remainder_theorem(int a[],int m[]);
void extended_euclidean_algorithm(int m[],int M[],int num); 
int e[maxsize];
int bin[maxsize];
void main()
{
	int p,q,n;//p、q为两个私钥，n=p*q 
	int count,judge,i;//count记录输入明文数量 
	int plaintext[maxsize];//存储明文
	int ciphertext[maxsize];//存储加密后所得密文 
	int a1[maxsize],a2[maxsize],a3[maxsize],a4[maxsize],m[maxsize],k1,k2,k3,k4,C;//C为一个密文  
	char s;
	srand(time(NULL));
	p=4*(rand()%5+2)+3;//p ≡q ≡3 mol 4
	q=4*(rand()%5+2)+3;//限制p、q范围 
	//判断P、q是否为素数,不是则重新生成 
	while(miller_rabin(p))	p=4*(rand()%5+2)+3;
	while(miller_rabin(q)||p==q)	q=4*(rand()%5+2)+3;
	printf("p=%d q=%d\n",p,q);
	//计算n 
	n=p*q;
	//加解密选择 
	printf("加密请输入1，解密请输入2：\n");
	scanf("%d",&judge);
	while(judge!=1&&judge!=2) 
	{
		printf("输入有误，请重新输入，加密请输入1，解密请输入2：\n"); 
		scanf("%d",&judge);
	}
	if(judge==1)
	{
	//输入明文 
		printf("请输入明文：\n");
		for(i=0;i<maxsize&&s!='\n';i++)	
		{
			scanf("%d",&plaintext[i]);
			s=getchar();//来接受是否是回车
			count++;//检测输入个数
		}
		printf("您要加密的明文：\n");
		for(i=0;i<count;i++)  printf("%d ",plaintext[i]);
	//加密
		for(i=0;i<count;i++) 
		{
			ciphertext[i]=fmod(pow(plaintext[i],2),n);
		}
		printf("\n加密后的密文:\n");
		for(i=0;i<count;i++) printf("%d ",ciphertext[i]);
	}
	//解密
	else
	{
		//输入密文 
		printf("请输入一个密文：\n");
		scanf("%d",&C);
		printf("您要解密的密文：\n");
		printf("%d ",C);
		//解密
		k1=pow(C,(p+1)/4);
		k2=p-pow(C,(p+1)/4);
		k3=pow(C,(q+1)/4);
		k4=q-pow(C,(q+1)/4);
		
		m[0]=p;
		m[1]=q;
		
		a1[0]=k1;
		a1[1]=k3;
		a2[0]=k1;
		a2[1]=k4;
		a3[0]=k2;
		a3[1]=k3;
		a4[0]=k2;
		a4[1]=k4;
		plaintext[0]=chinese_remainder_theorem(a1,m);
		plaintext[1]=chinese_remainder_theorem(a2,m);
		plaintext[2]=chinese_remainder_theorem(a3,m);
		plaintext[3]=chinese_remainder_theorem(a4,m);
		printf("\n解密后可能的明文：:\n");
		for(i=0;i<4;i++) printf("%d ",plaintext[i]);
	}
}

//中国剩余定理
int chinese_remainder_theorem(int a[],int m[]) 
{
	int i,M1=1,x=0,X;
	int M[maxsize];
	for(i=0;i<2;i++) M1=M1*m[i];
	for(i=0;i<2;i++) M[i]=M1/m[i];
	extended_euclidean_algorithm(m,M,2);
	for(i=0;i<2;i++) x+=a[i]*e[i]*M[i];
	X=fmod(x,M1);
	return X;
}
//素性检测 
int miller_rabin(int n)
{
	int a,temp,i,j,s,k,max;
	if(n==2||n==3||n==5) return 0;
	else
	{
		temp=n-1;
		for(s=0;temp%2==0;s++)
		{
			temp/=2;
		}
		k=(n-1)/pow(2,s);
		max=n-2;
		for(i=0;i<max;i++)//检测n-2次 
		{
			a=i+2;//遍历2~n-1 
			if(quickPow(a,k,n)==1) break;
			for(j=0;j<s;j++)
			{
				if(quickPow(a,k*pow(2,j),n)==-1) break;
			}
			if(j==s) continue;
			else break;
		}
		if(i==max&&j==s) return 1;
		else return 0;
	}
}
//快速指数算法 
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
//扩展的欧几里得算法
void extended_euclidean_algorithm(int m[],int M[],int num)
{
	int i,x1,x2,x3,y1,y2,y3,t1,t2,t3,Q;
	for(i=0;i<num;i++)
	{
		x1=1;
		x2=0;
		y1=0;
		y2=1;
		x3=m[i];
		y3=M[i];
		while(1)
		{
			if(y3==1) 
			{
				if(y2<0) e[i]=y2+m[i];
				else e[i]=y2;
				break;
			}
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
	}
}
	 
