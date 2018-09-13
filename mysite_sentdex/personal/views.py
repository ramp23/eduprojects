from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'personal/home.html')

def contact(request):
    return render(request, 'personal/basic.html', {'content':['Если вам понравился сайт и вы уже хотите предложить мне стажировку в компании из списка Fortune500, то вот мое мыло: ','ifreeman2398@gmail.com']})
