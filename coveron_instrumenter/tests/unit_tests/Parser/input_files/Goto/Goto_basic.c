int main()
{
    int a = 0;
    if (a == 0)
    {
        goto label1;
        a = a + 1;
    }
    int b = 0;
    int c = 0;

label1:
    a = a + 1;

    return 0;
}