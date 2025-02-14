from locust import HttpUser, task, between
import random
import string

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Random wait time between 1 and 3 seconds

    def on_start(self):
        """This is run before any task is executed"""
        self.token = self.login()


    @task(1)
    def register(self):
        full_name = self.random_string(10)
        user_name = self.random_string(8)
        email = f"{self.random_string(5)}@test.com"
        password = "Test@1234"
        phone = f"+1{random.randint(1000000000, 9999999999)}"

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


    @task(2)
    def login(self):
        # For login, we can reuse some of the user details from registration, or hardcode test data
        email = "testuser@test.com"  # Replace with a valid registered email or mock one
        user_name = "testuser"       # Replace with a valid registered username or mock one
        password = "Test@1234"       # A valid password

        # POST request to /client_login with form data
        response = self.client.post("/client_login", data={
            "userName": user_name,
            "email": email,
            "password": password
        })

        if response.status_code == 200 and 'token' in response.json():
            print(f"Login Successful for {email}")
        else:
            print(f"Failed Login for {email}")

    def random_string(self, length):
        """Generate a random string of letters and digits."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

