///////////////////////////////////////////////////////////////////
// Student name: Instructor
// Course: COSC 4553 - Information Security
// Assignment: Assignment #5 - RSA Key Generation
// File name: program5-driver.cpp  
// Purpose: Provides the driver that calls functions to generate 
//          the RSA public and private keys and then test those keys
//
// Limitations: None known
// 
// Development Computer: Dell  
// Operating System: Windows XP 
// Integrated Development Environment (IDE): None
// Compiler:  GNU g++
// Build Directions: g++ program5-driver.cpp student5.cpp
// Operational Status: All requirements are met
///////////////////////////////////////////////////////////////////

#include <iostream>
#include <math.h>
#include "RSA_Keys.h"

using namespace std;


// Function Prototypes
void displayUsageMessage(void);
void testKeyGeneration(int primeA, int primeB, int encryptionExponent, 
                       int decryptionExponent);
void testEncryptionAndDecryption(int primeA, int primeB, int encryptionExponent, 
                                 int decryptionExponent);


// ##################################################################
int main(int argc, char *argv[])
{
int largePrimeA;
int largePrimeB;
int encryptionExponent;
int decryptionExponent;

if (argc == 3)
   {
   largePrimeA = atoi(argv[1]);
   largePrimeB = atoi(argv[2]);

   generateKeys(largePrimeA, largePrimeB, encryptionExponent, decryptionExponent);

   testKeyGeneration(largePrimeA, largePrimeB, encryptionExponent, decryptionExponent);

   testEncryptionAndDecryption(largePrimeA, largePrimeB, encryptionExponent, decryptionExponent);

   return 0;
   } // End if

else
   {
   displayUsageMessage();
   return 1;
   } // End else

return 0;
} // End main


// ##################################################################
void displayUsageMessage(void)
{
cout << endl;
cout << "Usage: a.exe <prime number> <prime number>" << endl; 
cout << endl;
} // End displayUsageMessage


// ##################################################################
void testKeyGeneration(int primeA, int primeB, int encryptionExponent, 
                       int decryptionExponent)
{
int modulusN;
int phiProduct;
int result;

// Display and test the resulting keys
modulusN = primeA * primeB;
phiProduct = (primeA - 1) * (primeB - 1);
cout << endl;
cout << "Public key : (" << modulusN << ", " << encryptionExponent << ")" <<endl;
cout << "Private key: " << decryptionExponent << endl << endl;

cout << endl;
cout << "Test the key generation:" << endl << endl;

cout << "   (e * d) mod (p - 1)(q - 1) = 1 mod (p - 1)(q - 1)" << endl << endl;

cout << "   (" << encryptionExponent << " * " << decryptionExponent 
     << ") mod (" << primeA << " - 1)(" << primeB 
     << " - 1) = 1 mod (" << primeA << " - 1)(" << primeB 
     << " - 1)" << endl << endl;

cout << "   " << (encryptionExponent * decryptionExponent) << " mod " 
              << phiProduct << " = " 
              << "1 mod " << phiProduct << endl << endl;

result = (encryptionExponent * decryptionExponent) % phiProduct;

cout << "   " << result << " mod " 
              << phiProduct << " = " 
              << "1 mod " << phiProduct << endl;

cout << endl;
cout << "Test result: ";
if (result == 1)
   cout << "PASSED" << endl;
else 
   cout << "FAILED" << endl;

} // End testKeyGeneration


// ##################################################################
void testEncryptionAndDecryption(int primeA, int primeB, int encryptionExponent, 
                                 int decryptionExponent)
{
int modulusN;
long raisedBase;
long plainValue = 15;
long cipherValue;
long decipherValue;

cout << endl << endl;
cout << "Test the encryption and decryption:" << endl << endl;

modulusN = primeA * primeB;

cout << "   Plain value    : " << plainValue << endl;

raisedBase = (long) pow(plainValue, encryptionExponent);

cipherValue = raisedBase % modulusN;

cout << "   Cipher value   : " << raisedBase
     << " mod " << modulusN << " = " << cipherValue << endl;

raisedBase = (long) pow(cipherValue, decryptionExponent);

decipherValue = raisedBase % modulusN;

cout << "   Decipher value : " << raisedBase
     << " mod " << modulusN << " = " << decipherValue << endl;

cout << endl;
cout << "Test result: ";
if (plainValue == decipherValue)
   cout << "PASSED" << endl;
else 
   cout << "FAILED" << endl;

} // End testEncryptionAndDecryption



