from django.db import models

class Formula(models.Model):
    formula = models.CharField(max_length=255, default="(courses + td + tp * 0.75) * coef")

    def __str__(self):
        return self.formula


class Professor(models.Model):
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    grade = models.CharField(max_length=255)
    courses = models.FloatField(default=0)
    td = models.FloatField(default=0)
    tp = models.FloatField(default=0)
    coef = models.FloatField(default=0)
    max_surveillance_hours = models.FloatField(default=0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    session_id = models.CharField(max_length=10)
    date = models.DateField()
    time = models.TimeField()
    professor_1 = models.ForeignKey(Professor, related_name="sessions_as_prof_1", null=True, on_delete=models.SET_NULL)
    professor_2 = models.ForeignKey(Professor, related_name="sessions_as_prof_2", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.session_id} - {self.date} {self.time}"