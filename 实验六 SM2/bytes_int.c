#include<stdio.h>
#include<stdlib.h>
#include<math.h>
typedef   signed          char uint8_t;
typedef   signed short     int uint16_t;
typedef   signed           int uint32_t;
typedef   signed      int/*__INT64*/  uint64_t;
uint64_t ArrayToVariable(uint8_t *Array, uint8_t Length);
void Variable16ToArray(uint8_t *Array, uint32_t Variable);
void Variable32ToArray(uint8_t *Array, uint32_t Variable);
void Variable64ToArray(uint8_t *Array, uint64_t Variable);

void main()
{
	int i;
	uint8_t Array[100];
	uint32_t Variable=0000000000000001;
	Variable16ToArray(Array, Variable);//功能描述: 将16位整型数据转换为2字节
	for(i=0;i<2;i++) printf("%c ",Array[i]);
}

uint64_t ArrayToVariable(uint8_t *Array, uint8_t Length)
{
	uint64_t Variable = 0;
	
	if(Length == 2)
	{
		Variable = (((uint16_t)Array[0] << 8)  + ((uint16_t)Array[1]));
	}
	else if(Length == 4)
	{
		Variable = (((uint32_t)Array[0] << 24) + ((uint32_t)Array[1] << 16) 
				  + ((uint32_t)Array[2] << 8)  + ((uint32_t)Array[3]));
	}
	else if(Length == 8)
	{
		Variable = (((uint64_t)Array[0] << 56) + ((uint64_t)Array[1] << 48) 
		          + ((uint64_t)Array[2] << 40) + ((uint64_t)Array[3] << 32) 
		          + ((uint64_t)Array[4] << 24) + ((uint64_t)Array[5] << 16) 
				  + ((uint64_t)Array[6] << 8)  + ((uint64_t)Array[7]));
	}
	return Variable;
}

/***************************
函数名:   Variable16ToArray
功能描述: 将16位整型数据转换为2字节
参数：    Variable:待转换的16位整型数据 
		 Array:转换后的2字节数组
***************************/
void Variable16ToArray(uint8_t *Array, uint32_t Variable)
{
	*(Array)     = (uint8_t)(Variable >> 8);
	*(Array + 1) = (uint8_t)(Variable);
}

/***************************
函数名:   Variable32ToArray
功能描述: 将32位整型数据转换为4字节
参数：    Variable:待转换的32位整型数据 
		 Array:转换后的4字节数组
***************************/
void Variable32ToArray(uint8_t *Array, uint32_t Variable)
{
	*(Array)     = (uint8_t)(Variable >> 24);
	*(Array + 1) = (uint8_t)(Variable >> 16);
	*(Array + 2) = (uint8_t)(Variable >> 8);
	*(Array + 3) = (uint8_t)(Variable);
}

/***************************
函数名:   Variable64ToArray
功能描述: 将64位整型数据转换为8字节
参数：    Variable:待转换的64位整型数据 
		 Array:转换后的8字节数组
***************************/
void Variable64ToArray(uint8_t *Array, uint64_t Variable)
{
	*(Array) 	 = (uint8_t)(Variable >> 56);
	*(Array + 1) = (uint8_t)(Variable >> 48);
	*(Array + 2) = (uint8_t)(Variable >> 40);
	*(Array + 3) = (uint8_t)(Variable >> 32);
	*(Array + 4) = (uint8_t)(Variable >> 24);
	*(Array + 5) = (uint8_t)(Variable >> 16);
	*(Array + 6) = (uint8_t)(Variable >> 8);
	*(Array + 7) = (uint8_t)(Variable);
}

