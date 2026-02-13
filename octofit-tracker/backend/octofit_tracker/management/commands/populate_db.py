from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import connection
from pymongo import MongoClient
from datetime import date

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        # Create users
        users = [
            User(email='tony@stark.com', username='IronMan', team=marvel),
            User(email='steve@rogers.com', username='CaptainAmerica', team=marvel),
            User(email='bruce@wayne.com', username='Batman', team=dc),
            User(email='clark@kent.com', username='Superman', team=dc),
        ]
        for user in users:
            user.save()

        # Create activities
        Activity.objects.create(user=users[0], type='run', duration=30, date=date(2024,1,1))
        Activity.objects.create(user=users[1], type='cycle', duration=45, date=date(2024,1,2))
        Activity.objects.create(user=users[2], type='swim', duration=60, date=date(2024,1,3))
        Activity.objects.create(user=users[3], type='yoga', duration=20, date=date(2024,1,4))

        # Create workouts
        w1 = Workout.objects.create(name='Pushups', description='Upper body strength')
        w2 = Workout.objects.create(name='Squats', description='Lower body strength')
        w1.suggested_for.set([users[0], users[2]])
        w2.suggested_for.set([users[1], users[3]])

        # Create leaderboards
        Leaderboard.objects.create(team=marvel, points=150)
        Leaderboard.objects.create(team=dc, points=120)

        # Ensure unique index on email (MongoDB)
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.user.create_index('email', unique=True)
        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))
