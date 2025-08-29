from django.db import models

class Student(models.Model):
    roll_no = models.IntegerField()
    enrollment_no = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    attended = models.IntegerField()
    conducted = models.IntegerField()
    mentor = models.CharField(max_length=50)
    s_score = models.FloatField(default=0.0) # Ensure default for existing records
    batch = models.IntegerField()
    reason_for_low_attendance = models.TextField(blank=True, null=True) # New field

    @property
    def percentage(self):
        if self.conducted > 0:
            return round((self.attended / self.conducted) * 100, 2)
        return 0.0

    def __str__(self):
        return self.name

class ClassSchedule(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    conducted_by = models.CharField(max_length=100)
    class_id=models.CharField(blank=True, null=True,max_length=50)
    roll_from = models.IntegerField(null=True, blank=True)
    roll_to = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} on {self.date} by {self.conducted_by}"

