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

# def fake_movie_data():
#     """Generate a dict of movie data
#
#     The format is compatible with serializers (`Person` relations
#     represented by names).
#     """
#     movie_data = {
#         "title": f"{faker.job()} {faker.first_name()}",
#         "description": faker.sentence(),
#         "year": int(faker.year()),
#         "director": random_person().name,
#     }
#     people = Person.objects.all()
#     actors = sample(list(people), randint(1, len(people)))
#     actor_names = [a.name for a in actors]
#     movie_data["actors"] = actor_names
#     return movie_data
#
#
# def find_person_by_name(name):
#     """Return the first `Person` object that matches `name`."""
#     return Person.objects.filter(name=name).first()
#
#
# def create_fake_movie():
#     """Generate new fake movie and save to database."""
#     movie_data = fake_movie_data()
#     movie_data["director"] = find_person_by_name(movie_data["director"])
#     actors = movie_data["actors"]
#     del movie_data["actors"]
#     new_movie = Movie.objects.create(**movie_data)
#     for actor in actors:
#         new_movie.actors.add(find_person_by_name(actor))
