#include "powerUtility.h"

#define MAX_BITS 1000

// Function Prototypes
void binary(long decimalValue, int bits[], int &bitCount);

// Implements the repeated squaring algorithm
long powerModN(long base, long exponent, long modulus)
{
    int bits[MAX_BITS];
    int bitCount;

    binary(exponent, bits, bitCount);

    long result = 1;
    long power = base % modulus;

    for (int i = 0; i < bitCount; i++)
    {
        if (bits[i] == 1)
        {
            result = (result * power) % modulus;
        }
        power = (power * power) % modulus;
    }

    return result;
}

// Converts the exponent into its binary number representation
void binary(long decimalValue, int bits[], int &bitCount)
{
    bitCount = 0;

    while (decimalValue > 0)
    {
        bits[bitCount++] = decimalValue % 2;
        decimalValue /= 2;
    }
}
// g++ program5-driver.cpp student5.cpp -o a.exe
// a.exe 94 7 209
