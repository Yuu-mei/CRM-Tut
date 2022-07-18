from django.db.models.signals import post_save;
from django.contrib.auth.models import User, Group;
from .models import Customer;

# Signals will check whenever an event has fired and do something about it (make sure to add it to apps.py)
def create_customer_profile(sender, instance, created, **kwargs):
    if (created):
            # Query the groups
            group = Group.objects.get(name="customer");
            # Add the instance to the group
            instance.groups.add(group);

            # Create the Customer object
            Customer.objects.create(
                user=instance,
                name=instance.username
            );
# To save it to the db
post_save.connect(create_customer_profile, sender=User);