from django.db import models


class Company(models.Model):
    id = models.CharField(max_length=255, primary_key=True, editable=False)  # Custom ID field
    name = models.CharField(max_length=255, blank=True, null=True)
    about = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    founding_date = models.CharField(max_length=255, blank=True, null=True)
    number_of_employee = models.IntegerField()
    location = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Check if ID is not already set
            # Generate a custom ID
            prefix = self.name.replace(" ", "").lower()  # Convert name to lowercase and remove spaces
            last_company = Company.objects.all().order_by('-id').first()
            if last_company:
                last_id = int(last_company.id.split(prefix)[-1])  # Extract the number part of the last ID
                self.id = f"{prefix}{last_id + 1}"  # Increment the number by 1
            else:
                self.id = f"{prefix}1"  # This is the first company with this name
        super(Company, self).save(*args, **kwargs)  # Call the parent class's save method

    def __str__(self):
        return self.name
    
class AccountsUser(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users')

    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255, null=False, blank=False)
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    role = models.CharField(max_length=255, null=False, blank=False)
    birth_date = models.CharField(max_length=255, null=False, blank=False)
    reward_points = models.IntegerField(default=0)

    def __str__(self):
        return self.email


class Feedback(models.Model):
    sender = models.ForeignKey(AccountsUser, on_delete=models.CASCADE, related_name='feedbacks_sender', null=True)
    receiver = models.ForeignKey(AccountsUser, on_delete=models.CASCADE, related_name='feedbacks_receiver', null=True)

    insight  = models.CharField(max_length=255, blank=True, null=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.receiver.name
