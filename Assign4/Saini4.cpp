///////////////////////////////////////////////////////////////////
// Student name: Prashikshit Saini
// Course: COSC 4553 - Information Security
// Assignment: Assignment #5 - RSA Key Generation
// File name: Saini4.cpp
// Purpose: Defines the functions that generate the RSA public and
//          private keys
// Limitations: Assumes valid prime inputs from the user.
// Development Computer: Lenovo Legion 5 Pro
// Operating System: Windows 11 x64
// Integrated Development Environment (IDE): Visual Studio Code
// Compiler: GNU g++
// Build Directions: g++ program4-driver.cpp Saini4.cpp -o rsa_keys
// Operational Status: Passed test cases provided in the assignment sample-run.txt.
///////////////////////////////////////////////////////////////////

#include <iostream>
#include "RSA_Keys.h"

using namespace std;

// Helper function to compute the greatest common divisor (GCD)
static int gcd(int a, int b)
{
    while (b != 0)
    {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

static int relativelyPrime(int phi)
{
    for (int e = 2; e < phi; e++)
    {
        if (gcd(e, phi) == 1)
        {
            return e;
        }
    }
    return -1; // Should not occur with valid primes
}

// Extended Euclidean Algorithm to find the multiplicative inverse
static int extendedGCD(int a, int b, int &x, int &y)
{
    if (b == 0)
    {
        x = 1;
        y = 0;
        return a;
    }
    int x1, y1;
    int gcd = extendedGCD(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return gcd;
}

// Helper function to compute the multiplicative inverse modulo 'modulus'
static int inverse(int a, int modulus)
{
    int x, y;
    int g = extendedGCD(a, modulus, x, y);
    if (g != 1)
    {
        return -1; // Inverse doesn't exist, but should not happen here
    }
    else
    {
        // Ensure the result is positive
        return (x % modulus + modulus) % modulus;
    }
}

void generateKeys(int primeA, int primeB, int &encryptionExponent,
                  int &decryptionExponent)
{
    int phi = (primeA - 1) * (primeB - 1);
    encryptionExponent = relativelyPrime(phi);
    decryptionExponent = inverse(encryptionExponent, phi);
}