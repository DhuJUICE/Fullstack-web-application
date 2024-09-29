from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from user_management.models import UserProfile
from django.utils import timezone

#mailgun email api import
import requests
from django.conf import settings

#imports for handling verification code generation
import random
import string
import time

def homepage(request):
    context = {
        'url': 'http://127.0.0.1:8000',
        'link_text': 'Click here',
    }
    return render(request, 'homepage.html', context)

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
    # Get the username or email and password from the user
    username_or_email = request.POST.get('username_or_email')
    password = request.POST.get('password')
    print(username_or_email)
    print(password)
    
    # Try to authenticate based on email or username
    if '@' in username_or_email:
        # Attempt to get the user by email
        email_user = User.objects.get(email=username_or_email)
        user = auth.authenticate(username=email_user.username, password=password)
    else:
        # Attempt to authenticate using username directly
        user = auth.authenticate(username=username_or_email, password=password)

    if user is not None:
        # Securely log in the user
        auth.login(request, user)
        print("User logged in")

        if user.is_authenticated:
            userProfile = UserProfile.objects.get(user=user)
            role = userProfile.role
            print("Users Role in real life: ", role)
            #UserPRofile
                #fk#User = user
                #role
                #code
                #image
            response = {'userRole':role}
            return render(request, 'homepage.html', response)
        else:
            print("Something went wrong - log in again")
            return redirect("/loginpage")
    else:
        print("Invalid credentials or user does not exist")
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
    return redirect("/")


#PASSWORD RESET
#function to generate 8 character verification code
def generate_verification_code():
    codeLength = 8
    characters = string.ascii_letters + string.digits  # Includes a-z, A-Z, and 0-9
    code = ''.join(random.choice(characters) for _ in range(codeLength))  # Randomly select characters
    timestamp = timezone.now()  # Current time

    #give back the verification code
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

        #generate and get the generated code
        code = generate_verification_code()[0]
        timestamp = generate_verification_code()[1]		

        #output code and timestamp
        print("Verification Code: ", code, "\nGenerated Timestamp: ", timestamp, "\n")

        #save this code & timestamp into that users Users UserProfile object		
        user = User.objects.get(email=email)
        userProfile = UserProfile.objects.get(user=user)
        userProfile.verificationCode = code
        userProfile.codeTimestamp = timestamp
        userProfile.save()

        #send email to the users email with the newly generated verificationCode(will timeout after some time)
        EmailVerificationCode(email, code)

        response = {"email":email}

        return render(request, 'resetPasswordCode.html', response)

        #allow user to enter the verification code from their email
        #if the code is correct
            #Allow user to update their password
            #save the user instance with new password
            #redirect to log in page
        #if the code is incorrect
            #say code is incorrect 


    #if user does not exist
    else:
        print("Email does not exist, You CANNOT get a verification code")
        print("No user with that email\n")
        #give response that no user is registered with that email
        return redirect("/resetPasswordPage")




#function to send email to user with verification code
def EmailVerificationCode(recipient, code):
    subject = 'verificationCode'
    message = 'Here is your verification code: ' + code

    MAILGUN_API_KEY = settings.MAILGUN_API_KEY
    MAILGUN_DOMAIN = settings.MAILGUN_DOMAIN
    MAILGUN_API_URL = settings.MAILGUN_API_URL

    response = requests.post(
    MAILGUN_API_URL,auth=('api', MAILGUN_API_KEY),data={
    'from': f'postmaster@{MAILGUN_DOMAIN}',
    'to': recipient,
    'subject': subject,
    'text': message
    }
    )
    if response.status_code == 200:
        print("Email sent successfully.")
    else:
        print(f"Failed to send email: {response.status_code} - {response.text}")

#function to validate verification code - WHEN USER ENTERS THE CODE
def validate_verification_code(request):
    code = request.POST.get('code')
    email = request.POST.get('email')

    try:
        user = User.objects.get(email=email)
        userProfile = UserProfile.objects.get(user=user, verificationCode=code)
    except UserProfile.DoesNotExist:
        print("Incorrect/no verification code\n")
        return redirect("/resetPasswordPage")

    if userProfile.is_code_expired():
        print("Verification code expired\n")
        return redirect("/resetPasswordPage")
    response = {"email":email}
    return render(request, 'newPassword.html', response)  # Code is valid

#function to change user password after verification code is validated
def changePassword(request):
    newPassword = request.POST.get('newPassword')
    confirmPassword = request.POST.get('confirmPassword')
    email = request.POST.get('email')

    #get the user using the email
    user = User.objects.get(email=email)

    if newPassword == confirmPassword:
        #change the users password with the hashed version of the text password
        #this helps in terms of authentication
        user.set_password(newPassword)
        user.save()
        print("Password changed")

        return redirect("/loginpage")
    else:
        print("Passwords do not match")
        return render(request, 'newPassword.html')
 
#function to display update user role page
def updateRolePage(request):
    return render(request, 'updateUser.html')

#function to update user role
def updateRole(request):
    userId = request.POST.get('user_id')
    userRole = request.POST.get('role')
    print(str(userId) + " " + userRole)
    response = {'userRole':userRole}

    return render(request, 'homepage.html', response)