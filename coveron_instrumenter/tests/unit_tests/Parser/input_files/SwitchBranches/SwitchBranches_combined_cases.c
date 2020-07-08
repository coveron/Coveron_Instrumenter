int main()
{
    int a = 0;
    int b = 0;

    switch (a)
    {
    case -1:
        b = -1;
        break;
    case 0:
        b = 1;
    case 1:
        b = 2;
        break;
    case 2:
    case 3:
        b = 5;
    default:
        b = 3;
    }

    switch (a)
    {
    default:
    case 10:
        b = 10;
        break;
    }

    return 0;
}