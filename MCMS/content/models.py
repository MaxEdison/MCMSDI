from django.db import models

class Person(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    person_name = models.CharField(max_length=255)
    email = models.TextField()

    def __str__(self):
        return self.person_name

class Image(models.Model):
    image_path = models.TextField()
    title = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    descr = models.TextField()
    category = models.CharField(max_length=255)
    photographer = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='Images')

    def __str__(self):
        return self.image_path

class Article(models.Model):
    content = models.TextField()
    keywords = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    writer = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='Articles')

    def __str__(self):
        return self.title
