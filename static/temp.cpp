#include<bits/stdc++.h>
int main(){
    char c;
    FILE* f=fopen("whitepages.txt");
    while(fscanf(f,"%c",&c), c!=EOF){
        printf("%d ",c);
    }
}