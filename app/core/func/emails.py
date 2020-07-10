from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from credentials import SENDGRID_API_KEY

def send_verification_email(firstname, email, verification_code):
    message = Mail(
        from_email='verify@whiskers.app',
        to_emails=email)
    email_data = {"firstname": firstname, "verification_code":verification_code}
    message.dynamic_template_data = email_data
    message.template_id = 'd-6a1b611bbaa045c19015f73e463c7aa4'
    #print(os.environ.get('SENDGRID_API_KEY'))
    result = {}
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        if response.status_code != 202:
            result['status'] = 'fail'
            return result
        # result['body'] = response.body
        # result['response'] = response
        for header in str(response.headers).split('\n'):
            if "X-Message-Id:" in header:
                result['message_id'] = header[header.find(':')+1:].strip()
        result['status'] = 'success'
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
        return result
    except Exception as e:
        print(e)
        result['status'] = 'fail'
        return  result