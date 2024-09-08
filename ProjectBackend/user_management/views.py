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
	username = request.POST.get('username')
	password = request.POST.get('password')

	#validate and authenticate the User
	user = auth.authenticate(username=username, password=password)
	
	if user is not None:
		#securly log in the user
		auth.login(request, user)
		print("User logged in")
		#get the users is_superuser field from database as an object
		user_to_check = User.objects.get(username=username)
		return redirect("/loginpage")
        
	else:
		print("user does not exist")
		return redirect("/loginpage")

#handle the event of someone is registering to our store
def registerUser(request):
	#get all the customer information to be stored to the database
	firstname = request.POST.get('firstname')
	lastname = request.POST.get('lastname')
	username = request.POST.get('username')
	email = request.POST.get('email')
	password = request.POST.get('password')
	confPassword = request.POST.get('confirmpassword')

	#check to see if the username is taken already
	if User.objects.filter(username=username).exists():
		print("Username already taken")
		#open the register
		return redirect("/loginpage")

	#check to see if email is taken already
	elif User.objects.filter(email=email).exists():
		print("Email already taken")
		#open the register
		return redirect("/loginpage")

	#check to see if the two passwords are the same
	elif password != confPassword:
		print("Passwords do not match - Try again")

		#open the register
		return redirect("/loginpage")
	else:
		print("Passwords match")
		#create a user object to hold the data for a new user
		user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email, password=password)
		
		#save the new user data to the database
		user.save();

		print("created user")
		
		#redirect new user to login page, where user can then log in with their user credentials
		return redirect("/loginpage")

#function to logout of user account
def logout(request):
	auth.logout(request)

	#redirect the user to the login page
	return redirect("/loginpage")

#function to reset forgotten password - will use email with a verification code
def resetPassword(request):
	#get email from user to send verification code to
	#check if the user with that email exists
	#if user exists
		#generate verification code of 8 digits
		#save this code into that users Users UserProfile object
		#save the UserProfile instance with updated verificationCode which is valid for certain amount of time

		#send email to the users email with the newly generated verificationCode(will timeout after some time)

		#allow user to enter the verification code from their email
		#if the code is correct
			#Allow user to update their password
			#save the user instance with new password
			#redirect to log in page
		#if the code is incorrect
			#say code is incorrect and do this till code expires
	#if user does not exist
		#give response that no user is registered with that email
	return None