///////////////////////////////////////////////////////////////////
// Student name: Instructor
// Course: COSC 4553 - Information Security
// Assignment: Assignment #5 - Repeated Squaring
// File name: program6-driver.cpp  
// Purpose: Provides the driver that gets the base and exponent values from
//          the user, passes the two values to the function that implements the
//          repeated squaring algorithm, and then prints the returned result 
// Limitations: None known
// Development Computer: Dell  
// Operating System: Windows 7 
// Integrated Development Environment (IDE): None
// Compiler:  GNU g++
// Build Directions: g++ program6-driver.cpp student6.cpp
// Operational Status: All requirements are met
///////////////////////////////////////////////////////////////////

#include <iostream>
#include <math.h>
#include <assert.h>
#include "powerUtility.h"

using namespace std;

// Function Prototypes
void displayUsageMessage(void);


// ##################################################################
int main(int argc, char *argv[])
{
long baseValue;
long exponentValue;
long modulusValue;
long result;

if (argc == 4)
   {
   baseValue = atoi(argv[1]);
   exponentValue = atoi(argv[2]);
   modulusValue = atoi(argv[3]);

   result = powerModN(baseValue, exponentValue, modulusValue);

   cout << endl;
   cout << "   " << baseValue << '^' << exponentValue << " mod " 
        << modulusValue << " = " << result << endl;
   cout << endl;

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
cout << "Usage: a.exe <base value> <exponent value> <modulus value>" << endl; 
cout << endl;
} // End displayUsageMessage



