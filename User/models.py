from django.db import models


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phoneno = models.CharField(max_length=15)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class attack_prediction(models.Model):
    url = models.URLField(max_length=500)
    prediction = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.url} - {self.prediction}"


class detection_accuracy(models.Model):
    name = models.CharField(max_length=100)
    ratio = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.ratio}"


class detection_ratio(models.Model):
    name = models.CharField(max_length=100)
    ratio = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.ratio}"