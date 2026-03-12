#include <stdio.h>
#include <stdlib.h>

//a[0]=s  a[1]=t
int a[4];

//拓展欧几里德算法
void extended_euclid(int x,int y)
{
    int r1,r2,s1,s2,t1,t2;
    r1=x;s1=1;t1=0;
    r2=y;s2=0;t2=1;
    while(r2!=0)
    {
        int q=r1/r2;
        int tem1=r1-q*r2;
        int tem2=s1-q*s2;
        int tem3=t1-q*t2;
        r1=r2;s1=s2;t1=t2;
        r2=tem1;s2=tem2;t2=tem3;
    }
    a[0]=s1;a[1]=t1;
}
int main()
{
    int x,y;
    scanf("%d%d",&x,&y);
    extended_euclid(x,y);
    printf("s=%d   t=%d",a[0],a[1]);
    return 0;
}


