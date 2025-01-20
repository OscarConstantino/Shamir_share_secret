from os import urandom
from random import sample
from math import sqrt

class Shamir:
    secret = 0
    n_parts = 0
    k_parts = 0
    polynomial = []
    points = []
    prime_number = 2

    def __init__(self):
        #Validating that secret is an integer
        Shamir.points = []
        Shamir.polynomial = []

    def get_values(self, secret, n_parts, k_parts):
        if secret.isdigit() and n_parts.isdigit() and k_parts.isdigit():
            Shamir.secret, Shamir.n_parts, k_parts = int(secret), int(n_parts), int(k_parts)
            Shamir.prime_number = Shamir.generate_prime_number(self,5)
        else:
            raise TypeError("The secret and the parts that will be devided must be integer numbers")
        if k_parts > Shamir.n_parts or k_parts == 1:
            raise ArithmeticError("The minimum number to recover must be lower or equal than the nummber of pieces and should be greater than 1")
        else:
            Shamir.k_parts = k_parts
        Shamir.polynomial_construction(self)
        Shamir.points_generation(self)
        
    def generate_prime_number(self, size):
        random_number = int.from_bytes(urandom(size))
        if random_number < Shamir.secret:
            return Shamir.generate_larger_prime_number(self, size + 1)
        if not Shamir.check_prime(self, random_number):
            return Shamir.generate_prime_number(self, size)
        return random_number

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
        Shamir.polynomial = [Shamir.secret] + [ Shamir.random_number_coeff_selection(self, 5, 1) for _ in range(Shamir.k_parts - 1) ]
    
    def random_number_coeff_selection(self, size, iteration):
        random_number = int.from_bytes(urandom(size))
        if random_number == 0:
            return Shamir.random_number_coeff_selection(self, size, iteration+1)
        if random_number < (Shamir.prime_number - 1):
            return random_number
        else:
            if iteration % 3 != 0 or size == 1:
                return Shamir.random_number_coeff_selection(self, size, iteration+1)
            else:
                return Shamir.random_number_coeff_selection(self, size-1, iteration+1)

    def points_generation(self):
        for n in range(1, Shamir.n_parts + 1):
            result=0
            for power, coeff in enumerate(Shamir.polynomial):
                result = (result + coeff * pow(n, power, Shamir.prime_number)) % Shamir.prime_number
            Shamir.points.append((n,result))

    def modular_inverse(self, a, p):
        return pow(a, -1, p)

    def lagrange_basis_calculation(self, x_shares, j, p_number):
        lagrange_base = 1
        x_j = x_shares[j]
        for m, x_m in enumerate(x_shares):
            if m != j:
                numerator = (0 - x_m) % p_number
                denominator = (x_j - x_m) % p_number
                lagrange_base = (lagrange_base * numerator * Shamir.modular_inverse(self, denominator, p_number)) % p_number
        return lagrange_base

    def reconstruct_secret_shamir(self, min_points, p_number):
        x_shares, y_shares = zip(*min_points)
        secret = 0
        for j in range(len(min_points)):
            l_b = Shamir.lagrange_basis_calculation(self, x_shares, j, p_number)
            secret = (secret + y_shares[j] * l_b) % p_number
        return secret