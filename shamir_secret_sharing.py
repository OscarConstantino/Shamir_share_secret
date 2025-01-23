#!/usr/bin/env python3
# The program is meant to test the registration_isvp.py file

# The unittest package is used to performed the test on the Shamir class and its different methods.
import unittest
import time
from random import sample
from shamir_secret_sharing import Shamir

class TestShamir(unittest.TestCase):

    def test_1_shamir(self):
        """
        Test of Shamir class sharing a secret and recovering it correctly
        """
        shamir_instance = Shamir()
        result = shamir_instance.get_values('65','4','2')
        print("----------------------")
        print("Original_value: 65")
        print("Number of shares: 4")
        print("Minimum shares: 2")
        print("**********************")
        print("Prime number used: ", shamir_instance.prime_number)
        print("Points generated: ")
        for point in shamir_instance.points:
            print("     ",point)
        time.sleep(2)
        random_points = sample(shamir_instance.points,2)
        print("Recovering secret with random points...")
        print("Selected points:")
        for point in random_points:
            print("     ",point)
        secret = shamir_instance.reconstruct_secret_shamir(random_points,shamir_instance.prime_number)
        print("Secret recovered: ", secret)
        print("----------------------")
        time.sleep(2)
        self.assertTrue(result)
    
    def test_2_shamir(self):
        """
        Test of Shamir class sharing a secret and recovering it correctly
        """
        shamir_instance = Shamir()
        result = shamir_instance.get_values('9876543211234561231313123789','7','4')
        print("----------------------")
        print("Original_value: 9876543211234561231313123789")
        print("Number of shares: 7")
        print("Minimum shares: 4")
        print("**********************")
        print("Prime number used: ", shamir_instance.prime_number)
        print("Points generated: ")
        for point in shamir_instance.points:
            print("     ",point)
        time.sleep(2)
        random_points = sample(shamir_instance.points,4)
        print("Recovering secret with random points...")
        print("Selected points:")
        for point in random_points:
            print("     ",point)
        secret = shamir_instance.reconstruct_secret_shamir(random_points,shamir_instance.prime_number)
        print("Secret recovered: ", secret)
        print("----------------------")
        time.sleep(2)
        self.assertTrue(result)

    def test_3_shamir(self):
        """
        Test of Shamir class sharing a secret and recovering it correctly
        """
        shamir_instance = Shamir()
        result = shamir_instance.get_values('9876543211234561231313123789','7','4', 2**3072 + 813)
        print("----------------------")
        print("Original_value: 9876543211234561231313123789")
        print("Number of shares: 7")
        print("Minimum shares: 4")
        print("**********************")
        print("Prime number used: ", shamir_instance.prime_number)
        print("Points generated: ")
        for point in shamir_instance.points:
            print("     ",point)
        time.sleep(2)
        random_points = sample(shamir_instance.points,4)
        print("Recovering secret with random points...")
        print("Selected points:")
        for point in random_points:
            print("     ",point)
        secret = shamir_instance.reconstruct_secret_shamir(random_points,shamir_instance.prime_number)
        print("Secret recovered: ", secret)
        print("----------------------")
        time.sleep(2)
        self.assertTrue(result)

    def test_4_shamir(self):
        """
        Test of Shamir class sharing a secret and recovering it without the minimum shares
        """
        shamir_instance = Shamir()
        result = shamir_instance.get_values('65','4','3')
        print("----------------------")
        print("Original_value: 65")
        print("Number of shares: 4")
        print("Minimum shares: 2")
        print("**********************")
        print("Prime number used: ", shamir_instance.prime_number)
        print("Points generated: ")
        for point in shamir_instance.points:
            print("     ",point)
        time.sleep(2)
        random_points = sample(shamir_instance.points,2)
        print("Recovering secret with random points...")
        print("Selected points:")
        for point in random_points:
            print("     ",point)
        secret = shamir_instance.reconstruct_secret_shamir(random_points,shamir_instance.prime_number)
        print("Secret recovered: ", secret)
        print("----------------------")
        time.sleep(2)
        self.assertTrue(result)

    def test_5_shamir(self):
        """
        Test of Shamir class sharing with a greater value for mimum shares.
        """
        shamir_instance = Shamir()
        result = shamir_instance.get_values('65','4','5')
        print("----------------------")
        print("Original_value: 65")
        print("Number of shares: 4")
        print("Minimum shares: 5")
        print("**********************")
        print("Prime number used: ", shamir_instance.prime_number)
        print("Points generated: ")
        for point in shamir_instance.points:
            print("     ",point)
        print("----------------------")
        time.sleep(2)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()