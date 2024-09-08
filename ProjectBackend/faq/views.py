from django.shortcuts import render, redirect

#display all the FAQS from database
def displayFaqs(request):
	return redirect("/api/faq/deserial/paginated")