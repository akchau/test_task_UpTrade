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
    path("requisites/physycal_person/", test_func, name="physycal_person"),
    path("requisites/legal_entity/", test_func, name="legal_entity"),
    path("requisites/legal_entity/pay/", test_func, name="legal_entity_pay"),
    path(
        "requisites/physycal_person/pay",
        test_func,

        # адрес для самостоятельного добавления в меню
        name="physycal_person_pay"
    ),

    # адрес для демонстрации работы меню с незарегестрированным адресом
    path("<str:any>/", test_func, name="any"),

]
