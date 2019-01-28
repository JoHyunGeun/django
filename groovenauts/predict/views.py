from django.shortcuts import render
from .forms import InformationForm
from .Reader import Magellan


def index(request):
    form = InformationForm(request.POST or None, request.FILES or None)
    source = ""
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if instance.sex == 'male':
            a = Magellan('male')
            source = a.predict('media/' + str(instance.picture))
        elif instance.sex == 'female':
            a = Magellan('female')
            source = a.predict('media/' + str(instance.picture))

    context = {
        'form': form, 'source': source
    }
    return render(request, 'predict/index.html', context)