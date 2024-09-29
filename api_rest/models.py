from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    rut = models.CharField(max_length=12, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['name', 'last_name', 'email', 'phone_number', 'rut']

    def __str__(self):
        return self.email
    

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Commune(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='communes')

    def __str__(self):
        return self.name
    

class Address(models.Model):
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='addresses')

    def __str__(self):
        return f"{self.street} {self.number}, {self.city}, {self.postal_code}"
    
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='hotels')

    def __str__(self):
        return self.name
    

class Room(models.Model):
    type = models.CharField(max_length=2)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')

    def __str__(self):
        return f"{self.type} room at {self.hotel.name}"


class Reservation(models.Model):
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    number_of_guests = models.PositiveIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='reservations')

    def __str__(self):
        return f"Reservation by {self.user.email} for room {self.room.type} from {self.check_in_date} to {self.check_out_date}"

