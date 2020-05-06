from django.shortcuts import render
from django.http import HttpResponse
from senti.sentianalysis import main_function
from . import inputfile as ipf
import os
import datetime


def index(request):
    return render(request, 'senti/index.html')


def analysis(request):
    input_data = request.POST.get('input_data')
    filename = request.FILES.get('filename')
    # print(filename)
    if filename is not None:
        file_ext = os.path.splitext(filename.name)[1]
        fname = datetime.datetime.now().strftime("%y%m%d%H%M%S")

        # print(fname, file_ext)
        src = f'media/input/{fname}{file_ext}'
        with open(src, 'wb+') as f:
            for chunk in filename.chunks():
                f.write(chunk)
        x = ipf.all_file(src)
    else:
        x = input_data
    data = main_function(x)
    temp = data[0]

    # print(data[1][0][2:l-2])
    context = {
        'text': x,
        'sentiment': temp,
        'graph': data[1][0],
        'cloud': data[1][1]
    }
    return render(request, 'senti/result.html', context)
