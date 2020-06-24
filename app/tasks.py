from app.extensions import celery
from app.core.func import emails
from app import models, db
print(type(celery))

@celery.task()
def add_numbers(a,b):
    return a + b

@celery.task()
def task_send_verification_email(user_firstname, user_username, user_id, otp):
    email = emails.send_verification_email(user_firstname, user_username, otp)
    print(user_firstname, user_username, otp)
    otp = models.UserOTP(code=otp, user_id=user_id, sg_message_id=email['message_id'], type='first')
    db.session.add(otp)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        print("failed")

    return email