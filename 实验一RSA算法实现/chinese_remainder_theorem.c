#include<stdio.h>
#include<math.h>
#define  maxsize 100
int b[maxsize];
void extended_euclidean_algorithm(int m[],int M[],int num);
//中国剩余定理 
void main() 
{
	int num,a[maxsize],m[maxsize],M[maxsize],i,M1=1,x=0,X;
	printf("请输入同余式组中同余式的个数：");
	scanf("%d",&num);
	printf("\n请输入%d个整数 a：",num);
	//输入a 
	for(i=0;i<num;i++) scanf("%d",&a[i]);
	fflush(stdin);
	//输入m 
	printf("\n请输入%d个互素的整数 m：",num);
	for(i=0;i<num;i++) scanf("%d",&m[i]);
	//求M[i] 
	for(i=0;i<num;i++) M1=M1*m[i];
	for(i=0;i<num;i++) M[i]=M1/m[i];
	extended_euclidean_algorithm(m,M,num);
	for(i=0;i<num;i++) x+=a[i]*b[i]*M[i];
	X=fmod(x,M1);
	printf("同余式的解为%d",X);
	
}
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
				if(y2<0) b[i]=y2+m[i];
				else b[i]=y2;
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
	
