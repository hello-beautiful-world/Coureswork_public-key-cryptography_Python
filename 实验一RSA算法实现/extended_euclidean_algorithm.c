#include<stdio.h>
void main()
{
	int a,b,temp,x1=1,x2=0,x3,y1=0,y2=1,y3,t1,t2,t3,Q;
	printf("请输入两个整数：\n");
	scanf("%d%d",&a,&b);
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
	printf("%d的逆元为%d",b,y2);
}
	
