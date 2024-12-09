from locust import HttpUser, task, between
import random
import string

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Random wait time between 1 and 3 seconds


    @task(3)
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

    def random_string(self, length):
        """Generate a random string of letters and digits."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))



# locust -f load_test_client_register.py --host=http://127.0.0.1:5000 --csv=locust_results  --html=locust_report.html --users 10 --spawn-rate 1 --run-time 5m
# go to http://127.0.0.1:5000 - click start
# note: test duration was only 5min for sake of time, otherwise would realistically run for 30min-1hr and still run 3x times to ensure consistent results