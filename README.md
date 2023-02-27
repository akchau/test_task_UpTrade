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

# Подключение к проекту
Для добавления меню в проект необходимо скопировать папку `tree` и зарегестрировать новое приложение в `you_project.you_project.settings.py`.
```python
# you_project.you_project.settings.py
INSTALLED_APPS = [
     ...
    'tree.apps.TreeConfig',
```
Проверьте, что в настройках проекта был включен поиск шаблонов на уровне приложения. В данном примере подключен поиск шаблонов в папке /templates на уровне проекта и приложения. Шаблоны меню хранятся [тут](https://github.com/akchau/test_task_UpTrade/tree/main/menu/tree/templates/tree)
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
Выполните миграции
```bash
python manage.py makemigrations
python manage.py migrate
```
Запустите проект
```bash
python manage.py runserver
```
Далее по инструкции ниже наполнить админку.

# Настройка меню через админку
После подключения к проекту перейдите на и войдите в [админ-зону](http://127.0.0.1:8000/admin/).

Правила добавления секций:
- Нельзя создавать секции с одинаковыми именами в одном меню.
- Нельзя создавать секции с одинаковыми `named_url` в одном меню.
- Нельля задавать `named_url` который не зарегестирован в urlpatterns приложений проекта.
- Нельзя указывать одно меню, а родительскую секцию из другого.


# Тестовое наполнение БД
В приложении 
```bash
python manage.py loaddata fixtures.json
```

# Реализация
В проекте `menu` два приложения.

`tree` - приложение с меню. Шаблоны для отрисовки меню находятся в папке `menu/tree/templates/tree`. Для редактированиия дизайна шаблонов просто добавьте ваши классы в [шаблонах](https://github.com/akchau/test_task_UpTrade/tree/main/menu/tree/templates/tree). 
В кастомном теге [draw_menu](https://github.com/akchau/test_task_UpTrade/blob/main/menu/tree/templatetags/draw_menu_tag.py#L20) производится запрос к БД и с помощью [шаблонов](https://github.com/akchau/test_task_UpTrade/tree/main/menu/tree/templates/tree) `menu` и `tree` производится отрисовка меню. 
При запросе на отрисовку из любого шаблона проекта передается `slug` меню. Тег для отрисовки - `draw_menu`. Для подключения кастомного тега добавьте в ваш шаблон `{% load draw_menu_tag %}`. 
(В тестовом приложении в шаблоне [base.html](https://github.com/akchau/test_task_UpTrade/blob/main/menu/test_app/templates/base.html#L2) уже добавлены два меню - `main_menu`, `pay_menu`.
`test_app` - приложение для демонстрации меню. Для демонстрации работы меню в репозитории содержится тестовое приложение. В него уже добавлены адреса.
```python
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
        name="physycal_person_pay"
    ),
    path("<str:any>/", test_func, name="any"),

```
В корне проекта заготовлен файл с дампом тестовой базы `fixtures.json`. В базу добавлены все адреса кроме одного. Этот адрес предлагается добавить вручную для демонстрации процесса добавления.
```python
path(
        "requisites/physycal_person/pay",
        test_func,
        name="physycal_person_pay"
    ),
```

`menu` - настройки проекта

Дерево-меню реализовано с помощью связанного списка (см. [menu/tree/models.py](https://github.com/akchau/test_task_UpTrade/blob/main/menu/tree/models.py#L42)) через указание родительской директории для каждой секции `top_section`, и рекурсивного вызова шаблона `tree.html` (см. [menu/tree/templates/tree/includes/tree.html](https://github.com/akchau/test_task_UpTrade/blob/main/menu/tree/templates/tree/includes/tree.html#L8)) в случае нахождения активных родительских категорий текущего уровня для отрисовки вложенного уровня, пока не дойдем до активного уровня. После нахождения активного уронвня, отрисовывается его уровень и один уровень ниже. Это позволяет делать один запрос к БД при загрузке страницы.

# Отображение
Если меню не определяет активную секцию (напрмер адрес не зарегестирован через панель администратора), то будет отрисован только верхний уровень меню. 
Если меню определит активный уровень, то меню отрисует секцию активного уровня, над ней будут отрисованы секции дочерние активным. Активными считаются узлы дерева, через которые можно дойти до активной секции. Остальные секции первого уровня и все секции ниже (узлы, через которые нельзя попасть в активную секцию) будут свернуты.
Под активным уровнем будет отрисован 1 уровень вниз. Все секции кроме текущей кликабельные.

# Схема БД
В базе данных есть две таблицы:
- `Menu`- таблица 
    - `name` человекочитаемым заголовком меню
    - `slug` название для загрузки в шаблоны. 
    - related_field - `sections` записи о всех секциях которые относятся к этому меню. Запсии добавляются при создании секции относящийся к этому меню (см. `Section` ниже). При добавлении новой секции необходимо заполнить поле `menu` - указать к какому меню относится секция. 
- `Section`. - таблица с инфромацией о секциях меню. 
    - `name` - аналогично `Menu`, человекочитаемое имя секции которое будет отображаться.
    - `adress` - адресс секции.
    - `top_section` - родительский раздел. Если None то секция будет на первом уровне меню. Он всегда развернут
    - `menu` - указание на экземпляр модели Menu.
    - related_field - `down_sections` записи о всех  дочерних секциях которые относятся к этой секции. Запсии добавляются при создании секции относящийся к этой секци как `top_section`. При добавлении новой секции необходимо заполнить поле `top_section` - указать родительскую секцию. Если родительская секция не будет указана - секция появится в корне меню.


# Дальнейшие улучшения
1. Вместо записи имени а админке из пространства имен, можно сделать поле с предустановленным выбором. Вопрос, как автоматизировать передачу всех адресов в словарь.
2. Сделать предварительный разворот меню, чтобы с любого уровня можно было открыть любой вложенный.
