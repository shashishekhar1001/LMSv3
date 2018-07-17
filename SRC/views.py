from django.shortcuts import render

# def home(request):
#     if request.method == 'POST':
#         form = ContactForm
#     return render(request, "home.html", {})

def home(request):
    # if request.method == 'POST':
    #     form = ContactForm
    return render(request, "home.html", {})