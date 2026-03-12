#include<stdio.h>
#include<math.h>
#define  maxsize 100
int bin[maxsize];
int quickPow(int a,int m,int n);

void main()
{
	int n,a,temp,i,j,s,k,max;
	printf("请输入一个整数：");
	scanf("%d",&n);
	if(n==2||n==3||n==5) printf("%d是素数",n);
	else
	{
		temp=n-1;
		for(s=0;temp%2==0;s++)
		{
			temp/=2;
		}
		k=(n-1)/pow(2,s);
		printf("s=%d,k=%d\n",s,k);
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
		if(i==max&&j==s) printf("%d是合数",n);
		else printf("%d是素数",n);
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
