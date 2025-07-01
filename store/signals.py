from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Order


@receiver(pre_save, sender=Order)
def set_shipped_date(sender, instance, **kwargs):
    if not instance._state.adding:
        try:
            old_order = Order.objects.get(pk=instance.pk)
            if not old_order.status and instance.status:
                instance.shipped_date = timezone.now()
        except Order.DoesNotExist:
            pass
