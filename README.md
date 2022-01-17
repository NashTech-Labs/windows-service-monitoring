# Windows Service Monitoring

Service Controller is a Windows service manager using which we can query to get the state of a service in Windows from CLI. But what if we need to continuosly montior any service and alert us over Slack when it happens. This project uses Python and pywin32 library to monitor the specified service.

## Prerequisites

- \>=Python3.6
- python-venv

## Usage guide

There is a script to start the monitoring process, named `start.bat`. But it will need the slack webhook URL, service name to be monitored, notification window interval as environment variables.

To setup webhook on slack, visit [Slack-Webhook](https://api.slack.com/messaging/webhooks)

#### Setup Environment Variables

Considering the slack webhook has been set, next step will be to run the CMD(Windows Command Prompt) or Windows Powershell as administrator.  
> This script not only notifies but also manages the service, and tries to restart the service when it is stopped or when it fails. In case of failure it also sends the error description and code on Slack.

To set the variable on `CMD`
```
set url=<slack-webhook>
set service_name=<service-name>
set notify_interval=<notify-interval-in-minutes>
```
In case you are using `powershell  `
```
$env:url = <slack-webhook>
$env:service_name = <service-name>
$env:notify_interval = <notify-interval-in-minutes>
```

#### Starting the script

Now to start the script execute the `start.bat` as:
```
.\start.bat
```

The startup script will perform these tasks:  
- Create a virtual environment `venv`
- Activate the virtual environment
- Install all the required packages from `requirements.txt`
- Call the `main.py` which will use the win32 library to montior the services and notify through slack.
- The startup script takes default value of `notify_interval` to be 5 seconds
- The file `error_code.yaml` consists all the windows error codes and their names and description to the error. The script reads and display the error info from this file.

#### Status Codes
| Code | Status|
| - | - |
| 1 | Stopped |
| 4 | Running |
| 7 | Paused |

#### Slack snapshots