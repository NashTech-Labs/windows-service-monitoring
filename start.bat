@ECHO OFF
:: You can hard code the webhook URL, service name and notify interval by uncommenting the lines below
:: set url=<slack-webhook>
:: set service_name=<service-name>
:: set notify_interval=<notify-interval-in-minutes>

IF not defined url echo "Variable url Not Defined" & EXIT /B
IF not defined service_name echo "Variable service_name Not Defined" & EXIT /B
IF not defined notify_interval set notify_interval=5

call python -m venv .\venv
call .\venv\Scripts\activate
call pip install -r requirements.txt
call python main.py %url% %service_name% %notify_interval%
PAUSE