from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField(default=365)  # Duration in days
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), null=True, blank=True)
    
    # Adding a boolean field for activation status
    is_activated = models.BooleanField(default=False)
    
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    subscription_end_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.subscription_end_date and self.subscription_plan:
            from datetime import timedelta
            self.subscription_end_date = self.date_joined + timedelta(days=self.subscription_plan.duration)
        super().save(*args, **kwargs)


