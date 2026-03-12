#include<stdio.h>
#include<stdlib.h>
#include<time.h>
typedef struct tongyushi{
	int val;
	int mod;
}tys;

int ExEuclid(int f,int d){
 	int res,x0=1,x1=0,x2=f;
	int y0=0,y1=1,y2=d;
 	int t1,t2,t0,Q;
 	while(1){
		if(y2==0){
			res=x2;
			break;
		}
		if(y2==1){
			res=y2;
			break;
		}
		Q=x2/y2;
		t0=x0-Q*y0;
		t1=x1-Q*y1;
		t2=x2-Q*y2;
		x0=y0;
		x1=y1;
		x2=y2;
		y0=t0;
		y1=t1;		
		y2=t2;
		
	}
	return res;
 } 
 
int inverse(int f,int d){
 	int res,x0=1,x1=0,x2=f;
	int y0=0,y1=1,y2=d;
 	int t1,t2,t0,Q;
 	//	if(y2==0){
 		//	res=x2;
 			//break;
		 //}
	//	if(y2==1){
	//		res=y1;
	//		break;
	//	}
		do{
		Q=x2/y2;
//		printf("Q是%d\n",Q);
		t0=x0-Q*y0;
	//	printf("d是%d\n",d);
		t1=x1-Q*y1;
	//	printf("d是%d\n",d);
		t2=x2-Q*y2;
	//	printf("d是%d\n",d);
		x0=y0;
	//	printf("x0是%d\n",x0);
		x1=y1;
	//	printf("x1是%d\n",x1);
		x2=y2;
	//	printf("x2是%d\n",x2);
		y0=t0;
	//	printf("y0是%d\n",y0);
		y1=t1;		
	//	printf("y1是%d\n",y1);
		y2=t2;
	//	printf("y2是%d\n",y2);
		}while(y2!=1);
		res=y1;
		
	return res;
 } 
tys *CRT(tys t[]){
	int numsize=2;
	tys ni[2];
	int i,M=1;
	for(i=0;i<numsize;i++){
		M*=t[i].mod;
	}
//	printf("M==%d",M);
	for(i=0;i<numsize;i++){
		ni[i].val=M/t[i].mod;
		ni[i].mod=inverse(t[i].mod,ni[i].val);
	}
	tys *p=(tys*)malloc(sizeof(tys));
	p->mod=M;
	p->val=0;
	for(i=0;i<numsize;i++){
		p->val=p->val+(ni[i].val*ni[i].mod)*t[i].val;
	}
	p->val=((p->val % p->mod)+p->mod)%p->mod;
	return p;
}

int MillerRabin(int n){
	int s=0,g=n-1,i,c,a,j;
	while(g&1==0){
		g=g>>1;
		s++;
	}
	srand((unsigned)time(NULL));
	for(j=0;j<10;j++){
		a=rand()%n;
		c=Mypow1(a,g,n);
		if(c==1){
			return 0;
		}
		for(i=0;i<s;i++){
			c=Mypow1(a,i*g,n);
			if(c==n-1)
				return 0;
		}
	}
	return 1;
}

int emerge(){
	int k;
	srand((unsigned int)time(NULL));
do{	
	k=rand();
	}while(MillerRabin(k)==0);
	return k;
}
int Mypow1(int m,int n,int p){
	int t=m,c = 1;
	while(n>0){
		if(n&1)c=c*t%p;
		t=t*t%p;
		n=n/2;
	}
	return c;
}

int Encrypt(int m,int e,int n){
	int k=Mypow1(m,e,n);
	return (k+n)%n;
}
	//return k%n;

int Decrypt(int d,int c,int p,int q){
	tys s[2];
	printf("d=%d\n",d);
	printf("c=%d\n",c);
	s[0].val=Mypow1(c,d,p);
//	printf("s0val=%d\n",s[0].val); 
	s[0].mod=p;
	s[1].val=Mypow1(c,d,q);
//	printf("s1val=%d\n",s[1].val);
	s[1].mod=q;
	tys *j;
	j=CRT(s);
	return j->val;
	
	//return k%n;
}
int husuemerge(int n){
	int k;
	srand((unsigned)time(NULL));
do{
	k=rand()%n;
 
}while(ExEuclid(n,k)!=1);
	return k;
}

void RSA(int m){
	int p,q,Fin,e,d,n;
	srand((unsigned int)time(NULL));
	p=5;
	q=7;
//do{	
//	p=rand();
//	}while(MillerRabin(p)==0);
//do{	
//	q=rand();
//	}while(MillerRabin(q)==0||q==p);
//	p=emerge();
	printf("p=%d\n",p);
//	q=emerge();
	printf("q=%d\n",q);
	Fin=(p-1)*(q-1);
	printf("Fin=%d\n",Fin);	
	n=p*q;
	printf("n是%d\n",n);
	e=husuemerge(Fin);
	printf("e是%d\n",e);
	d=(inverse(Fin,e)+Fin)%Fin;
	printf("d是%d\n",d);
	printf("m是%d\n",m);
	int ct=Mypow1(m,e,n);
	printf("密文是%d\n",ct);
	int mk=Decrypt(d,ct,p,q);
	printf("明文是%d\n",mk);
	
}

int main(){
	RSA(22);
	return 0;
}
