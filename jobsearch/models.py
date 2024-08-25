from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, password, **extra_fields)


class user_table(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=15)
    address =models.CharField(max_length=50)
    domain=models.CharField(max_length=25)
    about=models.CharField(max_length=200)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)


    objects=UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'mobile_no' , 'address']


class Opportunity(models.Model):
    TYPE_CHOICES = [
        ('job', 'Job'),
        ('internship', 'Internship'),
    ]
    
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    domain = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Salary may not be applicable for internships
    experience = models.CharField(max_length=50)
    prerequisites = models.TextField()
    description = models.TextField()
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"
    

class AppliedJob(models.Model):
    user = models.ForeignKey('user_table', on_delete=models.CASCADE)
    opportunity = models.ForeignKey('opportunity', on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} applied for {self.opportunity.title}"
