from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'MoneyParce'
    return render(request, 'home/index.html', {
        'template_data': template_data})
def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html',
                  {'template_data': template_data})

def dashboard(request):
    template_data = {}
    template_data['title'] = 'Dashboard'
    return render(request, 'home/dashboard.html',
                  {'template_data': template_data})
