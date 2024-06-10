
# This script imports data from CSV files into database.
# RUN : python manage.py import_data

import csv
import os
import MySQLdb
from typing import Dict, Any
from django.core.management.base import BaseCommand
from content.models import Person, Image, Article
from django.conf import settings

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.create_database()
        os.system('python3 manage.py makemigrations')
        os.system('python3 manage.py migrate')
        self.import_people()
        self.import_images()
        self.import_articles()


    def create_database(self):
        
        name = settings.DATABASES['default']['NAME']
        user = settings.DATABASES['default']['USER']
        pswd = settings.DATABASES['default']['PASSWORD']
        host = 'localhost'
        port = 3306
        
        conn = MySQLdb.connect(
            host = host,
            user = user,
            password = pswd,
            port = port)
        
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {name}")
        cur.close()
        conn.close()

    def import_people(self):
        with open(f'{os.path.dirname(os.path.abspath(__file__))}/res_files/images.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    Person.objects.create(id=row['photographer_code'],
                                    person_name=row['photographer_name'],
                                    email=row['photographer_email'])

                except:
                    pass

    def import_images(self):
        with open(f'{os.path.dirname(os.path.abspath(__file__))}/res_files/images.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                photographer = Person.objects.get(id=row['photographer_code'])
                Image.objects.create(image_path=row['image_path'],
                                    title=row['title'],
                                    tags=row['tags'],
                                    descr=row['description'],
                                    category=row['category'],
                                    photographer=photographer)

    def import_articles(self):
        with open(f'{os.path.dirname(os.path.abspath(__file__))}/res_files/articles.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                writer = Person.objects.get(id=row['writer_code'])
                Article.objects.create(content=row['content'],
                                    keywords=row['keywords'],
                                    title=row['title'],
                                    category=row['category'],
                                    writer=writer)
