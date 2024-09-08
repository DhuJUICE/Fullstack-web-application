from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from user_management.models import UserProfile

#imports for handling verification code generation
import random
import string
import time

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


#PASSWORD RESET
#function to generate 8 character verification code
def generate_verification_code():
    codeLength = 8
    characters = string.ascii_letters + string.digits  # Includes a-z, A-Z, and 0-9
    code = ''.join(random.choice(characters) for _ in range(codeLength))  # Randomly select characters
    timestamp = time.time()  # Current time in seconds since epoch

    #give back the verification code and the generated timestamp of the code
    return code, timestamp

#reset password page
def resetPasswordPage(request):
	return render(request, 'resetPassword.html')

#function to reset forgotten password - will use email with a verification code
def resetPassword(request):
	#get email from user to send verification code to
	email = request.POST.get('email')		

	#check if the user with that email exists
	if User.objects.filter(email=email).exists():
		print("Email exists, You can get a verification code")

		#generate and get the generated code with timestamp
		code = generate_verification_code()[0]
		timestamp = generate_verification_code()[1]		

		#output code and timestamp
		print("Verification Code: ", code, "\nGenerated Timestamp: ", timestamp, "\n")

		#save this code & timestamp into that users Users UserProfile object		
		user = User.objects.get(email=email)
		userProfile = UserProfile.objects.get(user=user)
		userProfile.verificationCode = code
		userProfile.save()

		#send email to the users email with the newly generated verificationCode(will timeout after some time)
		#sendVerificationCode(email, code)

		displayEmail = {"email":email}
		response = displayEmail

		return render(request, 'resetPasswordCode.html', response)

		#allow user to enter the verification code from their email
		#if the code is correct
			#Allow user to update their password
			#save the user instance with new password
			#redirect to log in page
		#if the code is incorrect
			#say code is incorrect and do this till code expires


	#if user does not exist
	else:
		print("Email does not exist, You CANNOT get a verification code")
		print("No user with that email\n")
		#give response that no user is registered with that email
		return redirect("/resetPasswordPage")

#function to send email to user with verification code
def sendVerificationCode(recipient, code):
	pass