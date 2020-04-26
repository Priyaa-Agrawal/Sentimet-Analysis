from django.shortcuts import render
from django.http import HttpResponse
from senti.sentianalysis import main_function

# Create your views here.


def index(request):
    return render(request, 'senti/index.html')


def analysis(request):
    input_data = request.POST.get('input_data')
    temp = main_function(input_data)
    context = {
        'sentiment': temp
    }
    return render(request, 'senti/result.html', context)
