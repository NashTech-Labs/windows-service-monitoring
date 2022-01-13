import requests
import json

headers = {'Content-type': 'application/json'}
payload = {"text": "", "attachments": ""}


def alert_content(webhook_url, status, service_name, win32_err_code=0, service_error_code=0):
    if status == 1:
        payload['text'] = f"Service *{service_name}* is *Stopped*. \nAttempting to Start the Service."
        payload['attachments'] = [{"text": f"*Service*: `{service_name}`\n*Status*: `Stopped`", "color": "#808080"}]

    if status == 4:
        payload['text'] = f"Service *{service_name}* is *Running*. "
        payload['attachments'] = [{"text": f"*Service*: `{service_name}`\n*Status*: `Running`", "color": "#32CD32"}]

    if status == 7:
        payload['text'] = f"Service *{service_name}* is *Paused*. \nAttempting to Start the Service"
        payload['attachments'] = [{"text": f"*Service*: `{service_name}`\n*Status*: `Paused`", "color": "#FFFF00"}]

    if status == -1:
        if win32_err_code in range(1001, 1930):
            payload['text'] = f"Service *{service_name}* is *Failed*. \nAttempting to Restart the Service"
            payload['attachments'] = [{"text": f"*Service*: `{service_name}`\n*Status*: `Failed`\n*Win32 Error Code*: `{win32_err_code}` \n*Error Name*: `{error_code_dictionary[win32_err_code][1]}` \n*Error Description*: `{error_code_dictionary[win32_err_code][0]}`", "color": "#FF0000"}]
        else:
            payload['text'] = f"Service *{service_name}* is *Failed*. \nAttempting to Restart the Service"
            payload['attachments'] = [{"text": f"*Service*: `{service_name}`\n*Status*: `Failed`\n*Service Specific Error Code*: `{service_error_code}`","color": "#FF0000"}]

    requests.post(url=webhook_url, headers=headers, data=json.dumps(payload))