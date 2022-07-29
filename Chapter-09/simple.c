include <studio.h>

void checkPass(init x) {
    if(x == 7857){
        printf("Access Granted");
    }else{
        printf("Access Denied")
    }
}

int main(int argc, char *argv[]) {
    int x = 0;
    printf("Enter the password:  ");
    scanf("%d", &x);
    checkPass(x);
}
