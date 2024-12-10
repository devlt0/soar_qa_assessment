
import random
import string
from time import sleep
from locust import HttpUser, task, between, events


class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Random wait time between 1 and 3 seconds
    host = "http://localhost:5000"

    def random_string(self, length):
        return ''.join(random.choices(string.ascii_letters, k=length))

    def register(self, full_name:str="",
                       user_name:str="",
                       email:str="",
                       password:str="",
                       phone:str=""):
        phone = phone if phone else f"+1{random.randint(1000000000, 9999999999)}"

        # POST request to /client_registeration with form data
        response = self.client.post("/client_registeration", data={
            "fullName": full_name,
            "userName": user_name,
            "email": email,
            "password": password,
            "phone": phone
        })

        if response.status_code == 200:
            print(f"Registered User: {email}")
        else:
            print(f"Failed Registration for: {email}")


    @task(6)
    def register_valid_user(self):
        full_name = self.random_string(10)
        user_name = self.random_string(8)
        email     = f"{self.random_string(5)}@test.com"
        password  = "Test@1234"
        phone     = f"+1{random.randint(1000000000, 9999999999)}"

        response = self.client.post("/client_registeration", data={
            "fullName": full_name,
            "userName": user_name,
            "email": email,
            "password": password,
            "phone": phone
        })

        if response.status_code == 200:
            print(f"Registered User: {email}")
        else:
            print(f"Failed Registration for: {email}")


    @task(1) # will run 1/3 as oft as valid user
    def register_invalid_user(self):
        full_name = ""
        user_name = ""
        email     = ""
        password  = ""
        phone     = ""

        response = self.client.post("/client_registeration", data={
            "fullName": full_name,
            "userName": user_name,
            "email": email,
            "password": password,
            "phone": phone
        })

        if response.status_code == 200:
            print(f"Registered User: {email}")
        else:
            print(f"Failed Registration for: {email}")


    @task(1)
    def invalid_login_random_credentials(self):
        user_name = self.random_string(8)
        email     = f"{self.random_string(8)}@test.com"
        password  = self.random_string(8)

        response  = self.client.post("/client_login", data={
            "userName" : user_name,
            "email"    : email,
            "password" : password
        })

        if response.status_code == 200 and 'token' in response.json():
            print(f"Login Successful for {email}")
        else:
            print(f"Failed Login for {email}")


    @task(1)
    def invalid_login_empty_credentials(self):
        user_name = ""
        email     = ""
        password  = ""

        response  = self.client.post("/client_login", data={
            "userName" : user_name,
            "email"    : email,
            "password" : password
        })

        if response.status_code == 200 and 'token' in response.json():
            print(f"Login Successful for {email}")
        else:
            print(f"Failed Login for {email}")


    @task(6) # valid scenario should run 3x times as combined invalid scenarios by task weighting (6 vs 1+1)
    def valid_login(self):
        valid_uname = self.random_string(8)
        valid_email = f"{self.random_string(8)}@test.com"
        valid_pword = self.random_string(8)

        self.register(full_name = self.random_string(10),
                      user_name = valid_uname,
                      email     = valid_email,
                      password  = valid_pword,
                      phone     = f"1{random.randint(1000000000, 9999999999)}" )

        response = self.client.post("/client_login", data={
            "userName" : valid_uname,
            "email"    : valid_email,
            "password" : valid_pword
        })

        if response.status_code == 200 and 'token' in response.json():
            print(f"Login Successful for {valid_email}")
        else:
            print(f"Failed Login for {valid_email}")
