import csv
import StringIO
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.views.generic.base import View
from inventories.models import Inventory
from pharmacies.forms import MyRegistrationForm, ContactForm, EditProfileForm
from pharmacies.models import Pharmacy, Client


#My own logout system.
class Logout(View):
    """
    logout for pharmacies
    """

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect(reverse('home'))


class Main(generic.View):
    """The main dashboard once a pharmacy is logged in """
    model = Pharmacy
    template_name = 'registration/main.html'
    initial = {}

    def get(self, request, *args, **kwargs):
        self.initial['client'] = Client.objects.filter(pharmacy=self.request.user)
        self.initial['inventory'] = Inventory.objects.filter(pharmacy=self.request.user)
        return render(request, self.template_name, self.initial)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Main, self).dispatch(*args, **kwargs)


class LocationSearch(generic.View):
    template_name = 'map2.html'
    initial = {}

    def get(self, request, *args, **kwargs):
        pharmacy = Pharmacy.objects.get(username=kwargs['username'])
        self.initial['lat'] = pharmacy.lat
        self.initial['lng'] = pharmacy.lng
        return render(request, self.template_name, self.initial)


class DeleteContact(View):
    model = Client
    initial = {}
    form_class = ContactForm
    template_name = 'registration/add_staff.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pharmacies:contact_list'))
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DeleteContact, self).dispatch(*args, **kwargs)


class EditContact(View):
    model = Client
    initial = {}
    form_class = ContactForm
    template_name = 'registration/edit_user.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pharmacies:contact_list'))
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditContact, self).dispatch(*args, **kwargs)


class AddUser(View):
    model = Client
    initial = {}
    form_class = ContactForm
    template_name = 'registration/add_staff.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pharmacies:contact_list'))
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddUser, self).dispatch(*args, **kwargs)


class DeleteUser(View):
    model = Client
    initial = {}
    form_class = ContactForm
    template_name = 'registration/delete_staff.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pharmacies:contact_list'))
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DeleteUser, self).dispatch(*args, **kwargs)


class EditUser(View):
    model = Client
    initial = {}
    form_class = ContactForm
    template_name = 'registration/edit_staff.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pharmacies:contact_list'))
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditUser, self).dispatch(*args, **kwargs)


class ChangePassword(View):
    model = Pharmacy
    form_class = SetPasswordForm
    template_name = 'registration/password.html'
    initial = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.initial)

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(self.form_class(request.POST))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pharmacies:pharmacy'))
        self.initial['errors'] = form.errors
        return HttpResponseRedirect(reverse('pharmacies:change'))


class Chart(generic.ListView):
    template_name = 'registration/chart_dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SMS(generic.ListView):
    model = Client
    template_name = 'registration/sms.html'

    def get_context_data(self, **kwargs):
        context = super(SMS, self).get_context_data(**kwargs)
        pharmacy = self.request.user
        context['client'] = Client.objects.filter(pharmacy=pharmacy)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SMS, self).dispatch(*args, **kwargs)


class Email(generic.ListView):
    model = Client
    template_name = 'registration/email.html'

    def get_context_data(self, **kwargs):
        context = super(Email, self).get_context_data(**kwargs)
        context['client'] = Client.objects.filter(pharmacy=self.request.user)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Email, self).dispatch(*args, **kwargs)


class EditProfile(View):
    model = Pharmacy
    form_class = EditProfileForm
    initial = {}
    template_name = 'registration/edit_profile.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditProfile, self).dispatch(*args, **kwargs)


class Register(View):
    """
    class for registering pharmacies
    """
    form_class = MyRegistrationForm
    initial = {}
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.initial)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        self.initial['email'] = request.POST.get('email')
        self.initial['name'] = request.POST.get('name')
        self.initial['username'] = request.POST.get('username')
        if form.is_valid():
            form.save()
            user = auth.authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            auth.login(request, user)
            return HttpResponseRedirect(reverse('pharmacies:main'))
        self.initial['errors'] = form.errors
        return HttpResponseRedirect(reverse('register'))


class PharmacyProfile(View):
    """
    This class views pharmacy's profile and one can edit his profile in this class.
    """
    model = Pharmacy
    form_class = EditProfileForm
    template_name = 'registration/user.html'
    initial = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.initial)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pharmacies:pharmacy'))
        self.initial['errors'] = form.errors
        return HttpResponseRedirect(reverse('pharmacies:pharmacy'))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PharmacyProfile, self).dispatch(*args, **kwargs)


class ContactList(generic.ListView):
    model = Client
    template_name = 'registration/client_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContactList, self).get_context_data(**kwargs)
        context['client'] = Client.objects.filter(pharmacy=self.request.user)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ContactList, self).dispatch(*args, **kwargs)


class Contact(View):
    model = Client
    initial = {}
    form_class = ContactForm
    template_name = 'registration/contact.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pharmacies:contact_list'))
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Contact, self).dispatch(*args, **kwargs)


class Map(generic.ListView):
    template_name = 'registration/map.html'
    initial = {}

    def get(self, request, *args, **kwargs):
        pharmacy = request.user
        self.initial['lat'] = pharmacy.lat
        self.initial['lng'] = pharmacy.lng
        return render(request, self.template_name, self.initial)

    def post(self, request, *args, **kwargs):
        pharmacy = request.user
        if request.POST.get('lng'):
            pharmacy.lng = request.POST.get('lng')
            pharmacy.lat = request.POST.get('lat')
            pharmacy.save()
        return HttpResponseRedirect(reverse('pharmacies:map'))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Map, self).dispatch(*args, **kwargs)



