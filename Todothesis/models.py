from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):  # Main category
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubCategory(models.Model):  # Custom user-defined subcategory
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.main_category.name})"

class ProgressUpdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)  # ✅ NEW FIELD
    entry = models.TextField()
    feedback = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp.date()}"

class GoalSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Goal: {self.value}"
