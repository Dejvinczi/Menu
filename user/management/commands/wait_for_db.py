"""
Django command to wait for the db to be available.
"""

import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    help = "Waits for the database to be available"

    def handle(self, *args, **kwargs):
        self.stdout.write("Waiting for the database..")
        db_up = False
        while db_up:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write(
                    self.style.WARNING("Database unavailable, waiting 1 second..")
                )
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available"))
