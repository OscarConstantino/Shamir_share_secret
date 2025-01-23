#!/usr/bin/env python3
# The program is meant to show a simple implementation of the Shamir algorithm which shares a secret and can be recovered with 
# an specific number of the shares.
# It is important to select a big prime number to perfrom the operations correctly.
# This program is limitaded to a prime number of size 2**4096 + 1761, if a larger number is required, it is necessary to 
# calculate a big prime number and set it manually.

#The program requires the next packages:
    # os
    # math
# The program uses the urandom package to generate random numbers directly from the OS.
# The sqrt function is used during the prime number verification.
from os import urandom
from math import sqrt

class Shamir:
    # Shamir class used to perform the secret sharing and secret recovery.
    #Variables:
        # _PRIME an large prime number used in case of a large secret number is set
    #Methods:
        # get_values -> method to set the values to calculate the secret sharing opeartions.
        # generate_prime_number         ->  method to generate a prime number used for the secret sharing operations.
        # check_prime -> method         -> method that validates if the number given is a valid prime number.
        # polynomial_construction       -> method that generates the polynomial function for the secret sharing operaitons.
        # random_number_coeff_selection -> method used to randomly choose a coefficient for the secret sharing operaitons.
        # points_generation             -> method that calculates the shares based on the polinomial constructed.
        # lagrange_basis_calculation    -> method that calculate the lagrange basis to generate the values to recover the secret.
        # reconstruct_secret_shamir     -> method that recovers the secret based on the values given
    
    _PRIME = 2**4096 + 1761

    def __init__(self):
        # Shamir constructor method use to initialize the class with empty values.
        # Params:
            # -
        # Returns:
            # -
        # Description:
            # This method sets empty lists to the points and polynomial variables. This is done to avoid problems if the class is instanced multiple times.
        Shamir.points = []
        Shamir.polynomial = []

    def get_values(self, secret, n_parts, k_parts, prime_number = _PRIME):
        # get_values method use to set the values for the secret sharing operation.
        # Params:
            # secret        -> a string value that will be used as the secret that wanted to be shared
            # n_parts       -> a string value that will be used as the number of parts that the secret will be divided 
            # k_parts       -> a string value that will be used as the minimum parts to recover the secret
            # prime_number  -> an integer value that will set a prime value in case the value is too large
        # Returns:
            #  boolean  -> True
        # Description:
            # It validates that the parameters are digits and that the number of parts are smaller that the required numbers to recover.
            # After the validation and setting the correct values 
        if prime_number != Shamir._PRIME:
            Shamir._PRIME = prime_number
        if secret.isdigit() and n_parts.isdigit() and k_parts.isdigit():
            Shamir.secret, Shamir.n_parts, k_parts = int(secret), int(n_parts), int(k_parts)
            Shamir.prime_number = Shamir.generate_prime_number(self,5)
        else:
            raise TypeError("The secret and the parts that will be devided must be integer numbers")
        if k_parts > Shamir.n_parts or k_parts == 1:
            raise ArithmeticError("The minimum number to recover must be lower or equal than the nummber of pieces and should be greater than 1")
        else:
            Shamir.k_parts = k_parts
        # Generating the polynomial
        Shamir.polynomial_construction(self)
        # Generating the points from the constructed polynomial
        Shamir.points_generation(self)
        return True
        
    def generate_prime_number(self, size):
        # generate_prime_number method use to generate a valid prime number for the operations.
        # Params:
            # size  -> an ineger value used to 
        # Returns:
            #  integer  -> valid_prime_number
        # Description:
            # It validates if the size of the number is too large to be calculated, if it does it will use a static prime value or use a manually 
            # set large prime number. In case is not large enough it will raise a ValueError exception.
        if size == 7:
            # If the number is too large to be generated the program will use a given large prime number.
            if Shamir.secret < Shamir._PRIME:
                return Shamir._PRIME
            else:
                raise ValueError("The secret number is too large for the given prime number...")
        valid_prime_number = int.from_bytes(urandom(size))
        if valid_prime_number < Shamir.secret and size:
            # If the number is too large, we will try with a new big random number.
            return Shamir.generate_prime_number(self, size + 1)
        if not Shamir.check_prime(self, valid_prime_number):
            return Shamir.generate_prime_number(self, size)
        return valid_prime_number

    def check_prime(self, p):
    #check_prime function used for verifying if the p parameter is actually a prime number
    #Parameters:
        # p -> It's an integer that will be verified if it's prime or not
    #Description:
        # If p is even it can't be a primer number.
        # If p is 2 or 3 it is a prime number, no calculations needed.
        # If p is even it can't be a primer number.
        # The iterations are shortened by using the integer value of the sqrt of the number plus one and checking only odd numbers.
        # If there is another number that has a zero module then it is not a prime number, since it is divisible by another number than itself.

        if p==2 or p==3: return True
        if p%2==0: return False 
        for i in range(3, int(sqrt(p))+1, 2): 
            if p%i==0: 
                return False
        return True

    def polynomial_construction(self):
        # polynomial_construction method use to generate a polynomial function with the correct structure and size to calculate the shares and recover the secret
        # with the given parameters
        # Params:
            # -
        # Returns:
            # -
        # Description:
            #  The method uses the secret as the first parameters of the polynomial, then makes k_parts - 1 parts with random coefficients 
            # smaller that the prime number
        Shamir.polynomial = [Shamir.secret] + [ Shamir.random_number_coeff_selection(self, 5, 1) for _ in range(Shamir.k_parts - 1) ]
    
    def random_number_coeff_selection(self, size, iteration):
        # random_number_coeff_selection method use to generate a random coefficient with a valid size
        # with the given parameters
        # Params:
            # size      -> an integer value that will set the size of the random number
            # iteration -> an integer value that will initialize the iteration
        # Returns:
            # integer random_coeff
        # Description:
            # The random number is genrated randomly by the OS, the value is verified if it is not 0 or if the value is greater than the prime number and 
            # if it does a new value will be calculated.
        random_coeff = int.from_bytes(urandom(size))
        if random_coeff == 0:
            return Shamir.random_number_coeff_selection(self, size, iteration+1)
        if random_coeff < (Shamir.prime_number - 1):
            return random_coeff
        else:
            # If after five iterations the size is still too big the random parameter will be reduced.
            if iteration % 5 != 0 or size == 1:
                return Shamir.random_number_coeff_selection(self, size, iteration+1)
            else:
                return Shamir.random_number_coeff_selection(self, size-1, iteration+1)

    def points_generation(self):
        # points_generation method use to generate the points or the parts of the secret that will be shared.
        # with the given parameters
        # Params:
            # -
        # Returns:
            # -
        # Description:
            # Each part is evaluated with the generated coefficients and the positon in which it is calculated.
        for n in range(1, Shamir.n_parts + 1):
            result=0
            for power, coeff in enumerate(Shamir.polynomial):
                # The operations should retrun the sum of all of the coefficients evaluated in their positon
                # Then the module of the prime should also be applied to the result sum
                result = (result + coeff * pow(n, power)) % Shamir.prime_number
            # The points are stored as a tuple with the postion and the value.
            Shamir.points.append((n,result))

    def lagrange_basis_calculation(self, x_shares, iter_position, p_number):
        # lagrange_basis_calculation method use to calculate the lagrange basis polynomial using the given parameters
        # Params:
            # x_shares      -> a list with the point postions that were chosen to recover the secret
            # iter_position -> an integer value with the current position in the iteration of the calculation
            # p_number      -> an integer value with the prime number used during the secret sharing
        # Returns:
            # integer   ->  lagrange_base
        # Description:
            # The lagrange basis calculation is calculated using the polinomial postions and a multiplication series
            # of the postion evaluated in a x = 0. The calculation uses the module of the prime number for more accuracy 
            # in the operation, specially for big numbers.   
        lagrange_base = 1   # The multiplication base is intialized in 1
        x_j = x_shares[iter_position]   # The current position is selected from the points recovered
        for m, x_m in enumerate(x_shares):
            # The multiplication is only applied when the position is different from the one in the current iteration.
            if m != iter_position:
                # The numerator operation should be x - x_m, consider that the operation is evaluated 
                # when x = 0, then the module is applied for more security on the operations.
                numerator = (0 - x_m) % p_number
                # The denominator should be diference between the current position and the positions 
                # in the points recovered a module is also applied for security in the operations.
                denominator = (x_j - x_m) % p_number
                # The lagrange basis is the multiplication series of the division between the calculated numerator and 
                # the denominator. In this case the denominator is calculated by making the inverse of the denominator
                # value, then a module of the prime number is also applied for security measures.
                lagrange_base = (lagrange_base * numerator * pow(denominator, -1, p_number)) % p_number
        return lagrange_base

    def reconstruct_secret_shamir(self, min_points, p_number):
        # reconstruct_secret_shamir method use to calculate the secret with the given points and prime number.
        # Params:
            # min_points    -> a list with the minimum points to recover the secret number
            # p_number      -> an integer value with the prime number used in the secret sharing operation
        # Returns:
            # integer   ->  secret
        # Description:
            # This method perfomrs the sum series using the lagrange base and the points value.
        x_shares, y_shares = zip(*min_points) # The points are splited between the positions (x_shares) and the values (y_shares)
        secret = 0  # The secret is initialized as zero for the sum series that will be performed later
        # The series will be applied for every point, if less points are used or if invalid points 
        # are used the secret will not be recovered
        for position in range(len(min_points)):
            lagrange_base = Shamir.lagrange_basis_calculation(self, x_shares, position, p_number) # The lagrange value is calcualted for every point
            secret = (secret + y_shares[position] * lagrange_base) % p_number # The sum of the value of the point times the current lagrange base.
        return secret