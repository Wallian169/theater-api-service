from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name


class Play(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name="genres")
    actors = models.ManyToManyField(Actor, related_name="actors")

    def __str__(self) -> str:
        return self.name


class TheatreHall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name


class Performance(models.Model):
    play = models.ForeignKey(
        Play, on_delete=models.CASCADE, related_name="performances"
    )
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self) -> str:
        return f"{self.play.name} at {self.theatre_hall.name} on {self.date} at {self.time}"
