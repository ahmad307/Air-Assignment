from django.contrib import admin
from users import models

admin.site.register(models.UserProfile)
admin.site.register(models.Assignment)
admin.site.register(models.Course)
admin.site.register(models.Submission)
