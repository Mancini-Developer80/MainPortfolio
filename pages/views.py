from django.shortcuts import render

def home(request):
	return render(request, 'index.html')

def projects(request):
	return render(request, 'projects.html')

def about(request):
	return render(request, 'about.html')

def contact(request):
	return render(request, 'contact.html')

def angular_myflix_case(request):
	return render(request, 'angularmyflixcase.html')

def meetapp_case(request):
	return render(request, 'meetappcase.html')

def pokemon_case(request):
	return render(request, 'pokemoncase.html')

def promontolio_case(request):
	return render(request, 'promontoliocase.html')

def myflix_case(request):
	return render(request, 'myflixcase.html')

def jobtracker_case(request):
	return render(request, 'jobtracker.html')
