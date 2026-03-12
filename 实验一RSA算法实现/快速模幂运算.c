#include<stdio.h>
#include<math.h>
#define  maxsize 100

void main()
{
	int a,m,n,i,bin[maxsize],count,r,temp,temp2,t;
	printf("请输入底数a,指数m,模数n：\n");
	scanf("%d%d%d",&a,&m,&n);
	//把m转化为二进制数 
	r=m;
	for(i=0;r!=0;i++)
	{
		bin[i]=r%2;
		r/=2;
	}
	count=i;
	temp=1;
	//方法一 从左至右 
	for(i=count-1;i>=0;i--)
	{
		temp2=fmod(pow(temp,2)*pow(a,bin[i]),n);
		temp=temp2;
	}
	printf("\n方法一结果为%d",temp);
	//方法二 从右至左 
	temp=1;
	t=a;
	for(i=0;i<count;i++)
	{
		if(bin[i]==1) 
		{
			temp2=fmod(t*temp,n);
			temp=temp2;
		}
		t=fmod(t*t,n);
	}
	printf("\n方法二结果为%d",temp);
}
