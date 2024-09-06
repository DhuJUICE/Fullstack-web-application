from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth

# Create your views here.
#this function should validate and authenticate the user
def loginPage(request):
	return render(request, 'login.html')
    
def testPage(request):
    response = {"user name" : "james"}
    return render(request, 'testpage.html', response)

#function-view to get the registration page
def registerPage(request):
	return render(request, 'register.html')

#function-view to get the login buttons navigation
def loginUser(request):	
	#get the username and password from the user
	username = request.POST['username']
	password = request.POST['password']

	#validate and authenticate the User
	user = auth.authenticate(username=username, password=password)
	
	if user is not None:
		#securly log in the user
		auth.login(request, user)
		print("User logged in")
		
		#get the users is_superuser field from database as an object
		user_to_check = User.objects.get(username=username)

		response = {"user name" : user_to_check.username}
        return render(request, 'testpage.html', response)
	else:
		print("user does not exist")
		return redirect("/login")

#handle the event of someone is registering to our store
def registerUser(request):
	#get all the customer information to be stored to the database
	firstname = request.POST['firstname']
	lastname = request.POST['lastname']
	username = request.POST['username']
	email = request.POST['email']
	password = request.POST['password']
	confPassword = request.POST['confirmpassword']

	#check to see if the username is taken already
	if User.objects.filter(username=username).exists():
		print("Username already taken")
		#open the register
		return redirect("/register/")

	#check to see if email is taken already
	elif User.objects.filter(email=email).exists():
		print("Email already taken")
		#open the register
		return redirect("/register/")

	#check to see if the two passwords are the same
	elif password != confPassword:
		print("Passwords do not match - Try again")

		#open the register
		return redirect("/register/")
	else:
		print("Passwords match")
		#create a user object to hold the data for a new user
		user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email, password=password)
		
		#save the new user data to the database
		user.save();

		print("created user")
		
		#redirect new user to login page, where user can then log in with their user credentials
		return redirect("/login")

#function to logout of user account
def logout(request):
	auth.logout(request)

	#redirect the user to the login page
	return redirect("/login")