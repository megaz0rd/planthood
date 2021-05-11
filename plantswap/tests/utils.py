from random import sample, randint, choice
from faker import Faker

from members.models import User
from plantswap.constant import CARE_TYPE
from plantswap.models import Plant, Reminder, Transaction

faker = Faker("pl_PL")


def random_user():
    """Return a random User object from db."""
    user = User.objects.all()
    return choice(user)


def random_plant():
    """Return a random Plant object from db."""
    plant = Plant.objects.all()
    return choice(plant)


def random_status():
    """Return a random STATUS_CHOICE key"""
    return choice([1, 2, 3, 4])


def random_care():
    """Return a random CARE_TYPE key"""
    for key, value in CARE_TYPE:
        return choice(key)


def random_reminder():
    """Return a random Reminder object from db."""
    reminder = Reminder.objects.all()
    return choice(reminder)


def random_plant_for_transaction():
    """Return a random Plant object available for transaction from db."""
    plant = Plant.objects.filter(status__in=[1, 2])
    return choice(plant)


def random_transaction():
    """Return a random Transaction object from db."""
    transaction = Transaction.objects.all()
    return choice(transaction)
