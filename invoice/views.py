#  Copyright (c) 2022. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

# FROM SECTION
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib.auth import login, forms
from django.contrib import messages
from django.views import View
from .models import LineItem1, Invoice1, LineItem2, Invoice2, Customers
from .forms import LineItemFormset1, InvoiceForm1, LineItemFormset2, InvoiceForm2
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import auth
from datetime import datetime
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from django.http import HttpResponseRedirect

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.forms import UserCreationForm

# IMPORT SECTION
import pdfkit
import csv
import bleach
import logging
import psutil
import platform
import socket
import platform
import cgitb

import time
from django.core.serializers import serialize
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth import get_user_model

from django.db.models import Sum




cgitb.enable()
hostname = socket.gethostname()
IPAddress = socket.gethostbyname(hostname)

ALLOWED_TAGS = []
ALLOWED_ATTRIBUTES = {}

#Login Function
def est_login(request):
    request_method = request.method
    if request_method == 'POST':
        user_name = request.POST.get('username', '')
        user_password = request.POST.get('password', '')
        secure_username = bleach.clean(user_name, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True,
                                       strip_comments=True)
        user = auth.authenticate(request, username=secure_username, password=user_password)
        if user is not None:
            auth.login(request, user)
            response = HttpResponseRedirect('/')
            return response
        else:
            return render(request, 'invoice/est-login.html', {'wrong_password': True})
    else:
        return render(request, 'invoice/est-login.html')

#Logout Function
@login_required(login_url="/sign-in")
def est_logout(request):
    auth_logout(request)
    return redirect("/sign-in")

#Dashboard Function
class est_dashboard(LoginRequiredMixin, View):
    login_url = "/sign-in"

    def get(self, *args, **kwargs):
        # start = time.time()
        # time.sleep(1)
        # loadingtime = time.time() - start
        users = User.objects.all().order_by("-id")[:6]
        invoices1 = Invoice1.objects.all().order_by("-id")[:5]
        customers = Customers.objects.all().order_by("-id")[:5]
        lineitem1 = LineItem1.objects.all().order_by("-id")[:6]
        estimate_users_total_count = User.objects.count()
        administrator = User.objects.filter(is_superuser=1).count()
        staff = User.objects.filter(is_staff=1).count()
        tax_estimate_total_count = Invoice1.objects.count()
        context = {
            "title": "APRO Estimate - Dashboard",
            "logo_name": "APRO ESTIMATE",
            "lineitem1": lineitem1,
            "customers":customers,
            "tax_estimate_total_count": tax_estimate_total_count,
            "estimate_users_total_count": estimate_users_total_count,

            "users": users,
            "invoices1": invoices1,
            # "page_render": loadingtime,

            "current_ip_address": IPAddress,
            "total_administrator": administrator,
            "total_staff": staff,
            "user_level": "Administrator",
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "create": "CREATE",
            "tax_estimate": "TAX ESTIMATE",
            "view": "VIEW",
            "tax_view_estimate": "VIEW TAX ESTIMATES",
            "export": "EXPORT",
            "sort_by_date_positive": "SORT BY DATE (+)",
            "sort_by_date_negative": "SORT BY DATE (-)",
            "title_f": "Admin Panel",
            "export_customers_csv": "EXPORT CUSTOMERS AS CSV",
            "export_users": "EXPORT USERS AS CSV",
            "sort": "SORT",
            "system_status": "SYSTEM STATUS",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "logout": "LOGOUT",
            "errors": "Errors",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
        }
        # RENDER AND SHOW OUTPUT TO INVOICE-LIST.HTML
        return render(self.request, "invoice/est-dashboard.html", context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")

        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)

        # import pdb;pdb.set_trace()
        return redirect("invoice:dashboard")

