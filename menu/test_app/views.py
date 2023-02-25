from django.shortcuts import render


def index(request):
    """
    Главная страница.
    """
    template = "test_app/test_page.html"
    header = 'Главная страница'
    context = {
        'header': header
    }
    return render(request, template, context)


def test_func(request, any=None):
    """
    Любая другая страница с адресом.
    Сюда будет направляться любой запрос
    после клиика по секции меню.
    Адресс страницы содержится в секции.
    """
    header = f'Страница с адресом {request.path}'
    template = "test_app/test_page.html"
    context = {
        'header': header,
    }
    return render(request, template, context)
