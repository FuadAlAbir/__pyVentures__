"""
-------------------------------
    I N T R O D U C T I O N
-------------------------------
Author:         Fuad Al Abir
Date:           December 26, 2018
File name:      trailing_zeroes_of_factorial.py
Objective:      is to find the trailing zeroes of factorial of numbers
Problem Source: To derive a formula of the trailing zeroes comes with the factorial of a number

-------------------------------------
    I M P O R T E D   M O D U L E
-------------------------------------
Header: math
Reason: to get factorial() values

-------------------------------------------------
    U S E R   D E F I N E D   F U N C T I O N
-------------------------------------------------

Function: _powered_by(a)
Reason: 5 based logarithm of a
Function: _trailing_zeroes(a)
Reason: returns the number of trailing zeroes of a
        by the recursive formula
        w/o calculating the factorial of a
Function: _trailing_zeroes_in_range(a, b)
Reason: prints the number of trailing zeroes in range a to b by two methods

---------------------------------
    S A M P L E   O U T P U T
---------------------------------
15620! has 3900 = 3900 zeroes.
15621! has 3900 = 3900 zeroes.
15622! has 3900 = 3900 zeroes.
15623! has 3900 = 3900 zeroes.
15624! has 3900 = 3900 zeroes.
15625! has 3906 = 3906 zeroes.
15626! has 3906 = 3906 zeroes.
15627! has 3906 = 3906 zeroes.
15628! has 3906 = 3906 zeroes.
15629! has 3906 = 3906 zeroes.

--------------------------
    Recursive Formula:
--------------------------
                        0                                   if p = 0
_tailing_zeroes(n) =    n//5                                if p = 1        
                        n//5 + _tailing_zeroes(n//5)        if p > 1

                        here,   p       = 5 based log of n
                                n//5    = n's floor division by 5
"""

import math

def trailing_zeros(longint):
    manipulandum = str(longint)
    return len(manipulandum)-len(manipulandum.rstrip('0'))

# 5 based logarithm
def _powered_by(a):
    c = 0
    while a >= 5:
        a /= 5
        c += 1
    return c

def _trailing_zeroes(longint):
    p = _powered_by(longint)
    if (p == 0): return 0
    elif (p == 1): return longint//5
    else: return longint//5 + _trailing_zeroes(longint//5)
    
def _trailing_zeroes_in_range(a, b):
    for x in range(a, b):
        fact = math.factorial(x)
        print(x, end="")
        print("! has", _trailing_zeroes(x), "=", trailing_zeros(fact), "zeroes.")

_trailing_zeroes_in_range(5 ** 6 - 5, 5 ** 6 + 5)
