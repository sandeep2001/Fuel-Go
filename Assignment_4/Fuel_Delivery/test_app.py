import unittest
import requests
from Fuel_Go import views
from Fuel_Go import auth
import random
import string


class MyTestCase(unittest.TestCase):
    # Ensure login behaves correctly given the correct credential
    def test_login(self):
        # Ensure that Flask was set up correctly
        response = requests.get('http://127.0.0.1:5000/loginpage')
        self.assertEqual(response.status_code, 200)

    def test_correct_login(self):
        response = requests.post('http://127.0.0.1:5000/loginpage', data={'username': 'xyz', 'password1': '12345678'})
        self.assertTrue('Logged in successfully!' in response.text)

    def test_not_an_user_login(self):
        response = requests.post('http://127.0.0.1:5000/loginpage', data={'username': 'xxx', 'password1': '12345678'})
        self.assertTrue('Username does not exist.' in response.text)

    def test_wrong_password_login(self):
        response = requests.post('http://127.0.0.1:5000/loginpage',
                                 data={'username': 'xyz', 'password1': '123456789'})
        self.assertTrue('Incorrect password, try again.' in response.text)

    def test_home(self):
        response = requests.post('http://127.0.0.1:5000/loginpage', data={'username': 'xyz', 'password1': '12345678'})
        response = requests.get('http://127.0.0.1:5000/')
        self.assertEqual(response.status_code, 200)

############################################################################################

    def test_sign_up(self):
        response = requests.get('http://127.0.0.1:5000/registration')
        self.assertEqual(response.status_code, 200)

    def test_correct_sign_up(self):
        letters = string.ascii_lowercase
        user_name = ''.join(random.choice(letters) for i in range(10))
        response = requests.post('http://127.0.0.1:5000/registration',
                                 data={'username': user_name, 'email': 'ppp@gmail.com', 'password1': '12345678',
                                       'password2': '12345678'})
        self.assertTrue('Account created!' in response.text)

    def test_exist_username_sign_up(self):
        response = requests.post('http://127.0.0.1:5000/registration',
                                 data={'username': 'xyz', 'email': 'ppp@gmail.com', 'password1': '12345678',
                                       'password2': '12345678'})
        self.assertTrue('Username already exists.' in response.text)

    def test_password_not_match_sign_up(self):
        response = requests.post('http://127.0.0.1:5000/registration',
                                 data={'username': 'aaaxxx', 'email': 'ppp@gmail.com', 'password1': '12345678',
                                       'password2': '123456789'})
        self.assertTrue('Passwords don&#39;t match.' in response.text)

    def test_password_too_short_sign_up(self):
        response = requests.post('http://127.0.0.1:5000/registration',
                                 data={'username': 'aaa', 'email': 'ppp@gmail.com', 'password1': '123',
                                       'password2': '123'})
        self.assertTrue('Password must be at least 8 characters.' in response.text)

