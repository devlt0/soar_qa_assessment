
import random
import string
from time import sleep
from locust import HttpUser, task, between, events
'''
from locust.env import Environment


valid_credentials = []


def run_once_before_session():
    print("Running global setup task once before session to setup valid users")
    # generate valid users to be able to test valid login
    global valid_credentials # list of tuples (uname, email, pw) min req info for login
    environment = Environment(user_classes=[WebsiteUser])
    environment.create_local_runner()

    # Initialize the environment manually if needed
    user_handle = WebsiteUser(environment=environment)
    num_valid_users = 33
    for x in range(num_valid_users):
        fname = random_string(8)
        uname = random_string(8)
        email = f"{random_string(8)}@test.com"
        pw    = random_string(8)
        phone = random_string(11)
        try:
            #cur_user = WebsiteUser(environment=None)
            user_handle.register(full_name=fname,
                          user_name=uname,
                          email=email,
                          password=pw,
                          phone=phone)
            cur_valid_user_nfo = (uname, email, pw)
            valid_credentials.append(cur_valid_user_nfo)
        except Exception as e:
            print(e)

def random_string(length:int, inc_numbers:bool = False):
    """Generate a random string of letters and digits."""
    rand_str = ""
    if inc_numbers:
        rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    else:
        rand_str = ''.join(random.choices(string.ascii_letters, k=length))
    return rand_str


# Add this function to be executed before the session starts
@events.init.add_listener
def on_locust_init(environment, **kwargs):
    run_once_before_session()
'''

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Random wait time between 1 and 3 seconds
    host = "http://localhost:5000"
    '''
    def on_start(self):
        self.valid_uname = self.random_string(8)
        self.valid_pword = self.random_string(8)
        self.valid_email = f"{self.random_string(8)}@test.com"
        self.register(full_name = self.random_string(10),
                      user_name = self.valid_uname,
                      email     = self.valid_email,
                      password  = self.valid_pword,
                      phone     = f"+1{random.randint(1000000000, 9999999999)}" )
        # per user on start
    '''

    def random_string(self, length):
        """Generate a random string of letters and digits."""
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




# locust -f stress_test_client_login.py --host=http://127.0.0.1:5000 --html=locust_report.html --users 100 --spawn-rate 1 --run-time 5m
# go to http://127.0.0.1:5000 - click start
# note: test duration was only 5min for sake of time, otherwise would realistically run for 30min-1hr and still run 3x times to ensure consistent results
# since this is a stress test- and given server can handle 10req/sec, 100 users should generate more than that by at least factor of 3
# repeated tests reduce number of users to see if app still breaks under the stress, 100, 50, 25- presuming app fails under 10x expected num users* req/sec != # concurrent users