from django.shortcuts import render
from django.views import View
from main_app.models import Donation, Institution
from django.core.paginator import Paginator

# Create your views here.


class LandingPageView(View):
    def get(self, request):
        donations = Donation.objects.all()
        all_bags = 0
        for donation in donations:
            all_bags += donation.quantity
        institutions = Institution.objects.all()
        supported_institutions = 0
        for institution in institutions:
            institution_donations = institution.donation_set.all()
            if len(institution_donations) > 0:
                supported_institutions += 1
        foundations = Institution.objects.all().filter(type='foundation')
        organizations = Institution.objects.all().filter(type='non-governmental organization')
        local_collections = Institution.objects.all().filter(type='local collection')
        # pag_foundations = Paginator(foundations, 5)
        # pag_organizations = Paginator(organizations, 5)
        # pag_local_collections = Paginator(local_collections, 5)
        return render(request, 'index.html', {'all_bags': all_bags, 'supported_institutions': supported_institutions,
                                              'foundations': foundations, 'organizations': organizations,
                                              'local_collections': local_collections})


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
