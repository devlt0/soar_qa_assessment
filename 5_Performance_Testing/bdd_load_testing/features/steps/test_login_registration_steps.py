import subprocess
from behave import given, when, then
import requests

BASE_URL = "http://localhost:5000"

@when('When load tests are executed using "{num_users}" users for "{load_duration}" minutes spawn rate "{spawn_rate}" per sec and output report "{report_fname}"')
def step_impl(context, num_users, load_duration, spawn_rate, report_fname):
    if not report_fname.endswith(".html"):
        report_fname += '.html'
    print("Executing Locust load tests...")
    result = subprocess.run([
        "locust", "-f", "locust_login_registration_mixedvalid.py", "--headless", "--users", f"{num_users}", "--spawn-rate", f"{spawn_rate}", "--run-time", "{load_duration}m", "--html", f"{report_fname}"
    ], capture_output=True, text=True)
    context.locust_result = result
    print(result.stdout)
    print(result.stderr)

@then('the load testing should complete successfully')
def step_impl(context):
    assert context.locust_result.returncode == 0
    print("Locust load testing completed successfully.")
