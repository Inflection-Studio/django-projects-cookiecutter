from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class EmailService:
    def __init__(self, request):
        self.request = request

    def send_user_registration_email(self, user, password: str):
        current_site = get_current_site(self.request)
        subject = f"{current_site.name} account created"

        protocol = "https"

        if not self.request.is_secure():
            protocol = "http"

        # TODO: move this to function
        # send_email(recipient=user.email, from_email=settings.DEFAULT_FROM_EMAIL, subject=subject,template_name='account/emails/welcome.html')
        message = render_to_string(
            "account/emails/welcome.html",
            {
                "user": user,
                "protocol": protocol,
                "site": current_site,
                "password": password,
                "frontend_host": settings.FRONTEND_HOST,
            },
        )
        email = EmailMultiAlternatives(
            subject,
            message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[
                user.email,
            ],
        )
        email.content_subtype = "html"
        email.send()

    def send_new_contact_form_message_email(self, contact_message):
        current_site = get_current_site(self.request)
        subject = f"{current_site.name} contact form message"

        template_name = "account/emails/contact-form.html"

        for recipient in settings.CONTACT_EMAIL_RECIPIENTS:
            self.send_email(
                self.request,
                recipient=recipient,
                subject=subject,
                contact_message=contact_message,
                from_email=contact_message.get("email"),
                template_name=template_name,
            )

    def send_email(
        self,
        recipient: str,
        subject: str,
        contact_message: str,
        from_email: str,
        template_name: str,
    ):
        current_site = get_current_site(self.request)

        protocol = "http"

        if self.request.is_secure():
            protocol = "https"
        message = render_to_string(
            template_name,
            {
                "message": contact_message,
                "protocol": protocol,
                "site": current_site,
            },
        )
        email = EmailMultiAlternatives(
            subject,
            message,
            from_email=from_email,
            to=[
                recipient,
            ],
        )
        email.content_subtype = "html"
        email.send()
