int main()
{
    int a = 0;

    for (int i = 0; i < 20; a++)
    {
        if (i == 10)
        {
            continue; // include continue statement to test checkpoint marker creation for next statement
            a++;
        }
        a++;
    }

    return 0;
}