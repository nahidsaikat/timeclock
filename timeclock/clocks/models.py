from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class UserClock(models.Model):
    user = models.ForeignKey(
        User, related_name="user_clocks", on_delete=models.CASCADE
    )
    clocked_in = models.DateTimeField()
    clocked_out = models.DateTimeField(blank=True, null=True)
