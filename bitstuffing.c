#include <stdio.h>
#include <string.h>

int main()
{
    char ch, arr[100], fs[100] = "", t[100] = "";
    int counter = 0, j = 0, i = 0;

    printf("Enter the bit string: ");
    scanf("%s", arr);

    strcat(fs, "01111110-");

    if (strlen(arr) < 5)
    {
        strcat(fs, arr);
        strcat(fs, "-01111110");
        printf("The bits after stuffing:\n%s", fs);
    }
    else
    {
        while ((ch = arr[j]) != '\0')
        {
            if (ch == '1')
                ++counter;
            else
                counter = 0;

            t[i++] = ch;

            if (counter == 5)
            {
                t[i++] = '0';
                counter = 0;
            }
            j++;
        }
        t[i] = '\0';
        strcat(t, "-01111110");
        strcat(fs, t);
        printf("The bits after stuffing:\n%s", fs);
    }

    return 0;
}
