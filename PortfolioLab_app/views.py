from datetime import datetime


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Max
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from .models import Category, Donation, Institution
from django.views.generic import CreateView, FormView, DeleteView, UpdateView
from .forms import InstitutionForm, RegistrationForm, LoginForm, CategoryForm, DonationUpdateForm, \
    UserUpdateForm


# Create your views here.

class MainView(View):
    def get(self, request):
        all_donation = Donation.objects.all()
        total_quantity = sum(donation.quantity for donation in all_donation)
        all_institution = Institution.objects.aggregate(Max('id'))['id__max']

        page = request.GET.get('page')

        institution_fundacja = Institution.objects.filter(type=1).order_by('name')
        paginator_help_institution_fundacja = Paginator(institution_fundacja, 5)
        help_institution_fundacja = paginator_help_institution_fundacja.get_page(page)

        institution_organizacja = Institution.objects.filter(type=2).order_by('name')
        paginator_help_institution_organizacja = Paginator(institution_organizacja, 5)
        help_institution_organizacja = paginator_help_institution_organizacja.get_page(page)

        institution_zbiorka = Institution.objects.filter(type=3).order_by('name')
        paginator_help_institution_zbiorka = Paginator(institution_zbiorka, 5)
        help_institution_zbiorka = paginator_help_institution_zbiorka.get_page(page)

        context = {
            'total_quantity': total_quantity,
            'all_institution': all_institution,
            'help_institution_fundacja': help_institution_fundacja,
            'help_institution_organizacja': help_institution_organizacja,
            'help_institution_zbiorka': help_institution_zbiorka

        }
        return render(request, 'index.html', context)


class StaffRequiredMixin(UserPassesTestMixin, LoginRequiredMixin):
    def test_func(self):
        return self.request.user.is_staff


class LoginView(View):
    def get(self, request):
        form = LoginForm
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                return redirect('registration')


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = "register.html"
    success_url = '/login/'

    def form_valid(self, form):
        data = form.cleaned_data
        data.pop('password_confirmation')
        User.objects.create_user(**data)
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user_update.html'

    def get_success_url(self):
        user_id = self.object.id
        return reverse_lazy('profil', kwargs={'user_id': user_id})

    def form_valid(self, form):
        current_password = form.cleaned_data['current_password']
        user = self.request.user

        if not user.check_password(current_password):
            form.add_error('current_password', 'Nieprawidłowe hasło')
            return self.form_invalid(form)
        if form.cleaned_data.get('password'):
            new_password = form.cleaned_data['password']
            password_confirmation = form.cleaned_data['password_confirmation']
            user = self.request.user

            if new_password != password_confirmation:
                form.add_error('password_confirmation', 'Podane hasła różnią się')
                return self.form_invalid(form)

            user.set_password(new_password)
            user.save()

        return super().form_valid(form)

def logout_view(request):
    logout(request)
    return redirect('/')


class UserInfoView(LoginRequiredMixin, View):
    def get(self,request,user_id):
        users = User.objects.filter(id=user_id)
        context = {
            'users': users
        }
        return render(request, 'UserInfo.html', context)


class DonationView(LoginRequiredMixin, View):
    def get(self, request):
        all_category = Category.objects.all()
        all_institution = Institution.objects.all()
        context = {
            'all_category':all_category,
            'all_institution':all_institution,
        }
        return render(request, 'form.html', context)

    def post(self, request):
        try:
            institution_name = request.POST.get('organization')
            institution = Institution.objects.get(name=institution_name)
            categories_names = request.POST.getlist('categories')
            categories_ids = []
            for category_name in categories_names:
                    category = Category.objects.get(name=category_name)
                    categories_ids.append(category.id)
            user = request.user
            quantity = request.POST.get('bags')
            address = request.POST.get('address')
            phone_number = request.POST.get('phone')
            city = request.POST.get('city')
            zip_code = request.POST.get('postcode')
            pick_up_date_str = request.POST.get('data')
            pick_up_date = datetime.strptime(pick_up_date_str, '%Y-%m-%d').date()
            pick_up_time = request.POST.get('time')
            pick_up_comment = request.POST.get('more_info')
            new_donation= Donation.objects.create(quantity=quantity, institution=institution,
                                                  address=address, phone_number=phone_number, city=city,
                                                  zip_code=zip_code, pick_up_date=pick_up_date, pick_up_time=pick_up_time,
                                                  pick_up_comment=pick_up_comment, user=user)
            new_donation.categories.set(categories_ids)
            return render(request, 'form-confirmation.html')
        except Exception:
            return HttpResponseServerError('Coś poszło nie tak, sprobój pózniej')


class AllDonationView(StaffRequiredMixin, View):
    def get(self,request):
        donations_f = Donation.objects.filter(is_taken=False)
        donations_t = Donation.objects.filter(is_taken=True)
        return render(request, 'all_donations.html', {'donations_f':donations_f, 'donations_t':donations_t})

class DonationUpdateView(UpdateView):
    model = Donation
    form_class = DonationUpdateForm
    template_name = 'forms.html'
    success_url = reverse_lazy('all_donation')

class SuccessView(View):
    def get(self,request):
        return render(request, 'form-confirmation.html')


class AllInstitutionView(StaffRequiredMixin, View):
    def get(self, request):
        all_institution = Institution.objects.all()
        context = {
            'all_institution': all_institution
        }
        return render(request, 'all_institution.html', context)


class InstitutionCreateView(StaffRequiredMixin, CreateView):
    form_class = InstitutionForm
    template_name = 'institution_create.html'
    success_url = reverse_lazy('all_institution')


class InstitutionDeleteView(StaffRequiredMixin, DeleteView):
    model = Institution
    template_name = 'delete.html'
    success_url = reverse_lazy('all_institution')


class InstitutionUpdateView(StaffRequiredMixin, UpdateView):
    model = Institution
    form_class = InstitutionForm
    template_name = 'forms.html'
    success_url = reverse_lazy('all_institution')


class CategoryCreateView(CreateView):
    form_class = CategoryForm
    template_name = 'forms.html'
    success_url = '/'


class UserDonation(LoginRequiredMixin, View):
    def get(self, request):
        user_donation_f = Donation.objects.filter(user=request.user, is_taken=False)
        user_donation_t = Donation.objects.filter(user=request.user, is_taken=True)
        date_now = datetime.now().date()

        context = {
            'user_donation_f': user_donation_f,
            'user_donation_t':user_donation_t,
            'date_now': date_now,
        }

        return render(request, 'user_donation.html', context)

