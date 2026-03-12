#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>
#define  maxsize 100
int judge_p_a(int p2,double p3);

void main()
{
	int p,p2,a=1,i,judge,p4;
	double p3;
	srand(time(NULL));
	p=rand()%39+2;//限制范围在2到30
	while(1)
	{
		
		if(p==2||p==4) //判断p是否为2或4 
		{
			printf("p的值为：%d",p);
			break;
		}
		else
		{
			if(p%2==0)//判断p是否为素奇数的幂 
			{
				p2=p/2;
				p3=pow(p2,1.0/a);
				if(p3==(int)p3) judge=judge_p_a(p2,p3);
			}	
			else//判断p是否为2倍的素奇数的幂 
			{
				p2=p;
				p3=pow(p2,1.0/a);
				if(p3==(int)p3) judge=judge_p_a(p2,p3);
			}
		}
	if(judge==1) 
	{
		printf("p的值为：%d",p);
		break;
	}
	p=rand()%39+2;//重新生产p	
	}
}

int judge_p_a(int p2,double p3)
{
	int i,a=1;
	while(p3>2)
	{
		for(i=3;i<=sqrt(p3);i++)//判断p3是否为奇素数 
		{
			if((int)p3%i==0)
			{
				break;
			}
		}
		if(i>sqrt(p3))
		{
			return 1;
		}
		a++;
		p3=pow(p2,1.0/a);
		while(1)
		{
			if(p3==(int)p3) break;
			else
			{
				a++;
				p3=pow(p2,1.0/a);
			}
		}
	}
	if(p3<=2)	return 0;
}