#######################################################################################
    def test_logout(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/loginpage', data={'username': 'xyz', 'password1': '12345678'})

        response = s.get('http://127.0.0.1:5000/logout')
        self.assertTrue('Logged out successfully!' in response.text)

########################################################################################

    def test_create_profile(self):
        response = requests.get('http://127.0.0.1:5000/profilepage')
        self.assertEqual(response.status_code, 200)

    def test_post_create_profile(self):
        s = requests.Session()
        letters = string.ascii_lowercase
        user_name = ''.join(random.choice(letters) for i in range(10))
        response = s.post('http://127.0.0.1:5000/registration',
                          data={'username': user_name, 'email': 'ppp@gmail.com', 'password1': '12345678',
                                'password2': '12345678'})
        fullname = ''.join(random.choice(letters) for i in range(5))
        response = s.post('http://127.0.0.1:5000/profilepage',
                          data={'fullname': fullname, 'address1': 'ppp', 'address2': '123',
                                'city': 'acb', 'state': 'TX', 'zipcode': '7777777'})
        self.assertTrue('Profile created!' in response.text)

    def test_full_name_too_short_profile(self):
        response = requests.post('http://127.0.0.1:5000/profilepage',
                                 data={'fullname': 'x', 'address1': 'ppp', 'address2': '123',
                                       'city': 'acb', 'state': 'TX', 'zipcode': '7777777'})
        self.assertTrue('Full name must be greater than 2 and less than 50 characters.' in response.text)

    def test_address_too_short_profile(self):
        response = requests.post('http://127.0.0.1:5000/profilepage',
                                 data={'fullname': 'xmnnc', 'address1': 'p', 'address2': '123',
                                       'city': 'acb', 'state': 'TX', 'zipcode': '7777777'})
        self.assertTrue('Address must be greater than 2 and less than 100 characters.' in response.text)

    def test_city_too_short_profile(self):
        response = requests.post('http://127.0.0.1:5000/profilepage',
                                 data={'fullname': 'xmnnc', 'address1': 'pxts', 'address2': '123',
                                       'city': 'a', 'state': 'TX', 'zipcode': '7777777'})
        self.assertTrue('City must be greater than 2 and less than 100 characters.' in response.text)

    def test_state_not_two_profile(self):
        response = requests.post('http://127.0.0.1:5000/profilepage',
                                 data={'fullname': 'xmnnc', 'address1': 'pxts', 'address2': '123',
                                       'city': 'abc', 'state': 'TXMS', 'zipcode': '7777777'})
        self.assertTrue('Reselect state.' in response.text)

    def test_zipcode_not_correct_profile(self):
        response = requests.post('http://127.0.0.1:5000/profilepage',
                                 data={'fullname': 'xmnnc', 'address1': 'pxts', 'address2': '123',
                                       'city': 'abc', 'state': 'TX', 'zipcode': '77'})
        self.assertTrue('Zipcode must be greater than 5 and no more than 9 characters.' in response.text)


########################################################################################################

    def test_get_fuel_quote_form(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/loginpage', data={'username': 'xyz', 'password1': '12345678'})
        response = s.get('http://127.0.0.1:5000/fuel-quote')
        self.assertEqual(response.status_code, 200)

    def test_post_fuel_quote_form(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/loginpage', data={'username': 'xyz', 'password1': '12345678'})
        response = s.post('http://127.0.0.1:5000/fuel-quote',
                          data={'Total_Gallons_Requested': '100', 'delivery_date': '2021-07-08',
                                'delivery_Address': 'xysdgahdgsahd, FL'})
        self.assertTrue('Suggest price created!' in response.text)

    def test_first_post_fuel_quote_form(self):
        s = requests.Session()
        letters = string.ascii_lowercase
        user_name = ''.join(random.choice(letters) for i in range(10))
        response = s.post('http://127.0.0.1:5000/registration',
                          data={'username': user_name, 'email': 'ppp@gmail.com', 'password1': '12345678',
                                'password2': '12345678'})
        fullname = ''.join(random.choice(letters) for i in range(5))
        response = s.post('http://127.0.0.1:5000/profilepage',
                          data={'fullname': fullname, 'address1': 'xysdgahd', 'address2': 'gsah',
                                'city': 'xyz', 'state': 'TX', 'zipcode': '7777777'})
        response = s.post('http://127.0.0.1:5000/fuel-quote',
                          data={'Total_Gallons_Requested': '1050', 'delivery_date': '2021-07-08',
                                'delivery_Address': 'xysdgahdgsahxyz, TX'})
        self.assertTrue('Suggest price created!' in response.text)

    def test_get_fuel_quote_result(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/loginpage', data={'username': 'xyz', 'password1': '12345678'})
        s.post('http://127.0.0.1:5000/fuel-quote',
               data={'Total_Gallons_Requested': '100', 'delivery_date': '2021-07-08',
                     'delivery_Address': 'xysdgahdgsahd, FL'})

        response = s.get('http://127.0.0.1:5000/fuel-quote-result')
        self.assertEqual(response.status_code, 200)

    def test_post_fuel_quote_result(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/loginpage', data={'username': 'xyz', 'password1': '12345678'})
        s.post('http://127.0.0.1:5000/fuel-quote',
               data={'Total_Gallons_Requested': '100', 'delivery_date': '2021-07-08',
                     'delivery_Address': 'xysdgahdgsahd, FL'})

        response = s.post('http://127.0.0.1:5000/fuel-quote-result')
        self.assertTrue('Quote result added!' in response.text)

    def test_get_fuel_history(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/loginpage', data={'username': 'xyz', 'password1': '12345678'})
        response = s.get('http://127.0.0.1:5000/fuel-quote-history')
        self.assertEqual(response.status_code, 200)


###########################################################################################################

    def test_homepage(self):
        response = requests.get('http://127.0.0.1:5000/homepage')
        self.assertEqual(response.status_code, 200) 

    def test_Aboutus(self):
        response = requests.get('http://127.0.0.1:5000/Aboutus')
        self.assertEqual(response.status_code, 200)

    def test_Assignments(self):
        response = requests.get('http://127.0.0.1:5000/Assignments')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
