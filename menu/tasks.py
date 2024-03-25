"""
Menu module celery tasks.
"""

from collections import defaultdict
from celery import shared_task

from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from menu.models import Dish


@shared_task
def send_emails_with_updated_menu_information_to_users():
    recipients_emails = (
        get_user_model().objects.filter(is_active=True).values_list("email", flat=True)
    )

    if not recipients_emails:
        return

    yesterday = timezone.now() - timezone.timedelta(days=1)
    updated_dishes = Dish.objects.select_related("menu").filter(
        updated_on__date=yesterday.date()
    )

    if not updated_dishes:
        return

    dishes_grouped_by_menu = defaultdict(list)
    for dish in updated_dishes:
        dishes_grouped_by_menu[dish.menu].append(dish)

    html_message = render_to_string(
        "updated_dishes_notify_email.html",
        {"data": dict(dishes_grouped_by_menu)},
    )

    msg = EmailMultiAlternatives(
        subject="Menu news!",
        body=html_message,
        to=["dejvinczi.main@gmail.com", "dawid.gurgul.krakow@gmail.com"],
        bcc=["dejvinczi.main@gmail.com", "dawid.gurgul.krakow@gmail.com"],
    )
    msg.content_subtype = "html"
    msg.send()
