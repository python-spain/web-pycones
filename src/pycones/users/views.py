# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from braces.views import CsrfExemptMixin
from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.utils.translation import ugettext_lazy as _

from pycones.users.forms import SignInForm, RestorePasswordForm, RequestRestoreCodeForm
from pycones.users.models import User


class SignInView(CsrfExemptMixin, View):
    """View to allow to login users into the platform."""
    template_name = "users/sign_in.html"

    @staticmethod
    def get_next_page(request):
        """Gets the page to go after log in."""
        default_redirect = reverse('home')
        next_page = request.GET.get('next') or request.POST.get('next')
        return next_page or default_redirect

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        data = {
            "form": SignInForm(),
            "next": request.GET.get('next')
        }
        return render(request, self.template_name, data)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        next_page = self.get_next_page(request=request)
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password'),
                request=request
            )
            if user is not None:
                login(request, user)
                return redirect(next_page)
        data = {"form": form, "next": next_page}
        return render(request, self.template_name, data)


class SignOutView(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        logout(request)
        return redirect("home")


class RestorePasswordView(View):

    @staticmethod
    def get(request, restore_code):
        try:
            user = User.objects.get(restore_code=restore_code)
        except User.DoesNotExist:
            raise Http404
        data = {
            "user": user,
            "restore_code": restore_code,
            "form": RestorePasswordForm(initial={"restore_code": restore_code, "email": user.email})
        }
        return render(request, "users/restore.html", data)

    @staticmethod
    def post(request, restore_code):
        form = RestorePasswordForm(request.POST)
        try:
            user = User.objects.get(restore_code=restore_code)
        except User.DoesNotExist:
            raise Http404
        if form.is_valid():
            user.set_password(form.cleaned_data.get('password'))
            user.restore_code = None
            user.save()
            messages.success(request, _("Se ha establecido la nueva contraseña"))
            return redirect(reverse("users:sign-in"))
        data = {
            "user": user,
            "restore_code": restore_code,
            "form": form
        }
        return render(request, "users/restore.html", data)


class RequestRestorePasswordView(View):

    @staticmethod
    def get(request):
        data = {
            "form": RequestRestoreCodeForm()
        }
        return render(request, "users/request_code.html", data)

    @staticmethod
    def post(request):
        form = RequestRestoreCodeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, _("No se ha encontrado el correo electrónico."))
                return redirect("users:request-restore-password")
            user.send_restore_password_link()
            messages.success(request, _("Se ha enviado un correo a tu dirección "
                                        "con un enlace para establecer tu contraseña."))
        data = {
            "form": form
        }
        return render(request, "users/request_code.html", data)
