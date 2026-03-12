#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>
#define length 3
#define MaxSize 100
void createA(int *A);
int Euclid_t(int a,int b);
void create_k_t(int *k,int *t,int sum);
int Euclid_v(int k,int t);
void createB(int *B,int *A,int t,int k);
void encrypt(int *bit_m,int *digit_c,int *B,int num);
void decode(int *digit_c2,int *A,int *bit_m2,int count2,int v,int k);
void main()
{
	int A[length],i,j,count=0,sum=0,k,t,v,B[length],bit_m[MaxSize],digit_c[MaxSize/length+1],num;//A[length]为超递增背包向量,B[length]为非超递增背包向量 ,sum为超递增背包向量的容积 
	int bit_m2[MaxSize];//bit_m2[MaxSize]表示解密所得二进制明文 
	int digit_c2[MaxSize],count2;//digit_c2[MaxSize]表示需要解密的密文 ,count2表示密文数组中元素个数 
	createA(A);
	printf("超递增背包向量为：\n");
	for(i=0;i<length;i++) 
	{
		printf("%d ",A[i]);
		sum+=A[i];
	}
	create_k_t(&k,&t,sum); 
	v=Euclid_v(k,t);
	printf("\n模数为%d,正数t为%d,t的逆元v为%d",k,t,v);
	createB(B,A,t,k);
	printf("\n非超递增背包向量为：\n");
	for(i=0;i<length;i++) 	printf("%d ",B[i]);
	//输入二进制串形式的明文，并填充
	printf("\n请输入二进制串形式的明文（每个元素用空格隔开，输入非数字类型的元素结束输入）：\n");
	while (scanf("%d", &bit_m[count]) == 1)  count++;//元素个数为count 
	printf("填充后的明文为：\n");
	i = 0;																//******注意初始化i为0，因为前面代码改变了i的初值 
	if(count%length!=0) //分组不够，用0填充 
	{
		for(i=0;i<length-count%length;i++) bit_m[count+i]=0; 
	}
	num=(count+i)/length;
	for (j = 0; j < count+i; j++)  printf("%d ", bit_m[j]);//注意********i= length-count%length
	printf("\n明文分组有%d组\n",num);
	//加密
	encrypt(bit_m,digit_c,B,num);
	printf("加密所得密文：\n");
	for (j = 0; j < num; j++)  printf("%d ",digit_c[j]);
	//解密
	printf("\n请输入数值形式的密文（每个元素用空格隔开，输入非数字类型的元素结束输入）：\n");
	fflush(stdin);
	while (scanf("%d", &digit_c2[count2]) == 1)  count2++;//密文元素个数为count2 
	decode(digit_c2,A,bit_m2,count2,v,k);
	printf("解密所得明文：\n");
	for (j = 0; j < length*count2; j++)  printf("%d ",bit_m2[j]);
	
}

//生产超递增背包向量 
void createA(int *A)
{
	int i,mod=5; 
	srand(time(NULL));
	A[0]=rand()%mod+1;//mod限制随机生产的背包元素大小 
	for(i=1;i<length;i++) A[i]=2*A[i-1]+rand()%mod+1;
} 

//扩展欧几里得算法验证生成的t是否符合和k互素 
int Euclid_t(int a,int b) 
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
		if(y3==0) return 0;//不互素 
		if(y3==1) return 1;//互素 
	}
}

//生成模数k,整数t
void create_k_t(int *k,int *t,int sum) 
{
	srand(time(NULL));
	*k=rand()%20+sum+1;//保证模数k大于背包容积 
	*t=rand()%20+2;//t>1
	while(1)
	{
		if(Euclid_t(*k,*t)) break;
		*t=rand()%20+2;
	}
}
//扩展的欧几里得算法求v(t在模k下的逆元) 
int Euclid_v(int k,int t)
{
	int temp,x1=1,x2=0,x3,y1=0,y2=1,y3,t1,t2,t3,Q;
	if(k<t) //确保a大于b 
	{
		temp=k;
		k=t;
		t=temp;
	}
	x3=k;
	y3=t;
	while(1)
	{
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
	if(k>t) return (y2+k)%k;//保证v为正数 
	return (x2+k)%k;
}
//生成作为公钥的非超递增背包向量B[length]
void createB(int *B,int *A,int t,int k) 
{
	int i;
	for(i=0;i<length;i++)
	{
		B[i]=t*A[i]%k;
	}
}
//加密
void encrypt(int *bit_m,int *digit_c,int *B,int num) 
{
	int i,j,sum;
	for(i=0;i<num;i++)
	{
		sum=0;
		for(j=0;j<length;j++) sum+=bit_m[i*length+j]*B[j];//******注意下标 
		digit_c[i]=sum;
	}
}
//解密
void decode(int *digit_c2,int *A,int *bit_m2,int count2,int v,int k) 
{
	int i,j,s;
	for(i=0;i<count2;i++)
	{
		s=v*digit_c2[i]%k;
		for(j=length-1;j>=0;j--)
		{
			if(s>=A[j]) 
			{
				bit_m2[i*length+j]=1;
				s=s-A[j];
			}
			else bit_m2[i*length+j]=0;
		}
	}
}
