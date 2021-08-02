from celery import Celery
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from emailhistory.models import EmailHistory

app = Celery('celery_tasks', broker='pyamqp://guest@localhost//', backend='rpc://',)


@app.task
def send_email_task(body, sender, email):
    """
    task for send email
    :param body: email body
    :param sender: user wanna send email
    :param email: email receiver
    :return: none
    """
    try:
        send_mail('Your Quote', body, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
        EmailHistory.objects.create(creator=get_user_model().objects.get(username=sender), email=email, email_status=True)
        return 'Email send successfully.'
    except:
        EmailHistory.objects.create(creator=get_user_model().objects.get(username=sender), email=email, email_status=False)
        return 'Email send failed.'
