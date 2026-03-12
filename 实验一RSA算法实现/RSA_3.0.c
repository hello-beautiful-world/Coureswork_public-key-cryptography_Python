#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#define  mixsize 100

void main()
{
	int p=5,q=7,i,n=35,euler,c,d,e=5,count;//euler为欧拉函数，d为私钥，e为公钥 
	int int_plaintext[mixsize];
	int int_ciphertext[mixsize];
	char char_plaintext[mixsize];
	char s;
	euler=(p-1)*(q-1);
	//找到私钥d 
	for(d=2;;d++)
	{
		if((d*e-1)%euler==0) break;
	}
	printf("d=%d\n",d);
	
	//输入明文 
	printf("请输入明文：\n");
	scanf("%c",&s);
	for(i=0;i<mixsize&&s!='\n';i++)
	{
		char_plaintext[i]=s;
		scanf("%c",&s);
		count++;//检测输入个数
	}
	for(i=0;i<count;i++) int_plaintext[i]=char_plaintext[i]-'a'+1;////字母转为码值 	
	printf("您要加密的明文：\n");
	for(i=0;i<count;i++)  printf("%c ",char_plaintext[i]);
	//加密
	for(i=0;i<count;i++) 
	{
		int_ciphertext[i]=fmod(pow(int_plaintext[i],e),n);
	}
	printf("\n加密后的密文:\n");
	for(i=0;i<count;i++) printf("%d ",int_ciphertext[i]);
	
	//解密
	printf("\n您要解密的密文：\n");
	for(i=0;i<count;i++)  printf("%d ",int_ciphertext[i]);
	for(i=0;i<count;i++) 
	{
		int_plaintext[i]=fmod(pow(int_ciphertext[i],d),n);
		char_plaintext[i]=int_plaintext[i]+'a'-1;
	}
	printf("\n解密后的明文:\n");
	for(i=0;i<count;i++) printf("%c ",char_plaintext[i]);

}

