# tree (Menu for Django app)
Решение тестового задания для вакансии Junior Python Backend Developer.

# ТЗ:
Приложение, которое реализует древовидное по следующим условиям:
- Меню реализовано через template tag
- Все, что над выделенным пунктом - развернуто. Первый уровень вложенности под выделенным пунктом тоже развернут.
- Хранится в БД.
- Редактируется в стандартной админке Django.
- Активный пункт меню определяется исходя из URL текущей страницы.
- Меню на одной странице может быть несколько. Они определяются по названию.При клике на меню происходит переход по заданному в нем URL. URL может быть задан как явным образом, так и через named url.
- На отрисовку каждого меню требуется ровно 1 запрос к БД
- Нужен django-app, который позволяет вносить в БД меню (одно или несколько) через админку, и нарисовать на любой нужной странице меню по названию.
 {% draw_menu 'main_menu' %}
- При выполнении задания из библиотек следует использовать только Django и стандартную библиотеку Python.

# Инструменты
- Django
- Python

# Запуск проекта в виртуальном окружении venv


# Реализация
В проекте `menu` два приложения.

`tree` - приложение с меню. Шаблоны для отрисовки меню находятся в папке `menu/tree/templates/tree`. Для редактированиия дизайна шаблонов просто добавьте ваши классы в [шаблонах](https://github.com/akchau/test_task_UpTrade/tree/main/menu/tree/templates/tree). 

В кастомном теге [draw_menu](https://github.com/akchau/test_task_UpTrade/blob/main/menu/tree/templatetags/draw_menu_tag.py#L20) производится запрос к БД и с помощью [шаблонов](https://github.com/akchau/test_task_UpTrade/tree/main/menu/tree/templates/tree) `menu` и `tree` производится отрисовка меню. 

Для подключения кастомного тега добавьте в ваш шаблон `{% load draw_menu_tag %}`. 
(В тестовом приложении в шаблоне [base.html](https://github.com/akchau/test_task_UpTrade/blob/main/menu/test_app/templates/base.html#L2) уже добавлены два меню - `main_menu`, `pay_menu`.
 
`test_app` - приложение для демонстрации меню

`menu` - настройки проекта

Дерево-меню реализовано с помощью связанного списка (см. [menu/tree/models.py](https://github.com/akchau/test_task_UpTrade/blob/main/menu/tree/models.py#L42)) через указание родительской директории для каждой секции `top_section`, и рекурсивного вызова шаблона `tree.html` (см. [menu/tree/templates/tree/includes/tree.html](https://github.com/akchau/test_task_UpTrade/blob/main/menu/tree/templates/tree/includes/tree.html#L8)) в случае нахождения активных родительских категорий текущего уровня для отрисовки вложенного уровня, пока не дойдем до активного уровня. После нахождения активного уронвня, отрисовывается его уровень и один уровень ниже. Это позволяет делать один запрос к БД при загрузке страницы.

# Отображение
Если страница 

# Схема БД
В базе данных есть две таблицы:
- `Menu`- таблица 
    - человекочитаемым заголовком меню `name`
    - название для загрузки в шаблоны `slug`. 
    - Также в этой таблице есть related_field - `sections`. В нем есть записи о всех секциях которые относятся к этому меню. Запсии добавляются при создании секции относящийся к этому меню (см. `Section` ниже). При добавлении новой секции необходимо заполнить поле `menu` - указать к какому меню относится секция. 
- `Section`. - таблица с инфромацией о секциях меню. 
    - `name` - аналогично `Menu`, человекочитаемое имя секции которое будет отображаться.
    - `adress` - адресс секции.
    - 'top_section' - родительский раздел. Если None то секция будет на первом уровне меню. Он всегда развернут

При запросе на отрисовку из любого шаблона проекта передается `slug` меню. отрисовке меню в теге `draw_menu`.
Шаблон `tree.html` рекурсивно вызывается после секции из списка `active_top_sections` пока не дойдет до уровня текущей (активной) секции меню. `top_section` - секция являющаяся родительской. Если родительская секция не будет указана - секция появится в корне меню.


# Подключение к проекту
Для добавления меню в проект необходимо добавить папку `tree` и зарегестрировать новое приложение в `you_project.you_project.settings.py`.
```python
# you_project.you_project.settings.py
INSTALLED_APPS = [
     ...
    'tree.apps.TreeConfig',
```
Проверьте чтобы в настройках проекта был включен поиск шаблонов на уровне приложения. В данном примере подключен поиск шаблонов в папке /templates на уровне проекта и приложения.
```python
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True, # Должно стоять True !!!
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

# Настройка меню через админку
После подключения к проекту перейдите на http://127.0.0.1:8000/admin/ и войдите в админ-зону.
- Нельзя создавать секции с одинаковыми именами в одном меню.
- Нельля задавать `named_url` который не зарегестирован в urlpatterns приложений проекта.
- Для каждого `named_url` можно создать одну ссылку в одном меню.
- Нельзя указывать одно меню, а родительскую секцию из другого.


# Тестовое наполнение БД
В приложении 
```bash
python manage.py loaddata fixtures.json
```

# Дальнейшие улучшения
1. Вместо записи имени а админке из пространства имен, можно сделать поле с предустановленным выбором.
