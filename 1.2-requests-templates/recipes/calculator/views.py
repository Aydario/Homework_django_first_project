from django.shortcuts import render, reverse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

def home_view(request):
    pages = {
        'Главная страница': reverse('home'),
        'Рецепт омлета': reverse('omlet'),
        'Рецепт пасты': reverse('pasta'),
        'Рецепт бутерброда': reverse('buter')
    }
    context = {
      'pages': pages
    }
    return render(request, 'calculator/home.html', context)

def omlet(request):
    servings = int(request.GET.get('servings', 1))
    recipe = DATA['omlet']
    context = {
    'recipe': {k: round((v * servings), 1) for k, v in recipe.items()}
    }
    return render(request, 'calculator/index.html', context)

def pasta(request):
    servings = int(request.GET.get('servings', 1))
    recipe = DATA['pasta']
    context = {
    'recipe': {k: round((v * servings), 1) for k, v in recipe.items()}
    }
    return render(request, 'calculator/index.html', context)

def buter(request):
    servings = int(request.GET.get('servings', 1))
    recipe = DATA['buter']
    context = {
    'recipe': {k: round((v * servings), 1) for k, v in recipe.items()}
    }
    return render(request, 'calculator/index.html', context)
# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
