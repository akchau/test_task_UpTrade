from django.urls import path

from .views import index, test_func

app_name = "test_app"

urlpatterns = [
    path("", index, name="index"),
    path("contacts/", test_func, name="contacts"),
    path("contact_warehouse/", test_func, name="contact_warehouse"),
    path("contact_office/", test_func, name="contact_office"),
    path("contact_accountant/", test_func, name="contact_accountant"),
    path("contact_managers/", test_func, name="contact_managers"),
    path("contact_ceo/", test_func, name="contact_ceo"),
    path("contacts/physycal_person/", test_func, name="physycal_person"),
    path("<str:any>/", test_func, name="any"),
]
