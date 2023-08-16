from django.shortcuts import render

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
}


def recept_calculate(request, dish):
    servings = int(request.GET.get('servings', 1))
    if dish in DATA.keys():
        dish_recipe = DATA.get(dish).copy()
        for key in dish_recipe:
            dish_recipe[key] = dish_recipe[key] * servings
    else:
        dish_recipe = None

    context = {
        'recipe': dish_recipe
    }
    return render(request, 'calculator/index.html', context)
