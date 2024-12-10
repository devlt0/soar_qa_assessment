Feature: Client Login & Registration

  Scenario: Perform load testing for register and login with both valid and invalid credentials
    # Given # setup is nested in subproc call to locust file to be executed
    When load tests are executed using "10" users for "1" minutes spawn rate "1" per sec and output report "behave_wrapped_locust_report.html"
    Then the load testing should complete successfully