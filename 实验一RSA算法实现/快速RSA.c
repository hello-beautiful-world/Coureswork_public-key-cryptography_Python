#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>
#define  maxsize 100
int bin[maxsize];
int quickPow(int a,int m,int n);
int miller_rabin(int p);
int extended_euclidean(int a,int b);

void main()
{
	int p,q,i,n,euler,c,d,e,temp1,temp2,num;//p、q为两个素数，euler为欧拉函数，d为私钥，e为公钥 
	int judge,count=0;
	int plaintext[maxsize];
	int ciphertext[maxsize];
	char s;
	srand(time(NULL));
	p=rand()%19+2;//限制范围在2到20 
	q=rand()%19+2;
	//判断P、q是否为素数,不是则重新生成 
	while(miller_rabin(p))	p=rand()%19+2;
	while(miller_rabin(q)||p==q)	q=rand()%19+2;
	
	printf("p=%d q=%d\n",p,q);
	n=p*q;
	euler=(p-1)*(q-1);
	//找到合格的公钥e	
	while(1)
	{
		while(1)
		{
			e=rand()%euler;//私钥e<euler 
			if(e!=0&&e!=1) break;//私钥e>1
		}
		temp1=euler;
		temp2=e;
		while(c=temp1%temp2)//欧几里得算法 
		{
			temp1=temp2;
			temp2=c;
		}
		if(temp2==1) break;//e与 euler互素 
		else continue;
	}
	printf("e=%d\n",e);
	//找到私钥d 
	d=extended_euclidean(e,euler);
	
	for(d=2;;d++)
	{
		if((d*e-1)%euler==0) break;
	}
	printf("d=%d\n",d);
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
			ciphertext[i]=fmod(pow(plaintext[i],e),n);
		}
		printf("\n加密后的密文:\n");
		for(i=0;i<count;i++) printf("%d ",ciphertext[i]);
	}

	//解密
	else
	{
		printf("请输入密文：\n");
		for(i=0;i<maxsize&&s!='\n';i++)
			{
		 		scanf("%d",&ciphertext[i]);
		    	s=getchar();//来接受是否是回车
		    	count++;//检测输入个数
			}
		printf("您要解密的密文：\n");
		for(i=0;i<count;i++)  printf("%d ",ciphertext[i]);
		//解密
		for(i=0;i<count;i++) 
		{
			plaintext[i]=fmod(pow(ciphertext[i],d),n);
		}
		printf("\n解密后的明文:\n");
		for(i=0;i<count;i++) printf("%d ",plaintext[i]);
	}
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
//扩展的欧几里得算法 
int extended_euclidean(int a,int b)
{
	
	int temp,x1=1,x2=0,x3,y1=0,y2=1,y3,t1,t2,t3,Q;
	if(a<b) //确保a大于b 
	{
		temp=a;
		a=b;
		b=temp;
	}
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
	return y2;
}
