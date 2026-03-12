#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#define  maxsize 1000
int p,a,b,num;
int x[maxsize],y[maxsize];
int ifPrime(int p);//检测p是否为素数 
int extended_euclidean(int a,int b);//扩展的欧几里得算法 
double quickPow(int c,int m,int n);
int createGroud();//椭圆曲线群的构造 
void addition(int *P,int *Q,int *add);//加法运算
int fmod2(int a,int p);//取模，a mod p 
void EDPC(int x1,int y1,int n,int *sum);//高效倍点运算 
void main()
{
	int add[2]={0,0},sum[2]={0,0},judge;
	int x1[maxsize],y1[maxsize],n[maxsize],i=0;
	printf("请输入素数p：");
	scanf("%d",&p);
	while(!ifPrime(p))	
	{
		printf("\n您输入的数不是素数，请重新输入素数p：");
		scanf("%d",&p);
	}
	while(1)
	{
		printf("\n请输入椭圆曲线方程y^2=x^3+ax+b(mod p)中a和b的值：");
		scanf("%d %d",&a,&b);
		if(fmod(4*pow(a,3)+27*b*b,p)!=0) break;
		printf("您输入的a和b的使加法无意义！！！需要满足4*a^3+27*b^2(mod p)!=0\n"); 
	}
	fflush(stdin);
	printf("\n椭圆曲线方程:y^2=x^3+%d*x+%d(mod %d)",a,b,p);
	printf("椭圆曲线群中所有的点：\n");
	num=createGroud();
	printf("\n椭圆曲线群中共有%d个点\n\n",num);
	printf("请输入进行倍点运算的点的坐标和倍数：");
	scanf("%d %d %d",&x1[i],&y1[i],&n[i]);
	fflush(stdin);
	EDPC(x1[i],y1[i],n[i],sum);
	printf("%d(%d,%d)=(%d,%d)\n",n[i],x1[i],y1[i],sum[0],sum[1]);
	while(1)
	{
		i++;
		int sum[2]={0,0};
		printf("还要进行倍点运算吗？若继续进行，请输入1；结束请输入2:");
		scanf("%d",&judge);
		fflush(stdin);
		if(judge==2) break;
		printf("请输入进行倍点运算的点的坐标和倍数：");
		scanf("%d %d %d",&x1[i],&y1[i],&n[i]);
		fflush(stdin);
		EDPC(x1[i],y1[i],n[i],sum);
		printf("%d(%d,%d)=(%d,%d)\n",n[i],x1[i],y1[i],sum[0],sum[1]);
	}
}
//取模，a mod p 
int fmod2(int a,int p)
{
	return a-p*floor(1.0*a/p);
}
//检测p是否为素数 
int ifPrime(int p)
{
	int i;
	if(p!=2)
	{
		for(i=2;i<=sqrt(p);i++) 
			if(p%i==0) return 0;
	}
	return 1;
}
//快速模幂运算 
double quickPow(int c,int m,int n)//m为幂数，n为模数，c为底数 
{
	int r,i,temp,count,temp2,bin[maxsize];
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
		temp2=fmod(pow(temp,2)*pow(c,bin[i]),n);
		temp=temp2;
	}
	return 1.0*temp;
}
int createGroud()//椭圆曲线群的构造                  
{
	int j=0,i,k;
	float u[maxsize];
	for(i=0;i<p;i++)//算出勒让德符号,存入数组u中 
	{
		u[i]=quickPow(fmod(pow(i,3)+a*i+b,p),(p-1)/2,p);	
	}
	for(i=0;i<p;i++)
	{
		if(fmod2(pow(i,3)+a*i+b,p)==0) //y=0,只有1个平方根 
		{
			x[j]=i;
			y[j++]=0;
		}
		//根据勒让德符号，判断是否有二次剩余，若是将i存入横坐标数组 
		if((int)u[i]==1)
		{
			for(k=0;k<p;k++)//遍历0到p-1，求横坐标对应的两个纵坐标(j增加2)
			{
				if(fmod2(k*k-pow(i,3)-a*i-b,p)==0) 
				{
					x[j]=i;
					y[j++]=k;
				}
			}
		}
	}
	x[j]=0;
	y[j]=0;//把无穷远点放入数组 
	for(i=0;i<j+1;i++)
	{
		printf("(%2d,%2d)",x[i],y[i]);
	}
	return j+1;//返回圆曲线群中所有的点的数量 
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
	return y2;
}

//加法运算
void addition(int *P,int *Q,int *add) 
{
	int z,n1=-1,n2=-1,i;
	if(P[0]==0&&P[1]==0)//P为无穷远点 
	{
	add[0]=Q[0];add[1]=Q[1];return;
	}
	if(Q[0]==0&&Q[1]==0)//Q为无穷远点 
	{
		add[0]=P[0];add[1]=P[1];return;
	}
	if(P[0]==Q[0]&&(P[1]+Q[1])%p==0)//P为Q的加法逆元，相加为无穷远点，设定为（0，0） 
	{
		add[0]=0;add[1]=0;
		return;
	}
	if(P[0]!=Q[0]||P[1]!=Q[1])//Q和P不相等 
		z=fmod2((Q[1]-P[1])*extended_euclidean(p,fmod2(Q[0]-P[0],p)),p);
	else z=fmod2((3*P[0]*P[0]+a)*extended_euclidean(p,2*P[1]),p);//Q和P相等
	add[0]=fmod2(z*z-P[0]-Q[0],p);
	add[1]=fmod2(z*(P[0]-add[0])-P[1],p);
	return;
}
//高效倍点运算 
void EDPC(int x1,int y1,int n,int *sum)
{
	int Q[2],tmp[2];
	Q[0]=x1;
	Q[1]=y1;
	while(n>0)
	{
		if(n%2==1)
		{
			tmp[0]=sum[0];
			tmp[1]=sum[1];
			addition(tmp,Q,sum);
		}
		tmp[0]=Q[0];
		tmp[1]=Q[1];
		addition(tmp,tmp,Q);
		n=n/2;
	}
}
