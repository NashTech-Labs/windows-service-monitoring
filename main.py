import yaml
from time import sleep
import win32serviceutil
import sys
from _library.alertConfig import alert_content


#Get the service to be monitored and interval between notifcations
name_of_service = sys.argv[2]
notify_interval = int(sys.argv[3]) * 60

# Get the webhook url
webhook_url = sys.argv[1]

# Read the windows error code yaml file
error_codes_stream = open("error_code.yaml", "r")
error_code_dictionary = yaml.safe_load(error_codes_stream)


# Return the service status
def service_status(service_name):
    try:
        return win32serviceutil.QueryServiceStatus(serviceName=service_name)
    except:
        print("The specified service does not exist")


# Get the Service status and trigger the alert
def send_out_alerts(service_name):

    attempt_to_start = False
    while True:
        status_code = service_status(service_name)

        if status_code[3] == 0 and status_code[4] == 0:

            if status_code[1] == 1:
                try:
                    win32serviceutil.StartService(serviceName=service_name)
                    alert_content(webhook_url, status=status_code[1], service_name=service_name)
                    attempt_to_start = True
                    sleep(notify_interval)
                except:
                    continue
            
            elif status_code[1] == 7:
                try:
                    alert_content(status=status_code[1], service_name=service_name)
                    attempt_to_start = True
                    sleep(notify_interval)
                except:
                    continue

            elif status_code[1] == 4 and attempt_to_start is True:
                attempt_to_start = False
                alert_content(webhook_url, status=status_code[1], service_name=service_name)
                sleep(notify_interval)
                continue
        else:
            if status_code[3] in range(1001, 1930):
                try:
                    win32serviceutil.RestartService(serviceName=service_name)
                    alert_content(webhook_url, status=-1, service_name=service_name, win32_err_code=status_code[3])
                    attempt_to_start = True
                    sleep(notify_interval)
                except:
                    continue
            else:
                try:
                    win32serviceutil.RestartService(serviceName=service_name)
                    alert_content(webhook_url, status=-1, service_name=service_name, service_error_code=status_code[4])
                    attempt_to_start = True
                    sleep(notify_interval)
                except:
                    continue


send_out_alerts(service_name=name_of_service)