#APRO Rigs Service Page Function
class est_apro_rigs_page(LoginRequiredMixin, View):
    login_url = "/sign-in"

    def get(self, *args, **kwargs):
        # start = time.time()
        # time.sleep(1)
        # loadingtime = time.time() - start
        users = User.objects.all().order_by("-id")[:6]
        invoices1 = Invoice1.objects.all().order_by("-id")[:5]
        estimate_users_total_count = User.objects.count()
        administrator = User.objects.filter(is_superuser=1).count()
        staff = User.objects.filter(is_staff=1).count()
        tax_estimate_total_count = Invoice1.objects.count()

        context = {
            "title": "APRO Estimate - Dashborad",
            "logo_name": "APRO ESTIMATE",

            "tax_estimate_total_count": tax_estimate_total_count,
            "estimate_users_total_count": estimate_users_total_count,

            "users": users,
            "invoices1": invoices1,
            # "page_render": loadingtime,

            "current_ip_address": IPAddress,
            "total_administrator": administrator,
            "total_staff": staff,
            "user_level": "Administrator",
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "create": "CREATE",
            "tax_estimate": "TAX ESTIMATE",
            "view": "VIEW",
            "tax_view_estimate": "VIEW TAX ESTIMATES",
            "export": "EXPORT",
            "sort_by_date_positive": "SORT BY DATE (+)",
            "sort_by_date_negative": "SORT BY DATE (-)",
            "title_f": "Admin Panel",
            "export_customers_csv": "EXPORT CUSTOMERS AS CSV",
            "export_users": "EXPORT USERS AS CSV",
            "sort": "SORT",
            "system_status": "SYSTEM STATUS",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "logout": "LOGOUT",
            "errors": "Errors",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
        }
        # RENDER AND SHOW OUTPUT TO INVOICE-LIST.HTML
        return render(self.request, "invoice/est-apro-rigs.html", context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:dashboard")

#APRO CMS Service Page Function
class est_apro_cms_page(LoginRequiredMixin, View):
    login_url = "/sign-in"

    def get(self, *args, **kwargs):
        # start = time.time()
        # time.sleep(1)
        # loadingtime = time.time() - start
        users = User.objects.all().order_by("-id")[:6]
        invoices1 = Invoice1.objects.all().order_by("-id")[:5]
        estimate_users_total_count = User.objects.count()
        administrator = User.objects.filter(is_superuser=1).count()
        staff = User.objects.filter(is_staff=1).count()
        tax_estimate_total_count = Invoice1.objects.count()

        context = {
            "title": "APRO Estimate - Dashborad",
            "logo_name": "APRO ESTIMATE",

            "tax_estimate_total_count": tax_estimate_total_count,
            "estimate_users_total_count": estimate_users_total_count,

            "users": users,
            "invoices1": invoices1,
            # "page_render": loadingtime,

            "current_ip_address": IPAddress,
            "total_administrator": administrator,
            "total_staff": staff,
            "user_level": "Administrator",
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "create": "CREATE",
            "tax_estimate": "TAX ESTIMATE",
            "view": "VIEW",
            "tax_view_estimate": "VIEW TAX ESTIMATES",
            "export": "EXPORT",
            "sort_by_date_positive": "SORT BY DATE (+)",
            "sort_by_date_negative": "SORT BY DATE (-)",
            "title_f": "Admin Panel",
            "export_customers_csv": "EXPORT CUSTOMERS AS CSV",
            "export_users": "EXPORT USERS AS CSV",
            "sort": "SORT",
            "system_status": "SYSTEM STATUS",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "logout": "LOGOUT",
            "errors": "Errors",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
        }
        # RENDER AND SHOW OUTPUT TO INVOICE-LIST.HTML
        return render(self.request, "invoice/est-apro-cms.html", context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:dashboard")

#APRO Hosting Service Page Function
class est_apro_hosting_page(LoginRequiredMixin, View):
    login_url = "/sign-in"

    def get(self, *args, **kwargs):
        # start = time.time()
        # time.sleep(1)
        # loadingtime = time.time() - start
        users = User.objects.all().order_by("-id")[:6]
        invoices1 = Invoice1.objects.all().order_by("-id")[:5]
        estimate_users_total_count = User.objects.count()
        administrator = User.objects.filter(is_superuser=1).count()
        staff = User.objects.filter(is_staff=1).count()
        tax_estimate_total_count = Invoice1.objects.count()

        context = {
            "title": "APRO Estimate - Dashborad",
            "logo_name": "APRO ESTIMATE",

            "tax_estimate_total_count": tax_estimate_total_count,
            "estimate_users_total_count": estimate_users_total_count,

            "users": users,
            "invoices1": invoices1,
            # "page_render": loadingtime,

            "current_ip_address": IPAddress,
            "total_administrator": administrator,
            "total_staff": staff,
            "user_level": "Administrator",
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "create": "CREATE",
            "tax_estimate": "TAX ESTIMATE",
            "view": "VIEW",
            "tax_view_estimate": "VIEW TAX ESTIMATES",
            "export": "EXPORT",
            "sort_by_date_positive": "SORT BY DATE (+)",
            "sort_by_date_negative": "SORT BY DATE (-)",
            "title_f": "Admin Panel",
            "export_customers_csv": "EXPORT CUSTOMERS AS CSV",
            "export_users": "EXPORT USERS AS CSV",
            "sort": "SORT",
            "system_status": "SYSTEM STATUS",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "logout": "LOGOUT",
            "errors": "Errors",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
        }
        # RENDER AND SHOW OUTPUT TO INVOICE-LIST.HTML
        return render(self.request, "invoice/est-apro-hosting.html", context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:dashboard")

#APRO IT Solutions Service Page Function
class est_apro_it_solutions_page(LoginRequiredMixin, View):
    login_url = "/sign-in"

    def get(self, *args, **kwargs):
        # start = time.time()
        # time.sleep(1)
        # loadingtime = time.time() - start
        users = User.objects.all().order_by("-id")[:6]
        invoices1 = Invoice1.objects.all().order_by("-id")[:5]
        estimate_users_total_count = User.objects.count()
        administrator = User.objects.filter(is_superuser=1).count()
        staff = User.objects.filter(is_staff=1).count()
        tax_estimate_total_count = Invoice1.objects.count()

        context = {
            "title": "APRO Estimate - Dashborad",
            "logo_name": "APRO ESTIMATE",

            "tax_estimate_total_count": tax_estimate_total_count,
            "estimate_users_total_count": estimate_users_total_count,

            "users": users,
            "invoices1": invoices1,
            # "page_render": loadingtime,

            "current_ip_address": IPAddress,
            "total_administrator": administrator,
            "total_staff": staff,
            "user_level": "Administrator",
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "create": "CREATE",
            "tax_estimate": "TAX ESTIMATE",
            "view": "VIEW",
            "tax_view_estimate": "VIEW TAX ESTIMATES",
            "export": "EXPORT",
            "sort_by_date_positive": "SORT BY DATE (+)",
            "sort_by_date_negative": "SORT BY DATE (-)",
            "title_f": "Admin Panel",
            "export_customers_csv": "EXPORT CUSTOMERS AS CSV",
            "export_users": "EXPORT USERS AS CSV",
            "sort": "SORT",
            "system_status": "SYSTEM STATUS",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "logout": "LOGOUT",
            "errors": "Errors",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
        }
        # RENDER AND SHOW OUTPUT TO INVOICE-LIST.HTML
        return render(self.request, "invoice/est-apro-it-solution.html", context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:dashboard")

#Tax Estimates Full List View Function
class est_tax_estimates_view(LoginRequiredMixin, View):
    login_url = "/sign-in"

    def get(self, *args, **kwargs):
        # POPULATE DATA IN DATABASE TO INVOICE-LIST.HTML PAGE WITH ORDER_BY ID
        # SORT BY LATEST ID OR UPDATED ID
        start = time.time()
        time.sleep(0)
        loadingtime = time.time() - start

        invoices1 = Invoice1.objects.all().order_by("-id")
        estimate_users_total_count = User.objects.count()
        administrator = User.objects.filter(is_superuser=1).count()
        staff = User.objects.filter(is_staff=1).count()
        tax_estimate_total_count = Invoice1.objects.count()
        page_render_time = loadingtime

        context = {

            "tax_estimate_total_count": tax_estimate_total_count,
            "estimate_users_total_count": estimate_users_total_count,

            "invoices1": invoices1,
            "page_render": page_render_time,

            "current_ip_address": IPAddress,
            "total_administrator": administrator,
            "total_staff": staff,
            "user_level": "Administrator",
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "create": "CREATE",
            "tax_estimate": "TAX ESTIMATE",
            "view": "VIEW",
            "tax_view_estimate": "VIEW TAX ESTIMATES",
            "export": "EXPORT",
            "sort_by_date_positive": "SORT BY DATE (+)",
            "sort_by_date_negative": "SORT BY DATE (-)",
            "title_f": "Admin Panel",
            "export_customers_csv": "EXPORT CUSTOMERS AS CSV",
            "export_users": "EXPORT USERS AS CSV",
            "sort": "SORT",
            "system_status": "SYSTEM STATUS",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "logout": "LOGOUT",
            "errors": "Errors",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
        }
        # RENDER AND SHOW OUTPUT TO INVOICE-LIST.HTML

        return render(self.request, "invoice/est-tax-estimate-list.html", context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:invoice-list")

    class est_tax_estimates_view(LoginRequiredMixin, View):
        login_url = "/sign-in"

        def get(self, *args, **kwargs):
            # POPULATE DATA IN DATABASE TO INVOICE-LIST.HTML PAGE WITH ORDER_BY ID
            # SORT BY LATEST ID OR UPDATED ID
            start = time.time()
            time.sleep(0)
            loadingtime = time.time() - start

            invoices1 = Invoice1.objects.all().order_by("-id")
            estimate_users_total_count = User.objects.count()
            administrator = User.objects.filter(is_superuser=1).count()
            staff = User.objects.filter(is_staff=1).count()
            tax_estimate_total_count = Invoice1.objects.count()
            page_render_time = loadingtime

            context = {

                "tax_estimate_total_count": tax_estimate_total_count,
                "estimate_users_total_count": estimate_users_total_count,

                "invoices1": invoices1,
                "page_render": page_render_time,

                "current_ip_address": IPAddress,
                "total_administrator": administrator,
                "total_staff": staff,

                "main_title": "APRO ESTIMATE",
                "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
                "css_link_b": "static\css\style.css",
                "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
                "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
                "css_link_e": "static\css\main.css",
                "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
                "title_a": "Dashboard",
                "create": "CREATE",
                "tax_estimate": "TAX ESTIMATE",
                "view": "VIEW",
                "tax_view_estimate": "VIEW TAX ESTIMATES",
                "export": "EXPORT",
                "sort_by_date_positive": "SORT BY DATE (+)",
                "sort_by_date_negative": "SORT BY DATE (-)",
                "title_f": "Admin Panel",
                "export_customers_csv": "EXPORT CUSTOMERS AS CSV",
                "export_users": "EXPORT USERS AS CSV",
                "sort": "SORT",
                "system_status": "SYSTEM STATUS",
                "title_view_users": "View Users",
                "title_create_users": "Create Users",
                "title_change_password": "Change Password",
                "title_i": "Create New Tax Based Estimate",
                "title_j": "More Info",
                "title_k": "View Tax Estimates",
                "logout": "LOGOUT",
                "errors": "Errors",
                "title_m": "Total Users/Administrator/Staff",
                "table_head_a": "CUSTOMER ID",
                "table_head_b": "DATE",
                "table_head_c": "CUSTOMER NAME",
                "table_head_d": "SERVICE TYPE",
                "table_head_e": "GST(%)",
                "table_head_f": "TOTAL",
                "table_head_excluded_GST": "(excluded GST)",
                "table_head_included_GST": "(included GST)",
                "table_head_view": "View",
                "table_head_edit": "Edit",
                "table_head_delete": "Delete",
                "table_head_download": "Download",
            }
            # RENDER AND SHOW OUTPUT TO INVOICE-LIST.HTML

            return render(self.request, "invoice/est-tax-estimate-list.html", context)

        def post(self, request):
            # import pdb;pdb.set_trace()
            invoice1_ids = request.POST.getlist("invoice1_id")
            invoice1_ids = list(map(int, invoice1_ids))
            invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
            # import pdb;pdb.set_trace()
            return redirect("invoice:invoice-list")

#Products & Service Full List View Function
class est_products_services_tax_estimates_view(LoginRequiredMixin, View):
    login_url = "/sign-in"

    def get(self, *args, **kwargs):
        # POPULATE DATA IN DATABASE TO INVOICE-LIST.HTML PAGE WITH ORDER_BY ID
        # SORT BY LATEST ID OR UPDATED ID
        start = time.time()
        time.sleep(0)
        loadingtime = time.time() - start

        lineitem1 = LineItem1.objects.all().order_by("-id")
        estimate_users_total_count = User.objects.count()
        administrator = User.objects.filter(is_superuser=1).count()
        staff = User.objects.filter(is_staff=1).count()
        tax_estimate_total_count = Invoice1.objects.count()
        page_render_time = loadingtime

        context = {

            "tax_estimate_total_count": tax_estimate_total_count,
            "estimate_users_total_count": estimate_users_total_count,

            "lineitem1": lineitem1,
            "page_render": page_render_time,

            "current_ip_address": IPAddress,
            "total_administrator": administrator,
            "total_staff": staff,
            "user_level": "Administrator",
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "create": "CREATE",
            "tax_estimate": "TAX ESTIMATE",
            "view": "VIEW",
            "tax_view_estimate": "VIEW TAX ESTIMATES",
            "export": "EXPORT",
            "sort_by_date_positive": "SORT BY DATE (+)",
            "sort_by_date_negative": "SORT BY DATE (-)",
            "title_f": "Admin Panel",
            "export_customers_csv": "EXPORT CUSTOMERS AS CSV",
            "export_users": "EXPORT USERS AS CSV",
            "sort": "SORT",
            "system_status": "SYSTEM STATUS",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "logout": "LOGOUT",
            "errors": "Errors",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
        }
        # RENDER AND SHOW OUTPUT TO INVOICE-LIST.HTML

        return render(self.request, "invoice/est-products-services-tax-estimate-list.html", context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:invoice-list")

#Server Status Function
class est_server_status(LoginRequiredMixin, View):
    # LOGIN URL /ADMIN/LOGIN/?NEXT=/ADMIN/
    login_url = "/sign-in"

    def get(self, *args, **kwargs):
        # POPULATE DATA IN DATABASE TO INVOICE-LIST.HTML PAGE WITH ORDER_BY ID
        # SORT BY LATEST ID OR UPDATED ID
        invoices1 = Invoice1.objects.all().order_by("-id")
        total_users = User.objects.count()
        administrator = User.objects.filter(is_superuser=1).count()
        staff = User.objects.filter(is_staff=1).count()
        total_count = Invoice1.objects.count()
        system_check = platform.uname()
        System = system_check.system
        Node_Name = system_check.node
        Release = system_check.release
        Version = system_check.version
        Machine = system_check.machine
        Processor = system_check.processor
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        BootYr = bt.year
        BootMn = bt.month
        BootDy = bt.day
        BootHr = bt.hour
        BootMi = bt.minute
        BootSe = bt.second
        PhyCore = psutil.cpu_count(logical=False)
        TotCore = psutil.cpu_count(logical=True)
        cpufreq = psutil.cpu_freq()
        MaxFrequency = cpufreq.max
        MinFrequency = cpufreq.min
        CurrentFrequency = cpufreq.current
        TotalCPUUsage = psutil.cpu_percent()
        start = time.time()
        time.sleep(0)
        loadingtime = time.time() - start
        context = {
            "user_level": "Administrator",
            "system": System,
            "node_name": Node_Name,
            "release": Release,
            "version": Version,
            "machine": Machine,
            "physical_core": PhyCore,
            "maxfrequency": MaxFrequency,
            "minfrequency": MinFrequency,
            "totalcpuusage": TotalCPUUsage,
            "currentfrequency": CurrentFrequency,
            "total_core": TotCore,
            "boot_year": BootYr,
            "boot_hour": BootHr,
            "boot_minute": BootMi,
            "boot_second": BootSe,
            "boot_month": BootMn,
            "boot_day": BootDy,

            "invoices1": invoices1,
            "processor": Processor,
            "total_users": total_users,
            "current_ip_address": IPAddress,
            "total_administrator": administrator,
            "total_staff": staff,
            "total_count": total_count,
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "title_b": "Create Estimate",
            "title_c": "View Estimate",
            "title_d": "Filter by Date (+)",
            "title_e": "Filter by Date (-)",
            "title_f": "Admin Panel",
            "title_g": "Export As CSV",
            "title_h": "System Status",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "title_l": "Logout",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
            "sort": "SORT",
            "page_render": loadingtime,
        }
        # RENDER AND SHOW OUTPUT TO INVOICE-LIST.HTML

        return render(self.request, "invoice/est-server-status.html", context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:system-status")

#Password Change Function
@login_required(login_url="/sign-in")
def est_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'invoice/est-change-password.html', {
        'form': form
    })

#Export Tax Estimates to CSV Format Function
@login_required(login_url="/sign-in")
def est_export_customers(request):
    response_est_export_customers = HttpResponse(content_type="text/csv")

    writer_response_est_export_customers = csv.writer(response_est_export_customers)
    # DATAS TABLE COLUMN NAMES AND EXCEL COLUMN NAMES
    writer_response_est_export_customers.writerow(
        ["Customer ID", "Customer Name", "Estimate Date", "Service Type", "Bill Title", "Total Amount(Exc. GST)",
         "Sub Total(Inc. GST)"])
    for customers in Invoice1.objects.all().values_list("id", "customer", "date", "service_type", "bill_title",
                                                        "total_amount", "subtotal"):
        writer_response_est_export_customers.writerow(customers)

    # ATTACHMENT FILE NAME CUSTOMERS.CSV
    response_est_export_customers["Content-Disposition"] = 'attachment; filename="Customers.csv"'

    return response_est_export_customers

#Export Products & Services to CSV Format Function
@login_required(login_url="/sign-in")
def est_export_products_services(request):
    response_est_export_products_services = HttpResponse(content_type="text/csv")

    writer_response_est_export_products_services = csv.writer(response_est_export_products_services)

    writer_response_est_export_products_services.writerow(
        ["Product/Service ID", "Product/Service Name", "Description", "Quantity", "Rate", "Amount",
         "Customer ID"])
    for products_services in LineItem1.objects.all().values_list("id", "service", "description", "quantity", "rate",
                                                                 "amount", "customer_id"):
        writer_response_est_export_products_services.writerow(products_services)

    response_est_export_products_services["Content-Disposition"] = 'attachment; filename="Products and Services.csv"'

    return response_est_export_products_services

#Users Export to CSV Format Function
@login_required(login_url="/sign-in")
def est_export_users(request):
    # EXPORT SECTION CONTENT TYPE TEXT/CSV

    response_est_export_users = HttpResponse(content_type="text/csv")
    writer_response_est_export_users = csv.writer(response_est_export_users)
    # DATAS TABLE COLUMN NAMES AND EXCEL COLUMN NAMES
    writer_response_est_export_users.writerow(
        ["User ID", "Username", "First Name", "Last Name", "Password", "Email Address", "Last Login", "Super User",
         "Staff", "Active", "Join Date"])
    for users in User.objects.all().values_list("id", "username", "first_name", "last_name", "password", "email",
                                                "last_login", "is_superuser", "is_staff", "is_active", "date_joined"):
        writer_response_est_export_users.writerow(users)

    # ATTACHMENT FILE NAME CUSTOMERS.CSV
    response_est_export_users["Content-Disposition"] = 'attachment; filename="Users.csv"'

    return response_est_export_users

#JSON VIEW
class est_json_customers_list_view(LoginRequiredMixin, View):
    login_url = "/sign-in"

    def get(self, request, *args, **kwargs):
        qs = Invoice1.objects.all()
        data = serialize("json", qs)
        context = {
            "data": data,
            "user_level": "Administrator",
        }
        return render(self.request, "invoice/est-customers-api.html", context)
class est_json_users_list_view(LoginRequiredMixin, View):
    login_url = "/sign-in"

    def get(self, request, *args, **kwargs):
        qs = User.objects.all()
        data = serialize("json", qs)
        context = {
            "data": data,
            "user_level": "Administrator",
        }
        return render(self.request, "invoice/est-users-api.html", context)
class est_json_customers_url(LoginRequiredMixin, View):
    login_url = "/sign-in"

    def get(self, request, *args, **kwargs):
        qs = Invoice1.objects.all()
        data = serialize("json", qs)
        return JsonResponse(data, safe=False)
class est_json_users_url(LoginRequiredMixin, View):
    login_url = "/sign-in"

    def get(self, request, *args, **kwargs):
        qs = User.objects.all()
        data = serialize("json", qs)
        return JsonResponse(data, safe=False)

#Add New User Function
@login_required(login_url="/sign-in")
def est_create_new_account(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('/')

    else:
        f = UserCreationForm()

    return render(request, 'invoice/est-create-new-user.html', {'form': f})

#Delete Tax Estimate Function
@login_required(login_url="/sign-in")
def est_delete_tax_estimate(request, id):
    try:
        record = Invoice1.objects.get(id=id)
        record.delete()
    except:
        messages.info(request, f"The requested id doesnot exists!")

    return redirect("/view-estimates/")

#Profile Page Function
class est_my_profile(LoginRequiredMixin, View):
    login_url = "/sign-in"

    def get(self, *args, **kwargs):
        # POPULATE DATA IN DATABASE TO INVOICE-LIST.HTML PAGE WITH ORDER_BY ID
        # SORT BY LATEST ID OR UPDATED ID
        start = time.time()
        time.sleep(0)
        loadingtime = time.time() - start

        invoices1 = Invoice1.objects.all().order_by("-id")

        total_users = User.objects.count()

        administrator = User.objects.filter(is_superuser=1).count()

        staff = User.objects.filter(is_staff=1).count()

        total_count = Invoice1.objects.count()

        page_render_time = loadingtime

        context = {
            "invoices1": invoices1,
            "page_render": page_render_time,
            "total_users": total_users,
            "current_ip_address": IPAddress,
            "total_administrator": administrator,
            "total_staff": staff,
            "total_count": total_count,
            "user_level": "Administrator",
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "create": "CREATE",
            "tax_estimate": "TAX ESTIMATE",
            "view": "VIEW",
            "tax_view_estimate": "VIEW TAX ESTIMATES",
            "export": "EXPORT",
            "sort_by_date_positive": "SORT BY DATE (+)",
            "sort_by_date_negative": "SORT BY DATE (-)",
            "title_f": "Admin Panel",
            "export_customers_csv": "EXPORT CUSTOMERS AS CSV",
            "export_users": "EXPORT USERS AS CSV",
            "sort": "SORT",
            "system_status": "SYSTEM STATUS",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "logout": "LOGOUT",
            "errors": "Errors",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
        }
        # RENDER AND SHOW OUTPUT TO INVOICE-LIST.HTML

        return render(self.request, "invoice/est-view-profile.html", context)

    def post(self, redirect):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:user-account")

#List Users Function
class est_list_all_users(LoginRequiredMixin, View):
    login_url = "/sign-in"

    def get(self, *args, **kwargs):
        start = time.time()
        time.sleep(0)
        loadingtime = time.time() - start
        users = User.objects.all().order_by("-id")
        aaa = Invoice1.objects.all().aggregate(Sum('subtotal'))
        print(aaa)
        invoices1 = Invoice1.objects.all().order_by("-id")[:5]
        estimate_users_total_count = User.objects.count()
        administrator = User.objects.filter(is_superuser=1).count()
        staff = User.objects.filter(is_staff=1).count()
        tax_estimate_total_count = Invoice1.objects.count()
        page_render_time = loadingtime

        context = {

            "tax_estimate_total_count": tax_estimate_total_count,
            "estimate_users_total_count": estimate_users_total_count,

            "users": users,
            "invoices1": invoices1,
            "page_render": page_render_time,

            "current_ip_address": IPAddress,
            "total_administrator": administrator,
            "total_staff": staff,
            "user_level": "Administrator",
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "create": "CREATE",
            "tax_estimate": "TAX ESTIMATE",
            "view": "VIEW",
            "tax_view_estimate": "VIEW TAX ESTIMATES",
            "export": "EXPORT",
            "sort_by_date_positive": "SORT BY DATE (+)",
            "sort_by_date_negative": "SORT BY DATE (-)",
            "title_f": "Admin Panel",
            "export_customers_csv": "EXPORT CUSTOMERS AS CSV",
            "export_users": "EXPORT USERS AS CSV",
            "sort": "SORT",
            "system_status": "SYSTEM STATUS",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "logout": "LOGOUT",
            "errors": "Errors",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
        }
        return render(self.request, "invoice/est-view-users.html", context)
@login_required(login_url="/sign-in")

#Tax Estimate Update Functions
def est_tax_update(request, id):
    invoice1 = Invoice1.objects.get(id=id)
    template = loader.get_template("invoice/est-estimate-edit.html")
    context = {
        "invoice1": invoice1,
        "user_level": "Administrator",
    }
    return HttpResponse(template.render(context, request))
@login_required(login_url="/sign-in")
def est_tax_update_record(request, id):
    # CUSTOMER NAME
    customer = request.POST["customername"]
    # BILL TITLE
    bill_title = request.POST["billtitle"]

    # SERVICE TYPE
    service_type = request.POST["service_type"]
    invoice1 = Invoice1.objects.get(id=id)
    invoice1.customer = customer
    invoice1.bill_title = bill_title
    invoice1.service_type = service_type

    invoice1.save()
    messages.info(request, f"The Customer {customer} has been updated successfully!")
    return redirect("/")

#Create New Tax Estimate Function
@login_required(login_url="/sign-in")
def est_create_tax_invoice(request):
    """
    Invoice Generator page it will have Functionality to create new invoices,
    this will be protected view, only admin has the authority to read and make
    changes here.
    """
    start = time.time()
    time.sleep(0)
    loadingtime = time.time() - start

    heading_message = "Apro IT Solutions"
    if request.method == "GET":
        formset = LineItemFormset1(request.GET or None)
        form = InvoiceForm1(request.GET or None)
    elif request.method == "POST":
        formset = LineItemFormset1(request.POST)
        form = InvoiceForm1(request.POST)
        gstpercentageinfloat = form.data["gst"]
        a = float(gstpercentageinfloat) * 100
        b = int(a)
        servicea = form.data["service"]
        # IF CONDITION
        if servicea == "http://apropack.com/assets/apro-rigs.svg":
            terms1 = form.data["termsandconditionsaprorigs"]
            additionalnotes = form.data["fulldescriptionrigs"]
        elif servicea == "http://apropack.com/assets/apro-it.svg":
            terms1 = form.data["termsandconditionsaproitsolutions"]
            additionalnotes = form.data["fulldescriptionit"]
        elif servicea == "http://apropack.com/assets/apro-hosting.svg":
            terms1 = form.data["termsandconditionsaprohosting"]
            additionalnotes = form.data["fulldescriptionaprohosting"]
        else:
            terms1 = form.data["termsandconditionsaprocms"]
            additionalnotes = form.data["fulldescriptioncms"]

        currencycountry = form.data["currency"]
        footerdefault = form.data["footer"]
        defaultval1 = "This estimate specifies the price for"
        defaultval2 = " for your company."
        customernamecleandata = bleach.clean(
            form.data["customer"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        billtitlefrontcleandata = defaultval1
        billtitlebackcleandata = defaultval2
        gstcleandata = bleach.clean(
            gstpercentageinfloat,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        termsandconditioncleandata = bleach.clean(
            terms1,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        additionalnotescleandata = bleach.clean(
            additionalnotes,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        datecleandata = bleach.clean(
            form.data["date"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        servicetypecleandata = bleach.clean(
            form.data["service_type"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        servicecleandata = bleach.clean(
            servicea,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        currencycleandata = bleach.clean(
            currencycountry,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        footercleandata = bleach.clean(
            footerdefault,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        Str1 = billtitlefrontcleandata
        Str2 = servicetypecleandata
        Str3 = billtitlebackcleandata
        abcs = Str1 + " " + Str2 + "" + Str3

        if form.is_valid():
            invoice1 = Invoice1.objects.create(
                customer=customernamecleandata,
                bill_titlefront=billtitlefrontcleandata,
                bill_titleback=billtitlebackcleandata,
                gst=gstcleandata,
                termsandconditions=termsandconditioncleandata,
                fulldescription=additionalnotescleandata,
                bill_title=abcs,
                date=datecleandata,
                service_type=servicetypecleandata,
                gstpercentage=b,
                service=servicecleandata,
                currency=currencycleandata,
                footer=footercleandata,
            )
            # invoice.save()
        if formset.is_valid():
            # import pdb;pdb.set_trace()
            # extract name and other data from each form and save
            total = 0
            for form in formset:
                service = form.cleaned_data.get("service")
                description = form.cleaned_data.get("description")
                quantity = form.cleaned_data.get("quantity")
                rate = form.cleaned_data.get("rate")
                if service and description and quantity and rate:
                    amount = float(rate) * float(quantity)
                    total += amount
                    servicecleandata = bleach.clean(
                        service,
                        tags=ALLOWED_TAGS,
                        attributes=ALLOWED_ATTRIBUTES,
                        strip=False,
                        strip_comments=True,
                    )
                    descriptioncleandata = bleach.clean(
                        description,
                        tags=ALLOWED_TAGS,
                        attributes=ALLOWED_ATTRIBUTES,
                        strip=False,
                        strip_comments=True,
                    )

                    LineItem1(
                        customer=invoice1,
                        service=servicecleandata,
                        description=descriptioncleandata,
                        quantity=quantity,
                        rate=rate,
                        amount=amount,
                    ).save()
            invoice1.total_amount = total
            totala = float(total)
            gsta = float(gstpercentageinfloat)
            gsttotala = totala * gsta
            floata = gsttotala
            format_float = "{:.2f}".format(floata)
            invoice1.gsttotal = format_float
            subtotal = gsttotala + totala
            abc = float(subtotal)
            invoice1.subtotal = abc
            invoice1.save()

            try:
                generate_PDF1(request, id=invoice1.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect("/")
    context = {
        "title": "Invoice Generator",
        "formset": formset,
        "form": form,
        "page_render": loadingtime,
        "user_level": "Administrator",
    }

    return render(request, "invoice/est-create-new-t-estimate.html", context)



# ON DEVELOPMENT

#Add Client Function
@login_required(login_url="/sign-in")
def est_add_client(request):
    """
    Invoice Generator page it will have Functionality to create new invoices,
    this will be protected view, only admin has the authority to read and make
    changes here.
    """
    start = time.time()
    time.sleep(0)
    loadingtime = time.time() - start

    heading_message = "Apro IT Solutions"
    if request.method == "GET":
        formset = LineItemFormset1(request.GET or None)
        form = InvoiceForm1(request.GET or None)
    elif request.method == "POST":
        formset = LineItemFormset1(request.POST)
        form = InvoiceForm1(request.POST)
        gstpercentageinfloat = form.data["gst"]
        a = float(gstpercentageinfloat) * 100
        b = int(a)
        servicea = form.data["service"]
        # IF CONDITION
        if servicea == "http://apropack.com/assets/apro-rigs.svg":
            terms1 = form.data["termsandconditionsaprorigs"]
            additionalnotes = form.data["fulldescriptionrigs"]
        elif servicea == "http://apropack.com/assets/apro-it.svg":
            terms1 = form.data["termsandconditionsaproitsolutions"]
            additionalnotes = form.data["fulldescriptionit"]
        elif servicea == "http://apropack.com/assets/apro-hosting.svg":
            terms1 = form.data["termsandconditionsaprohosting"]
            additionalnotes = form.data["fulldescriptionaprohosting"]
        else:
            terms1 = form.data["termsandconditionsaprocms"]
            additionalnotes = form.data["fulldescriptioncms"]

        currencycountry = form.data["currency"]
        footerdefault = form.data["footer"]
        defaultval1 = "This estimate specifies the price for"
        defaultval2 = " for your company."
        customernamecleandata = bleach.clean(
            form.data["customer"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        billtitlefrontcleandata = defaultval1
        billtitlebackcleandata = defaultval2
        gstcleandata = bleach.clean(
            gstpercentageinfloat,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        termsandconditioncleandata = bleach.clean(
            terms1,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        additionalnotescleandata = bleach.clean(
            additionalnotes,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        datecleandata = bleach.clean(
            form.data["date"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        servicetypecleandata = bleach.clean(
            form.data["service_type"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        servicecleandata = bleach.clean(
            servicea,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        currencycleandata = bleach.clean(
            currencycountry,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        footercleandata = bleach.clean(
            footerdefault,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        Str1 = billtitlefrontcleandata
        Str2 = servicetypecleandata
        Str3 = billtitlebackcleandata
        abcs = Str1 + " " + Str2 + "" + Str3

        if form.is_valid():
            invoice1 = Invoice1.objects.create(
                customer=customernamecleandata,
                bill_titlefront=billtitlefrontcleandata,
                bill_titleback=billtitlebackcleandata,
                gst=gstcleandata,
                termsandconditions=termsandconditioncleandata,
                fulldescription=additionalnotescleandata,
                bill_title=abcs,
                date=datecleandata,
                service_type=servicetypecleandata,
                gstpercentage=b,
                service=servicecleandata,
                currency=currencycleandata,
                footer=footercleandata,
            )
            # invoice.save()
        if formset.is_valid():
            # import pdb;pdb.set_trace()
            # extract name and other data from each form and save
            total = 0
            for form in formset:
                service = form.cleaned_data.get("service")
                description = form.cleaned_data.get("description")
                quantity = form.cleaned_data.get("quantity")
                rate = form.cleaned_data.get("rate")
                if service and description and quantity and rate:
                    amount = float(rate) * float(quantity)
                    total += amount
                    servicecleandata = bleach.clean(
                        service,
                        tags=ALLOWED_TAGS,
                        attributes=ALLOWED_ATTRIBUTES,
                        strip=False,
                        strip_comments=True,
                    )
                    descriptioncleandata = bleach.clean(
                        description,
                        tags=ALLOWED_TAGS,
                        attributes=ALLOWED_ATTRIBUTES,
                        strip=False,
                        strip_comments=True,
                    )

                    LineItem1(
                        customer=invoice1,
                        service=servicecleandata,
                        description=descriptioncleandata,
                        quantity=quantity,
                        rate=rate,
                        amount=amount,
                    ).save()
            invoice1.total_amount = total
            totala = float(total)
            gsta = float(gstpercentageinfloat)
            gsttotala = totala * gsta
            floata = gsttotala
            format_float = "{:.2f}".format(floata)
            invoice1.gsttotal = format_float
            subtotal = gsttotala + totala
            abc = float(subtotal)
            invoice1.subtotal = abc
            invoice1.save()

            try:
                generate_PDF1(request, id=invoice1.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect("/")
    context = {
        "title": "Invoice Generator",
        "formset": formset,
        "form": form,
        "user_level": "Administrator",
        "page_render": loadingtime,
    }

    return render(request, "invoice/est-add-new-client.html", context)

#Single Tax Estimate View Function
@login_required(login_url="/sign-in")
def est_view_tax_estimate_detail(request, id=None):
    invoice1 = get_object_or_404(Invoice1, id=id)
    lineitem1 = invoice1.lineitem1_set.all()
    context = {
        "company": {
            "name": "APRO IT Solutions Pvt. Ltd.",
            "address001": "2nd Floor, Supriya Building, South Junction",
            "address002": "Chalakudy, Kerala - 680307, Tel. +91 62 386 83 058",
            # "phone": "+91 9746344984",
            "website": "www.aproitsolutions.com",
            "email": "info@aproitsolutions.com",
        },
        "invoice_id": invoice1.id,
        "invoice_gst": invoice1.gst,
        "invoice_total": invoice1.total_amount,
        "customer": invoice1.customer,
        "bill_title": invoice1.bill_title,
        "fulldescription": invoice1.fulldescription,
        "termsandconditions": invoice1.termsandconditions,
        "service": invoice1.service,
        "date": invoice1.date,
        "service_type": invoice1.service_type,
        "gstpercentage": invoice1.gstpercentage,
        "subtotal": invoice1.subtotal,
        "gsttotal": invoice1.gsttotal,
        "currency": invoice1.currency,
        "lineitem1": lineitem1,
    }
    return render(request, "invoice/est-view-tax-estimate-detail.html", context)

#Create Non Tax Estimate Section
@login_required(login_url="/sign-in")
def est_create_non_tax_invoice(request):
    """
    Invoice Generator page it will have Functionality to create new invoices,
    this will be protected view, only admin has the authority to read and make
    changes here.
    """
    start = time.time()
    time.sleep(0)
    loadingtime = time.time() - start

    heading_message = "Apro IT Solutions"
    if request.method == "GET":
        formset = LineItemFormset1(request.GET or None)
        form = InvoiceForm1(request.GET or None)
    elif request.method == "POST":
        formset = LineItemFormset1(request.POST)
        form = InvoiceForm1(request.POST)
        gstpercentageinfloat = form.data["gst"]
        a = float(gstpercentageinfloat) * 100
        b = int(a)
        servicea = form.data["service"]
        # IF CONDITION
        if servicea == "http://apropack.com/assets/apro-rigs.svg":
            terms1 = form.data["termsandconditionsaprorigs"]
            additionalnotes = form.data["fulldescriptionrigs"]
        elif servicea == "http://apropack.com/assets/apro-it.svg":
            terms1 = form.data["termsandconditionsaproitsolutions"]
            additionalnotes = form.data["fulldescriptionit"]
        elif servicea == "http://apropack.com/assets/apro-hosting.svg":
            terms1 = form.data["termsandconditionsaprohosting"]
            additionalnotes = form.data["fulldescriptionaprohosting"]
        else:
            terms1 = form.data["termsandconditionsaprocms"]
            additionalnotes = form.data["fulldescriptioncms"]

        currencycountry = form.data["currency"]
        footerdefault = form.data["footer"]
        defaultval1 = "This estimate specifies the price for"
        defaultval2 = " for your company."
        customernamecleandata = bleach.clean(
            form.data["customer"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        billtitlefrontcleandata = defaultval1
        billtitlebackcleandata = defaultval2
        gstcleandata = bleach.clean(
            gstpercentageinfloat,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        termsandconditioncleandata = bleach.clean(
            terms1,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        additionalnotescleandata = bleach.clean(
            additionalnotes,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        datecleandata = bleach.clean(
            form.data["date"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        servicetypecleandata = bleach.clean(
            form.data["service_type"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        servicecleandata = bleach.clean(
            servicea,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        currencycleandata = bleach.clean(
            currencycountry,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        footercleandata = bleach.clean(
            footerdefault,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        Str1 = billtitlefrontcleandata
        Str2 = servicetypecleandata
        Str3 = billtitlebackcleandata
        abcs = Str1 + " " + Str2 + "" + Str3

        if form.is_valid():
            invoice1 = Invoice1.objects.create(
                customer=customernamecleandata,
                bill_titlefront=billtitlefrontcleandata,
                bill_titleback=billtitlebackcleandata,
                gst=gstcleandata,
                termsandconditions=termsandconditioncleandata,
                fulldescription=additionalnotescleandata,
                bill_title=abcs,
                date=datecleandata,
                service_type=servicetypecleandata,
                gstpercentage=b,
                service=servicecleandata,
                currency=currencycleandata,
                footer=footercleandata,
            )
            # invoice.save()
        if formset.is_valid():
            # import pdb;pdb.set_trace()
            # extract name and other data from each form and save
            total = 0
            for form in formset:
                service = form.cleaned_data.get("service")
                description = form.cleaned_data.get("description")
                quantity = form.cleaned_data.get("quantity")
                rate = form.cleaned_data.get("rate")
                if service and description and quantity and rate:
                    amount = float(rate) * float(quantity)
                    total += amount
                    servicecleandata = bleach.clean(
                        service,
                        tags=ALLOWED_TAGS,
                        attributes=ALLOWED_ATTRIBUTES,
                        strip=False,
                        strip_comments=True,
                    )
                    descriptioncleandata = bleach.clean(
                        description,
                        tags=ALLOWED_TAGS,
                        attributes=ALLOWED_ATTRIBUTES,
                        strip=False,
                        strip_comments=True,
                    )

                    LineItem1(
                        customer=invoice1,
                        service=servicecleandata,
                        description=descriptioncleandata,
                        quantity=quantity,
                        rate=rate,
                        amount=amount,
                    ).save()
            invoice1.total_amount = total
            totala = float(total)
            gsta = float(gstpercentageinfloat)
            gsttotala = totala * gsta
            floata = gsttotala
            format_float = "{:.2f}".format(floata)
            invoice1.gsttotal = format_float
            subtotal = gsttotala + totala
            abc = float(subtotal)
            invoice1.subtotal = abc
            invoice1.save()

            try:
                generate_PDF1(request, id=invoice1.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect("/")
    context = {
        "title": "Invoice Generator",
        "formset": formset,
        "form": form,
        "user_level": "Administrator",
        "page_render": loadingtime,
    }

    return render(request, "invoice/est-create-new-n-estimate.html", context)

# LOGOUT SECTION AND REDIRECT REQUEST
# ADMIN LOGIN LINK /ADMIN/LOGIN/?NEXT=/ADMIN/
def logout(request):
    auth_logout(request)
    return redirect("/login")


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'invoice/password_change.html', {
        'form': form
    })


# INVOICE TYPE 2 NO TAX CUSTOMERS
class InvoiceListView2(View):
    def get(self, *args, **kwargs):
        invoices2 = Invoice2.objects.all().order_by("-id")
        context = {
            "invoices2": invoices2,
        }
        return render(self.request, "invoice/invoice-list-2.html", context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice2_ids = request.POST.getlist("invoice2_id")
        invoice2_ids = list(map(int, invoice2_ids))
        invoices2 = Invoice2.objects.filter(id__in=invoice2_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:invoice-list-2")


class JSONEstimatesListView(View):
    def get(self, request, *args, **kwargs):
        qs = Invoice1.objects.all()
        data = serialize("json", qs)
        return JsonResponse(data, safe=False)


class JSONUsersListView(View):
    def get(self, request, *args, **kwargs):
        qs = User.objects.all()
        data = serialize("json", qs)
        return JsonResponse(data, safe=False)


def register_new_account(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('/login')
    else:
        f = UserCreationForm()
    return render(request, 'invoice/register-new-account.html', {'form': f})


def lockout(request, credentials, *args, **kwargs):
    return JsonResponse({"status": "Locked out due to too many login failures"})


def do_register(request):
    request_method = request.method
    if request_method == 'POST':
        user_name = request.POST.get('username', '')
        user_password = request.POST.get('password', '')
        # authenticate user account.
        user = auth.authenticate(request, username=user_name, password=user_password)
        if user is not None:
            # login user account.
            auth.login(request, user)
            response = HttpResponseRedirect('/')
            return response
        else:
            return render(request, 'invoice/register.html', {'wrong_password': True})
    else:
        return render(request, 'invoice/register.html')


# INVOICE TYPE 1 TAX (GST) CUSTOMERS
# INVOICE LIST TYPE 1 VIEW MAIN WITH LOGIN ALSO CHECKED
class InvoiceListView1(LoginRequiredMixin, View):
    # LOGIN URL /ADMIN/LOGIN/?NEXT=/ADMIN/
    login_url = "/login"

    def get(self, *args, **kwargs):
        # POPULATE DATA IN DATABASE TO INVOICE-LIST.HTML PAGE WITH ORDER_BY ID
        # SORT BY LATEST ID OR UPDATED ID
        start = time.time()
        time.sleep(0)
        loadingtime = time.time() - start

        invoices1 = Invoice1.objects.all().order_by("-id")
        total_users = User.objects.count()
        administrator = User.objects.filter(is_superuser=1).count()
        staff = User.objects.filter(is_staff=1).count()
        total_count = Invoice1.objects.count()
        page_render_time = loadingtime

        context = {
            "invoices1": invoices1,
            "page_render": page_render_time,
            "total_users": total_users,
            "current_ip_address": IPAddress,
            "total_administrator": administrator,
            "total_staff": staff,
            "total_count": total_count,
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "create": "CREATE",
            "tax_estimate": "TAX ESTIMATE",
            "view": "VIEW",
            "tax_view_estimate": "VIEW TAX ESTIMATES",
            "export": "EXPORT",
            "sort_by_date_positive": "SORT BY DATE (+)",
            "sort_by_date_negative": "SORT BY DATE (-)",
            "title_f": "Admin Panel",
            "export_customers_csv": "EXPORT CUSTOMERS AS CSV",
            "export_users": "EXPORT USERS AS CSV",
            "sort": "SORT",
            "system_status": "SYSTEM STATUS",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "logout": "LOGOUT",
            "errors": "Errors",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
        }
        # RENDER AND SHOW OUTPUT TO INVOICE-LIST.HTML

        return render(self.request, "invoice/invoice-list.html", context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:invoice-list")


class UserAccount(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, *args, **kwargs):
        # POPULATE DATA IN DATABASE TO INVOICE-LIST.HTML PAGE WITH ORDER_BY ID
        # SORT BY LATEST ID OR UPDATED ID
        start = time.time()
        time.sleep(3)
        loadingtime = time.time() - start

        invoices1 = Invoice1.objects.all().order_by("-id")

        total_users = User.objects.count()

        administrator = User.objects.filter(is_superuser=1).count()

        staff = User.objects.filter(is_staff=1).count()

        total_count = Invoice1.objects.count()

        page_render_time = loadingtime

        context = {
            "invoices1": invoices1,
            "page_render": page_render_time,
            "total_users": total_users,
            "current_ip_address": IPAddress,
            "total_administrator": administrator,
            "total_staff": staff,
            "total_count": total_count,
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "create": "CREATE",
            "tax_estimate": "TAX ESTIMATE",
            "view": "VIEW",
            "tax_view_estimate": "VIEW TAX ESTIMATES",
            "export": "EXPORT",
            "sort_by_date_positive": "SORT BY DATE (+)",
            "sort_by_date_negative": "SORT BY DATE (-)",
            "title_f": "Admin Panel",
            "export_customers_csv": "EXPORT CUSTOMERS AS CSV",
            "export_users": "EXPORT USERS AS CSV",
            "sort": "SORT",
            "system_status": "SYSTEM STATUS",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "logout": "LOGOUT",
            "errors": "Errors",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
        }
        # RENDER AND SHOW OUTPUT TO INVOICE-LIST.HTML

        return render(self.request, "invoice/user-account.html", context)

    def post(self, redirect):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:user-account")


class Services(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, *args, **kwargs):
        # POPULATE DATA IN DATABASE TO INVOICE-LIST.HTML PAGE WITH ORDER_BY ID
        # SORT BY LATEST ID OR UPDATED ID
        invoices1 = Invoice1.objects.all().order_by("-id")
        total_users = User.objects.count()
        administrator = User.objects.filter(is_superuser=1).count()
        staff = User.objects.filter(is_staff=1).count()
        total_count = Invoice1.objects.count()

        context = {
            "invoices1": invoices1,
            "total_users": total_users,
            "current_ip_address": IPAddress,
            "total_administrator": administrator,
            "total_staff": staff,
            "total_count": total_count,
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "create": "CREATE",
            "tax_estimate": "TAX ESTIMATE",
            "view": "VIEW",
            "tax_view_estimate": "VIEW TAX ESTIMATES",
            "export": "EXPORT",
            "sort_by_date_positive": "SORT BY DATE (+)",
            "sort_by_date_negative": "SORT BY DATE (-)",
            "title_f": "Admin Panel",
            "export_customers_csv": "EXPORT CUSTOMERS AS CSV",
            "export_users": "EXPORT USERS AS CSV",
            "sort": "SORT",
            "system_status": "SYSTEM STATUS",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "logout": "LOGOUT",
            "errors": "Errors",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
        }
        # RENDER AND SHOW OUTPUT TO INVOICE-LIST.HTML
        return render(self.request, "invoice/our-services.html", context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:invoice-services")


class SystemStatus(LoginRequiredMixin, View):
    # LOGIN URL /ADMIN/LOGIN/?NEXT=/ADMIN/
    login_url = "/login"

    def get(self, *args, **kwargs):
        # POPULATE DATA IN DATABASE TO INVOICE-LIST.HTML PAGE WITH ORDER_BY ID
        # SORT BY LATEST ID OR UPDATED ID
        invoices1 = Invoice1.objects.all().order_by("-id")
        total_users = User.objects.count()
        administrator = User.objects.filter(is_superuser=1).count()
        staff = User.objects.filter(is_staff=1).count()
        total_count = Invoice1.objects.count()
        system_check = platform.uname()
        System = system_check.system
        Node_Name = system_check.node
        Release = system_check.release
        Version = system_check.version
        Machine = system_check.machine
        Processor = system_check.processor
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        BootYr = bt.year
        BootMn = bt.month
        BootDy = bt.day
        BootHr = bt.hour
        BootMi = bt.minute
        BootSe = bt.second
        PhyCore = psutil.cpu_count(logical=False)
        TotCore = psutil.cpu_count(logical=True)
        cpufreq = psutil.cpu_freq()
        MaxFrequency = cpufreq.max
        MinFrequency = cpufreq.min
        CurrentFrequency = cpufreq.current
        TotalCPUUsage = psutil.cpu_percent()
        start = time.time()
        time.sleep(0)
        loadingtime = time.time() - start
        context = {
            "physical_core": PhyCore,
            "maxfrequency": MaxFrequency,
            "minfrequency": MinFrequency,
            "totalcpuusage": TotalCPUUsage,
            "currentfrequency": CurrentFrequency,
            "total_core": TotCore,
            "boot_year": BootYr,
            "boot_hour": BootHr,
            "boot_minute": BootMi,
            "boot_second": BootSe,
            "boot_month": BootMn,
            "boot_day": BootDy,
            "invoices1": invoices1,
            "system": System,
            "node_name": Node_Name,
            "release": Release,
            "version": Version,
            "machine": Machine,

            "processor": Processor,
            "total_users": total_users,
            "current_ip_address": IPAddress,
            "total_administrator": administrator,
            "total_staff": staff,
            "total_count": total_count,
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "title_b": "Create Estimate",
            "title_c": "View Estimate",
            "title_d": "Filter by Date (+)",
            "title_e": "Filter by Date (-)",
            "title_f": "Admin Panel",
            "title_g": "Export As CSV",
            "title_h": "System Status",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "title_l": "Logout",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
            "sort": "SORT",
            "page_render": loadingtime,
        }
        # RENDER AND SHOW OUTPUT TO INVOICE-LIST.HTML

        return render(self.request, "invoice/system-status.html", context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:system-status")


class UserView(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, *args, **kwargs):
        start = time.time()
        time.sleep(0)
        loadingtime = time.time() - start

        invoices1 = Invoice1.objects.all().order_by("-id")
        total_users = User.objects.count()
        administrator = User.objects.filter(is_superuser=1).count()
        staff = User.objects.filter(is_staff=1).count()
        total_count = Invoice1.objects.count()
        page_render_time = loadingtime

        User = get_user_model()
        users = User.objects.all()
        print(users)
        context = {

            "invoices1": invoices1,
            "user": users,
            "total_users": total_users,
            "total_administrator": administrator,
            "total_staff": staff,
            "total_count": total_count,
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "title_b": "Create Estimate",
            "title_c": "View Estimate",
            "title_d": "Filter by Date (+)",
            "title_e": "Filter by Date (-)",
            "title_f": "Admin Panel",
            "title_g": "Export As CSV",
            "title_h": "System Status",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "title_l": "Logout",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "User ID",
            "table_head_b": "First Name",
            "table_head_c": "Last Name",
            "table_head_username": "Username",
            "table_head_d": "User Email Address",
            "table_head_e": "Encrypted Password",
            "table_head_f": "Super Admin",
            "table_head_g": "Staff",
            "table_head_active": "Account Active",
            "table_head_join": "Joined Date",
            "table_head_last_login": "Last Login",
        }
        return render(self.request, "invoice/users.html", context)


class Invoice_List_View_1_date_negative(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, *args, **kwargs):
        invoices1 = Invoice1.objects.all().order_by("-date")
        total_users = User.objects.count()
        administrator = User.objects.filter(is_superuser=1).count()
        staff = User.objects.filter(is_staff=1).count()
        total_count = Invoice1.objects.count()
        start = time.time()
        time.sleep(3)
        loadingtime = time.time() - start
        context = {
            "invoices1": invoices1,
            "page_render": loadingtime,
            "total_users": total_users,
            "current_ip_address": IPAddress,
            "total_administrator": administrator,
            "total_staff": staff,
            "total_count": total_count,
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "create": "CREATE",
            "tax_estimate": "TAX ESTIMATE",
            "view": "VIEW",
            "tax_view_estimate": "VIEW TAX ESTIMATES",
            "export": "EXPORT",
            "sort_by_date_positive": "SORT BY DATE (+)",
            "sort_by_date_negative": "SORT BY DATE (-)",
            "title_f": "Admin Panel",
            "export_customers_csv": "EXPORT CUSTOMERS AS CSV",
            "export_users": "EXPORT USERS AS CSV",
            "sort": "SORT",
            "system_status": "SYSTEM STATUS",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "logout": "LOGOUT",
            "errors": "Errors",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
        }

        return render(self.request, "invoice/invoice-list-date-negative.html", context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:invoice-list-date-negative")


class Invoice_List_View_1_date_positive(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, *args, **kwargs):
        invoices1 = Invoice1.objects.all().order_by("date")
        total_users = User.objects.count()
        administrator = User.objects.filter(is_superuser=1).count()
        staff = User.objects.filter(is_staff=1).count()
        total_count = Invoice1.objects.count()
        start = time.time()
        time.sleep(3)
        loadingtime = time.time() - start
        context = {
            "invoices1": invoices1,
            "page_render": loadingtime,
            "total_users": total_users,
            "current_ip_address": IPAddress,
            "total_administrator": administrator,
            "total_staff": staff,
            "total_count": total_count,
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "css_link_e": "static\css\main.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "create": "CREATE",
            "tax_estimate": "TAX ESTIMATE",
            "view": "VIEW",
            "tax_view_estimate": "VIEW TAX ESTIMATES",
            "export": "EXPORT",
            "sort_by_date_positive": "SORT BY DATE (+)",
            "sort_by_date_negative": "SORT BY DATE (-)",
            "title_f": "Admin Panel",
            "export_customers_csv": "EXPORT CUSTOMERS AS CSV",
            "export_users": "EXPORT USERS AS CSV",
            "sort": "SORT",
            "system_status": "SYSTEM STATUS",
            "title_view_users": "View Users",
            "title_create_users": "Create Users",
            "title_change_password": "Change Password",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "logout": "LOGOUT",
            "errors": "Errors",
            "title_m": "Total Users/Administrator/Staff",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
        }
        return render(self.request, "invoice/invoice-list-date-positive.html", context)

    @login_required(login_url="/admin/login/?next=/admin/")
    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:invoice-list-date-positive")


@login_required(login_url="/login")
def createInvoice1(request):
    """
    Invoice Generator page it will have Functionality to create new invoices,
    this will be protected view, only admin has the authority to read and make
    changes here.
    """
    start = time.time()
    time.sleep(0)
    loadingtime = time.time() - start

    heading_message = "Apro IT Solutions"
    if request.method == "GET":
        formset = LineItemFormset1(request.GET or None)
        form = InvoiceForm1(request.GET or None)
    elif request.method == "POST":
        formset = LineItemFormset1(request.POST)
        form = InvoiceForm1(request.POST)
        gstpercentageinfloat = form.data["gst"]
        a = float(gstpercentageinfloat) * 100
        b = int(a)
        servicea = form.data["service"]
        # IF CONDITION
        if servicea == "http://apropack.com/assets/apro-rigs.svg":
            terms1 = form.data["termsandconditionsaprorigs"]
            additionalnotes = form.data["fulldescriptionrigs"]
        elif servicea == "http://apropack.com/assets/apro-it.svg":
            terms1 = form.data["termsandconditionsaproitsolutions"]
            additionalnotes = form.data["fulldescriptionit"]
        elif servicea == "http://apropack.com/assets/apro-hosting.svg":
            terms1 = form.data["termsandconditionsaprohosting"]
            additionalnotes = form.data["fulldescriptionaprohosting"]
        else:
            terms1 = form.data["termsandconditionsaprocms"]
            additionalnotes = form.data["fulldescriptioncms"]

        currencycountry = form.data["currency"]
        footerdefault = form.data["footer"]
        defaultval1 = "This estimate specifies the price for"
        defaultval2 = " for your company."
        customernamecleandata = bleach.clean(
            form.data["customer"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        billtitlefrontcleandata = defaultval1
        billtitlebackcleandata = defaultval2
        gstcleandata = bleach.clean(
            gstpercentageinfloat,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        termsandconditioncleandata = bleach.clean(
            terms1,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        additionalnotescleandata = bleach.clean(
            additionalnotes,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        datecleandata = bleach.clean(
            form.data["date"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        servicetypecleandata = bleach.clean(
            form.data["service_type"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        servicecleandata = bleach.clean(
            servicea,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        currencycleandata = bleach.clean(
            currencycountry,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        footercleandata = bleach.clean(
            footerdefault,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        Str1 = billtitlefrontcleandata
        Str2 = servicetypecleandata
        Str3 = billtitlebackcleandata
        abcs = Str1 + " " + Str2 + "" + Str3

        if form.is_valid():
            invoice1 = Invoice1.objects.create(
                customer=customernamecleandata,
                bill_titlefront=billtitlefrontcleandata,
                bill_titleback=billtitlebackcleandata,
                gst=gstcleandata,
                termsandconditions=termsandconditioncleandata,
                fulldescription=additionalnotescleandata,
                bill_title=abcs,
                date=datecleandata,
                service_type=servicetypecleandata,
                gstpercentage=b,
                service=servicecleandata,
                currency=currencycleandata,
                footer=footercleandata,
            )
            # invoice.save()
        if formset.is_valid():
            # import pdb;pdb.set_trace()
            # extract name and other data from each form and save
            total = 0
            for form in formset:
                service = form.cleaned_data.get("service")
                description = form.cleaned_data.get("description")
                quantity = form.cleaned_data.get("quantity")
                rate = form.cleaned_data.get("rate")
                if service and description and quantity and rate:
                    amount = float(rate) * float(quantity)
                    total += amount
                    servicecleandata = bleach.clean(
                        service,
                        tags=ALLOWED_TAGS,
                        attributes=ALLOWED_ATTRIBUTES,
                        strip=False,
                        strip_comments=True,
                    )
                    descriptioncleandata = bleach.clean(
                        description,
                        tags=ALLOWED_TAGS,
                        attributes=ALLOWED_ATTRIBUTES,
                        strip=False,
                        strip_comments=True,
                    )

                    LineItem1(
                        customer=invoice1,
                        service=servicecleandata,
                        description=descriptioncleandata,
                        quantity=quantity,
                        rate=rate,
                        amount=amount,
                    ).save()
            invoice1.total_amount = total
            totala = float(total)
            gsta = float(gstpercentageinfloat)
            gsttotala = totala * gsta
            floata = gsttotala
            format_float = "{:.2f}".format(floata)
            invoice1.gsttotal = format_float
            subtotal = gsttotala + totala
            abc = float(subtotal)
            invoice1.subtotal = abc
            invoice1.save()

            try:
                generate_PDF1(request, id=invoice1.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect("/")
    context = {
        "title": "Invoice Generator",
        "formset": formset,
        "form": form,
        "page_render": loadingtime,
    }

    return render(request, "invoice/invoice-create.html", context)


def createInvoice2(request):
    """
    Invoice Generator page it will have Functionality to create new invoices,
    this will be protected view, only admin has the authority to read and make
    changes here.
    """

    heading_message = "Apro IT Solutions"
    if request.method == "GET":
        formset = LineItemFormset2(request.GET or None)
        form = InvoiceForm2(request.GET or None)
    elif request.method == "POST":
        formset = LineItemFormset2(request.POST)
        form = InvoiceForm2(request.POST)

        gstpercentageinfloat = form.data["gst"]
        a = float(gstpercentageinfloat) * 100
        b = int(a)
        servicea = form.data["service"]
        if servicea == "https://www.aprorigs.com/wp-content/uploads/2021/11/logo3.png":
            terms1 = form.data["termsandconditionsaprorigs"]
            additionalnotes = form.data["fulldescriptionrigs"]

        elif (
                servicea
                == "https://aproitsolutions.com/wp-content/uploads/2019/07/apro-logo-for-web-new-dark-1.png"
        ):
            terms1 = form.data["termsandconditionsaproitsolutions"]
            additionalnotes = form.data["fulldescriptionit"]

        elif (
                servicea == "https://aprohosting.com/wp-content/uploads/2021/11/logo-02.png"
        ):
            terms1 = form.data["termsandconditionsaprohosting"]
            additionalnotes = form.data["fulldescriptionaprohosting"]

        else:
            terms1 = form.data["termsandconditionsaprocms"]
            additionalnotes = form.data["fulldescriptioncms"]

        currencycountry = form.data["currency"]
        footerdefault = form.data["footer"]

        if form.is_valid():
            invoice2 = Invoice2.objects.create(
                customer=form.data["customer"],
                bill_title=form.data["bill_title"],
                gst=gstpercentageinfloat,
                termsandconditions=terms1,
                fulldescription=additionalnotes,
                date=form.data["date"],
                service_type=form.data["service_type"],
                gstpercentage=b,
                service=servicea,
                currency=currencycountry,
                footer=footerdefault,
            )

            # invoice.save()

        if formset.is_valid():
            # import pdb;pdb.set_trace()
            # extract name and other data from each form and save
            total = 0

            for form in formset:
                service = form.cleaned_data.get("service")
                description = form.cleaned_data.get("description")
                quantity = form.cleaned_data.get("quantity")
                rate = form.cleaned_data.get("rate")

                if service and description and quantity and rate:
                    amount = float(rate) * float(quantity)

                    total += amount
                    LineItem2(
                        customer=invoice2,
                        service=service,
                        description=description,
                        quantity=quantity,
                        rate=rate,
                        amount=amount,
                    ).save()
            invoice2.total_amount = total
            totala = float(total)
            gsta = float(gstpercentageinfloat)
            gsttotala = totala * gsta
            floata = gsttotala
            format_float = "{:.2f}".format(floata)

            invoice2.gsttotal = format_float
            subtotal = gsttotala + totala
            abc = float(subtotal)
            invoice2.subtotal = abc
            invoice2.save()

            try:
                generate_PDF2(request, id=invoice2.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect("/")
    context = {
        "title": "Invoice Generator",
        "formset": formset,
        "form": form,
    }
    return render(request, "invoice/invoice-create-2.html", context)


def view_PDF1(request, id=None):
    invoice1 = get_object_or_404(Invoice1, id=id)
    lineitem1 = invoice1.lineitem1_set.all()
    context = {
        "company": {
            "name": "APRO IT Solutions Pvt. Ltd.",
            "address001": "2nd Floor, Supriya Building, South Junction",
            "address002": "Chalakudy, Kerala - 680307, Tel. +91 62 386 83 058",
            # "phone": "+91 9746344984",
            "website": "www.aproitsolutions.com",
            "email": "info@aproitsolutions.com",
        },
        "invoice_id": invoice1.id,
        "invoice_gst": invoice1.gst,
        "invoice_total": invoice1.total_amount,
        "customer": invoice1.customer,
        "bill_title": invoice1.bill_title,
        "fulldescription": invoice1.fulldescription,
        "termsandconditions": invoice1.termsandconditions,
        "service": invoice1.service,
        "date": invoice1.date,
        "service_type": invoice1.service_type,
        "gstpercentage": invoice1.gstpercentage,
        "subtotal": invoice1.subtotal,
        "gsttotal": invoice1.gsttotal,
        "currency": invoice1.currency,
        "lineitem1": lineitem1,
    }
    return render(request, "invoice/pdf2oldnew.html", context)


def view_PDF2(request, id=None):
    invoice2 = get_object_or_404(Invoice2, id=id)
    lineitem2 = invoice2.lineitem2_set.all()

    context = {
        "company": {
            "name": "APRO IT Solutions Pvt. Ltd.",
            "address001": "2nd Floor, Supriya Building, South Junction",
            "address002": "Chalakudy, Kerala - 680307, Tel. +91 62 386 83 058",
            # "phone": "+91 9746344984",
            "website": "www.aproitsolutions.com",
            "email": "info@aproitsolutions.com",
        },
        "invoice_id": invoice2.id,
        "invoice_total": invoice2.total_amount,
        "customer": invoice2.customer,
        "bill_title": invoice2.bill_title,
        "fulldescription": invoice2.fulldescription,
        "termsandconditions": invoice2.termsandconditions,
        "service": invoice2.service,
        "date": invoice2.date,
        "service_type": invoice2.service_type,
        "subtotal": invoice2.subtotal,
        "currency": invoice2.currency,
        "lineitem2": lineitem2,
    }
    return render(request, "invoice/pdfout.html", context)


def generate_PDF1(request, id):
    options = {
        "page-size": "A4",
        "margin-top": "0.00in",
        "margin-right": "0.00in",
        "margin-bottom": "0.00in",
        "margin-left": "0.00in",
        "encoding": "UTF-8",
        "custom-header": [("Accept-Encoding", "gzip")],
        "no-outline": None,
    }

    pdf = pdfkit.from_url(
        request.build_absolute_uri(reverse("invoice:invoice-detail", args=[id])),
        False,
        options=options,
    )
    response = HttpResponse(pdf, content_type="application/pdf")

    response["Content-Disposition"] = 'attachment; filename="pdf.pdf"'
    return response


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


# PDF GENERATE SECTION FOR NON TAX CUSTOMERS
def generate_PDF2(request, id):
    options = {
        "page-size": "B4",
        "margin-top": "0.00in",
        "margin-right": "0.00in",
        "margin-bottom": "0.00in",
        "margin-left": "0.00in",
        "encoding": "UTF-8",
        "custom-header": [("Accept-Encoding", "gzip")],
        "no-outline": None,
    }
    # Use False instead of output path to save pdf to a variable
    pdf = pdfkit.from_url(
        request.build_absolute_uri(reverse("invoice:invoice-detail", args=[id])),
        False,
        options=options,
    )
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="pdf.pdf"'
    return response


def change_status1(request):
    return redirect("invoice:invoice-list")


def view_4041(request, *args, **kwargs):
    return redirect("invoice:invoice-list")


# DELETE INVOICE SECTION FOR NON TAX CUSTOMERS
def deleteInvoice2(request, id):
    try:
        record = Invoice2.objects.get(id=id)
        record.delete()
    except:
        messages.info(request, f"The requested id doesnot exists!")
    return redirect("invoice:invoice-list-2")


# DELETE INVOICE SECTION FOR TAX CUSTOMERS
def deleteInvoice1(request, id):
    try:
        record = Invoice1.objects.get(id=id)
        record.delete()
    except:
        messages.info(request, f"The requested id doesnot exists!")
    return redirect("invoice:invoice-list")


# UPDATE RECORD SECTION A
def update1(request, id):
    invoice1 = Invoice1.objects.get(id=id)
    template = loader.get_template("invoice/edittaxcustomers.html")
    context = {
        "invoice1": invoice1,
    }
    return HttpResponse(template.render(context, request))


# UPDATE RECORD SECTION B
def updaterecord1(request, id):
    # CUSTOMER NAME
    customer = request.POST["customername"]
    # BILL TITLE
    bill_title = request.POST["billtitle"]
    # SERVICE TYPE
    service_type = request.POST["service_type"]
    invoice1 = Invoice1.objects.get(id=id)
    invoice1.customer = customer
    invoice1.bill_title = bill_title
    invoice1.service_type = service_type
    invoice1.save()
    messages.info(request, f"The Customer {customer} has been updated successfully!")
    return redirect("/")


# EXPORT SECTION CODE (DATABASE EXPORT TO CSV FILE)
@login_required(login_url="/login")
def export_customers(request):
    response_a = HttpResponse(content_type="text/csv")

    writer_a = csv.writer(response_a)
    # DATAS TABLE COLUMN NAMES AND EXCEL COLUMN NAMES
    writer_a.writerow(
        ["Customer ID", "Customer Name", "Estimate Date", "Service Type", "Bill Title", "Total Amount(Exc. GST)",
         "Sub Total(Inc. GST)"])
    for customers in Invoice1.objects.all().values_list("id", "customer", "date", "service_type", "bill_title",
                                                        "total_amount", "subtotal"):
        writer_a.writerow(customers)

    # ATTACHMENT FILE NAME CUSTOMERS.CSV
    response_a["Content-Disposition"] = 'attachment; filename="Customers.csv"'

    return response_a


@login_required(login_url="/login")
def export_users(request):
    # EXPORT SECTION CONTENT TYPE TEXT/CSV

    response_users = HttpResponse(content_type="text/csv")
    writer_users = csv.writer(response_users)
    # DATAS TABLE COLUMN NAMES AND EXCEL COLUMN NAMES
    writer_users.writerow(
        ["User ID", "Username", "First Name", "Last Name", "Password", "Email Address", "Last Login", "Super User",
         "Staff", "Active", "Join Date"])
    for users in User.objects.all().values_list("id", "username", "first_name", "last_name", "password", "email",
                                                "last_login", "is_superuser", "is_staff", "is_active", "date_joined"):
        writer_users.writerow(users)

    # ATTACHMENT FILE NAME CUSTOMERS.CSV
    response_users["Content-Disposition"] = 'attachment; filename="Users.csv"'

    return response_users
