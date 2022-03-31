//write a program to check if number is odd or even using command line argument
#include<stdio.h>
int main(int argc, char *argv[])
{
    int num;
    num = atoi(argv[1]);
    if(num%2==0)
    {
        printf("%d is even\n",num);
    }
    else
    {
        printf("%d is odd\n",num);
    }
    return 0;
}