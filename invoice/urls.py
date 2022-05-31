#  Copyright (c) 2022. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from django.contrib import admin
from django.urls import path
from .views import est_json_customers_url,est_add_client,est_view_tax_estimate_detail, est_apro_cms_page, est_apro_hosting_page, est_apro_it_solutions_page, \
    est_apro_rigs_page, est_products_services_tax_estimates_view, est_export_products_services, \
    est_create_non_tax_invoice, est_tax_update, est_tax_update_record, est_create_tax_invoice, est_list_all_users, \
    est_my_profile, est_delete_tax_estimate, est_tax_estimates_view, est_create_new_account, est_json_users_url, \
    est_logout, est_server_status, createInvoice1, generate_PDF1, SystemStatus, view_PDF1, UserAccount, update1, \
    do_register, JSONEstimatesListView, est_json_customers_list_view, JSONUsersListView, change_password, \
    register_new_account, est_dashboard, updaterecord1, deleteInvoice1, Services, \
    Invoice_List_View_1_date_negative, est_export_customers, est_json_users_list_view, est_export_users, \
    Invoice_List_View_1_date_positive, UserView, est_login, est_change_password
from .views import InvoiceListView2, createInvoice2, generate_PDF2, view_PDF2, deleteInvoice2, logout
from django.conf.urls import include
from .views import export_customers, export_users
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404
from . import views
from django.contrib.auth import views
from django.urls import path


app_name = 'invoice'
urlpatterns = [

    path('invoice-filter-date-negative', Invoice_List_View_1_date_negative.as_view(),
         name="invoice-list-date-negative"),
    path('invoice-filter-date-positive', Invoice_List_View_1_date_positive.as_view(),
         name="invoice-list-date-positive"),
    path('invoicelist', InvoiceListView2.as_view(), name="invoice-list-2"),
    path('users-list', UserView.as_view(), name="users-list"),
    path('create-tax-estimate/', createInvoice1, name="invoice-create-tax-estimate"),
    path('createnotax/', createInvoice2, name="invoice-create-2"),
    path('invoice-detail/<id>', view_PDF1, name='invoice-detail'),
    path('invoice-detail-notax/<id>', view_PDF2, name='invoice-detail-2'),
    path('invoice-download/<id>', generate_PDF1, name='invoice-download'),
    path('invoice-download-notax/<id>', generate_PDF2, name='invoice-download-2'),
    path('invoice-delete/<id>', deleteInvoice1, name='invoice-delete'),
    path('invoice-delete-notax/<id>', deleteInvoice2, name='invoice-delete-2'),
    path('update/<int:id>', update1, name='update'),
    path('update/updaterecord/<int:id>', updaterecord1, name='updaterecord'),
    path('system-status', SystemStatus.as_view(), name='system-status'),

    path('our-services', Services.as_view(), name='our-services'),

    path('export-customers/', export_customers, name='export-customers'),
    path('export-users/', export_users, name='export-users'),

    path("tax-estimates-api", JSONEstimatesListView.as_view(), name='tax-estimates-api'),
    path("users-api", JSONUsersListView.as_view(), name='users-api'),

    path("user-account", UserAccount.as_view(), name='user-account'),

    path('logout/', logout, name='logout'),

    path('register-new-account', register_new_account, name='register-new-account'),
    path('register', do_register, name='register'),

    path('password-change/', change_password, name='password-change'),

    path("", est_dashboard.as_view(), name='dashboard'),
    path("apro-rigs/", est_apro_rigs_page.as_view(), name='apro-rigs'),
    path("apro-it-solutions/", est_apro_it_solutions_page.as_view(), name='apro-it-solutions'),
    path("apro-hosting/", est_apro_hosting_page.as_view(), name='apro-hosting'),
    path("apro-cms/", est_apro_cms_page.as_view(), name='apro-cms'),

    path("sign-in", est_login, name='sign-in'),
    path('sign-out/', est_logout, name='sign-out'),
    path('server-details/', est_server_status.as_view(), name='server-details'),
    path('change-password/', est_change_password, name='change-password'),
    path('export-customers-data/', est_export_customers, name='export-customers-data'),
    path('export-product-service-data/', est_export_products_services, name='export-product-service-data'),

    path('export-users-data/', est_export_users, name='export-users-data'),
    path("customers-api-view/", est_json_customers_list_view.as_view(), name='customers-api-view'),
    path("users-api-view", est_json_users_list_view.as_view(), name='users-api-view'),
    path("customers-api-url/", est_json_customers_url.as_view(), name='customers-api-url'),
    path("users-api-url/", est_json_users_url.as_view(), name='users-api-url'),
    path("create-new-user/", est_create_new_account, name='create-new-user'),
    path("view-estimates/", est_tax_estimates_view.as_view(), name='view-estimates'),
    path("view-products-services-tax-estimates/", est_products_services_tax_estimates_view.as_view(),
         name='view-products-services-tax-estimates'),
    path('view-tax-estimate-detail/<id>', est_view_tax_estimate_detail, name='view-tax-estimate-detail'),
    path('estimate-delete-forever/<id>', est_delete_tax_estimate, name='estimate-delete-forever'),
    path('my-profile-view/', est_my_profile.as_view(), name='my-profile-view'),
    path('view-all-users-list/', est_list_all_users.as_view(), name='view-all-users-list'),
    path('create-new-estimate/', est_create_tax_invoice, name='create-new-estimate'),
    path('create-new-non-tax-estimate/', est_create_non_tax_invoice, name='create-new-non-tax-estimate'),
    path('create-new-client/', est_add_client, name='create-new-client'),


    path('update-record/<int:id>', est_tax_update, name='update-record'),
    path('update-record/updaterecord/<int:id>', est_tax_update_record, name='update-record-a'),



]
