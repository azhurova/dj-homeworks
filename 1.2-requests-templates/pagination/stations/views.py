import csv
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    bus_station = []
    with open(settings.BUS_STATION_CSV, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bus_station.append(row)

    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(bus_station, 10)
    page = paginator.get_page(page_number)

    context = {
        'bus_stations': page.object_list,
        'page': page
    }

    return render(request, 'stations/index.html', context)
