from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings as conf_settings

from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings as conf_settings
from celery import shared_task


@shared_task
def send_email(subject, template_path, template_context, receiver, body=None):
    """
    Helper function to send emails with HTML content.
    """
    htmly = get_template(template_path)
    html_content = htmly.render(template_context)

    message = EmailMultiAlternatives(
        subject=subject,
        body=body or "",
        from_email=conf_settings.DEFAULT_FROM_EMAIL,
        to=[receiver],
    )
    message.attach_alternative(html_content, "text/html")
    try:
        message.send(fail_silently=False)
        # print('Success', receiver)
    except Exception as e:
        # print('Email did not send', e)
        pass


def _send_welcome_email(template_context, receiver):
    send_email(
        subject="Welcome to Snowberry.",
        template_path="dashboard/email/welcome_email.html",
        template_context=template_context,
        receiver=receiver,
        body="Welcome!!!",
    )


def _send_first_credential_email(template_context, receiver):
    send_email(
        subject="Login Credential.",
        template_path="dashboard/email/first_credential_email.html",
        template_context=template_context,
        receiver=receiver,
        body="Very confidential content, do not share.",
    )
