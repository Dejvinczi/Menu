"""
Menu model tasks tests.
"""

import pytest

from django.core import mail
from django.utils import timezone

from user.tests.factories import UserFactory
from menu.tasks import send_emails_with_updated_menu_information_to_users


@pytest.mark.django_db
def test_send_emails_with_updated_menu_information_to_users(
    email_backend_setup,
    menu_factory,
    dish_factory,
    dish_model,
):
    """Test of sending emails with updated dishes to users."""

    menu1 = menu_factory(name="Test Menu 1")
    menu2 = menu_factory(name="Test Menu 2")
    menu3 = menu_factory(name="Test Menu 3")
    dish1 = dish_factory(name="Dish 1", menu=menu1)
    dish2 = dish_factory(name="Dish 2", menu=menu2)

    yesterday = timezone.now() - timezone.timedelta(days=1)
    dish_model.objects.filter(id__in=[dish1.id, dish2.id]).update(updated_on=yesterday)

    UserFactory(email="user1@example.com", is_active=True)
    UserFactory(email="user2@example.com", is_active=True)

    send_emails_with_updated_menu_information_to_users()

    assert len(mail.outbox) == 1

    email = mail.outbox[0]

    assert "Menu news!" in email.subject
    assert menu1.name in email.body
    assert dish1.name in email.body
    assert menu2.name in email.body
    assert dish2.name in email.body
    assert menu3.name not in email.body


@pytest.mark.django_db
def test_send_emails_with_updated_menu_information_to_users_without_users(
    email_backend_setup,
    menu_factory,
    dish_factory,
    dish_model,
):
    """Test of sending emails with updated dishes to users without having users."""

    menu1 = menu_factory(name="Test Menu 1")
    menu2 = menu_factory(name="Test Menu 2")
    dish1 = dish_factory(name="Dish 1", menu=menu1)
    dish2 = dish_factory(name="Dish 2", menu=menu2)

    yesterday = timezone.now() - timezone.timedelta(days=1)
    dish_model.objects.filter(id__in=[dish1.id, dish2.id]).update(updated_on=yesterday)

    send_emails_with_updated_menu_information_to_users()

    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_send_emails_with_updated_menu_information_to_users_without_updated_dishes(
    email_backend_setup,
):
    """Test of sending emails with updated dishes to users without updated dishes."""

    UserFactory(email="user1@example.com", is_active=True)
    UserFactory(email="user2@example.com", is_active=True)

    send_emails_with_updated_menu_information_to_users()

    assert len(mail.outbox) == 0
