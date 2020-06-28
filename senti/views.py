from django.shortcuts import render
from django.http import HttpResponse
from senti.sentianalysis import main_function
from . import tweet as tw
from . import inputfile as ipf
import os
import datetime


def index(request):
    return render(request, 'senti/index.html')


def textanalysis(request):
    input_data = request.POST.get('input_data')
    filename = request.FILES.get('filename')
    # print(filename)

    try:
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
        
        context = {
            'text': x,
            'sentiment': data[0],
            'graph': data[1][0],
            'cloud': data[1][1]
        }
        return render(request, 'senti/textresult.html', context)
    except ValueError as identifier:
        pass

def tweetanalysis(request):
    tweet = request.POST.get('tweet')
    tweet_no = int(request.POST.get('tweet_no'))
    data = tw.tweetanalysis(tweet,tweet_no)
    context = {
        'sentiment': data[0],
        'piechart': data[1]
    }
    
    return render(request, 'senti/tweetresult.html', context)
