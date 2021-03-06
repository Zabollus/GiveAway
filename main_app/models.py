from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nazwa')

    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'

    def __str__(self):
        return self.name


TYPES = {
    ('foundation', 'fundacja'),
    ('non-governmental organization', ' organizacja pozarządowa'),
    ('local collection', 'zbiórka lokalna')
}


class Institution(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nazwa')
    description = models.TextField(verbose_name='Opis')
    type = models.CharField(choices=TYPES, default='foundation', max_length=32)
    categories = models.ManyToManyField(Category, verbose_name='Kategorie')

    class Meta:
        verbose_name = 'Instytucja'
        verbose_name_plural = 'Instytucje'

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField(verbose_name='Liczba worków')
    categories = models.ManyToManyField(Category, verbose_name='Kategorie')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name='Instytucja')
    address = models.CharField(max_length=128, verbose_name='Adres')
    phone_number = models.CharField(max_length=12, verbose_name='Numer telefonu')
    city = models.CharField(max_length=32, verbose_name='Miasto')
    zip_code = models.CharField(max_length=6, verbose_name='Kod pocztowy')
    pick_up_date = models.DateField(verbose_name='Data odebrania')
    pick_up_time = models.TimeField(verbose_name='Godzina odebrania')
    pick_up_comment = models.TextField(verbose_name='Komentarz do przesyłki', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    is_taken = models.BooleanField(verbose_name='Odebrany', default=False)

    class Meta:
        verbose_name = 'Donacja'
        verbose_name_plural = 'Donacje'

    def __str__(self):
        return str(self.quantity) + ' worków od ' + self.user.first_name + ' ' + self.user.last_name + ' dla ' + \
               self.institution.name
