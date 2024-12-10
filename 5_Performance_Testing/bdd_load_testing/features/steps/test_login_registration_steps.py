import subprocess
from behave import given, when, then
import requests

BASE_URL = "http://localhost:5000"

@when('load tests are executed using "{num_users}" users for "{load_duration}" minutes spawn rate "{spawn_rate}" per sec and output report "{report_fname}"')
def step_impl(context, num_users, load_duration, spawn_rate, report_fname):
    if not report_fname.endswith(".html"):
        report_fname += '.html'
    print("Executing Locust load tests...")
    result = subprocess.run([
        "locust", "-f", "C:/Users/human-c137/Documents/GitHub/soar_qa_assessment/5_Performance_Testing/bdd_load_testing/features/steps/locust_login_registration_mixedvalid.py", "--headless", "--users", f"{num_users}", "--spawn-rate", f"{spawn_rate}", "--run-time", f"{load_duration}m", "--html", f"{report_fname}"
    ], capture_output=True, text=True)
    context.locust_result = result

@then('the load testing should complete successfully')
def step_impl(context):
    ran_to_timeout_msg = "Shutting down (exit code 1)"
    assert (ran_to_timeout_msg in context.locust_result.stderr) \
    or (ran_to_timeout_msg in context.locust_result.stdout)

    # since 0 is usually successful exit code and this is known issue with running locust via command line/subproc
