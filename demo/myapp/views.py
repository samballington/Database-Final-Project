# views.py
from django.shortcuts import render
from .queries import get_all_cuisines, get_restaurants_by_cuisine, get_consumer_preferences

def home(request):
    cuisines = get_all_cuisines()
    selected_cuisines = request.POST.getlist('cuisine') if 'search' in request.POST else []
    sort_by = request.POST.get('sort_by', '')

    if selected_cuisines:
        restaurants = get_restaurants_by_cuisine(selected_cuisines, sort_by)
    else:
        restaurants = []

    # Fetch the top 5 most popular cuisines regardless of user input
    top_cuisines = get_consumer_preferences(summary=True)

    context = {
        'cuisines': cuisines,
        'selected_cuisines': selected_cuisines,
        'restaurants': restaurants,
        'top_cuisines': top_cuisines,
        'sort_by': sort_by
    }
    return render(request, 'home.html', context)
