from django.db import models

# Create your models here.


class Booking(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    no_of_guests = models.IntegerField(blank=False)
    reservation_date = models.DateTimeField()
    reservation_slot = models.SmallIntegerField(default=10)
    def __str__(self):
        return self.first_name

class MenuItem(models.Model):
    title = models.CharField(max_length=255, blank=False)
    inventory = models.SmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    description = models.TextField(blank=True)  # optional
    #category = models.ForeignKey(MenuCategory, on_delete=models.PROTECT)
    #featured = models.BooleanField(db_index=True, default=False)
    def __str__(self):
        return self.title

   


    def get_item(self):
        return f'{self.title} : {str(self.price)}'
    def __str__(self):
        return self.title
