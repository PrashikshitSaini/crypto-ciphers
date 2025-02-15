///////////////////////////////////////////////////////////////////
// Student name: Instructor
// Course: COSC 4553 - Information Security
// Assignment: Assignment #5 - RSA Key Generation
// File name: RSA_Keys.h  
// Purpose: Declares the prototype for the function that is used to 
//          generate the RSA public and private keys
//
// Limitations: None known
// 
// Development Computer: Dell  
// Operating System: Windows XP 
// Integrated Development Environment (IDE): None
// Compiler:  GNU g++
// Build Directions: See the driver module
// Operational Status: All requirements are met
///////////////////////////////////////////////////////////////////

#ifndef RSA_HEADER
#define RSA_HEADER

#include <math.h>

void generateKeys(int primeA, int primeB, int &encryptionExponent, 
                  int &decryptionExponent);

#endif

