int main() {

    int a = 5;
    int b = 10;
    int c = 15;
    int d = 20;
    int e = 25;

    if(a > 5 || b > 10 || c > 50 || (a==10 && b==5)) {
        return 1;
    }

    if((a && b) || (c && d) || e) {
        return 2;
    }

    return 0;
}