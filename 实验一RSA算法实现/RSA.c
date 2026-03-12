#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>
#define  maxsize 100

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
	//判断P、q是否为素数(是否能被不超过sqrt(q)的整数整除)，不是则重新生成 
	while(1){
		for(i=2;i<=sqrt(p);i++)
		{
			if(p%i==0)
			{
				break;
			}
		}
		if(i>sqrt(p))
		{
			break;
		}
		else
		{
			p=rand()%19+2; 
		}
	}
	while(1){
		for(i=2;i<=sqrt(q);i++)
		{
			if(q%i==0)
			{
				break;
			}
		}
		if(i>sqrt(q)&&p!=q)//p不能等于q 
		{
			break;
		}
		else
		{
			q=rand()%19+2;
		}
	}		
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

