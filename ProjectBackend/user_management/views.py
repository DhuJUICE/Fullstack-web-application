from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from user_management.models import UserProfile
from django.utils import timezone
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

#mailgun email api import
import requests
from django.conf import settings

#imports for handling verification code generation
import random
import string
import time

from django.shortcuts import get_object_or_404

def homepage(request):
    return render(request, 'homepage.html')
    user = request.user  # Access the logged-in user
    if user.is_authenticated:
        # The user is logged in
        userProfile = UserProfile.objects.get(user=user)
        role = userProfile.role
        if role == "adminUser":
            response = {"userRole":role}
        elif role == "moderatorUser":
            response = {"userRole":role}   
        elif role == "educatorUser":
            response = {"userRole":role}

        return render(request, 'homepage.html', response)

    else:
        # The user is not logged in
        return render(request, 'homepage.html')

    #context = {
    #    'url': 'http://127.0.0.1:8000',
    #    'link_text': 'Click here',
    #}

    return render(request, 'homepage.html')

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
    # Only allow POST requests
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    # Get the username or email and password from the user
    username_or_email = request.POST.get('username_or_email')
    password = request.POST.get('password')

    # Try to authenticate based on email or username
    user = None
    if '@' in username_or_email:
        # Attempt to get the user by email
        try:
            email_user = User.objects.get(email=username_or_email)
            user = auth.authenticate(username=email_user.username, password=password)
        except User.DoesNotExist:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
    else:
        # Attempt to authenticate using username directly
        user = auth.authenticate(username=username_or_email, password=password)

    if user is not None:
        # Securely log in the user
        auth.login(request, user)

        if user.is_authenticated:
            userProfile = UserProfile.objects.get(user=user)
            role = userProfile.role
            response = {
                'message': "User logged in successfully",
                'userRole': role,
				'username':user.username
            }
            return JsonResponse(response, status=200)
        else:
            return JsonResponse({"error": "User not authenticated"}, status=401)
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

#register new users of the system
def registerUser(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        # Load JSON data from the request body
        data = json.loads(request.body)
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confPassword = data.get('confirmpassword')

        # Check to see if the username is taken already
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)

        # Check to see if email is taken already
        elif User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already taken"}, status=400)

        # Check to see if the two passwords are the same
        elif password != confPassword:
            return JsonResponse({"error": "Passwords do not match - Try again"}, status=400)

        else:
            # Create a user object to hold the data for a new user
            user = User.objects.create_user(
                first_name=firstname,
                last_name=lastname,
                username=username,
                email=email,
                password=password
            )

            # Save the new user data to the database
            user.save()

            return JsonResponse({"message": "User registered successfully"}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

#function to logout of user account
def logout(request):
    auth.logout(request)

    return JsonResponse({"message": "User logged out successfully"}, status=200)


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

#function to reset password using your email
def resetPassword(request):
    # Check if the request method is POST
    if request.method == "POST":
        # Get email from user to send verification code to
        email = request.POST.get('email')

        # Check if the user with that email exists
        if User.objects.filter(email=email).exists():
            print("Email exists, You can get a verification code")

            # Generate and get the generated code
            code, timestamp = generate_verification_code()

            # Output code and timestamp
            print("Verification Code: ", code, "\nGenerated Timestamp: ", timestamp, "\n")

            # Save this code & timestamp into that user's UserProfile object
            user = get_object_or_404(User, email=email)
            userProfile = get_object_or_404(UserProfile, user=user)
            userProfile.verificationCode = code
            userProfile.codeTimestamp = timestamp
            userProfile.save()

            # Send email to the user's email with the newly generated verification code
            EmailVerificationCode(email, code)

            # Prepare JSON response
            response = {"message": "Verification code sent to your email.", "email": email, 'code':code}
            return JsonResponse(response, status=200)

        # If user does not exist
        else:
            # Give response that no user is registered with that email
            response = {"error": "No user registered with that email."}
            return JsonResponse(response, status=404)

    # If the request method is not POST
    else:
        response = {"error": "Invalid request method."}
        return JsonResponse(response, status=400)




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

def validateCodePage(request):
    return render(request, 'resetPasswordCode.html', {'email':'james@gmail.com'})

#function to validate verification code - WHEN USER ENTERS THE CODE
def validate_verification_code(request):
    # Check if the request method is POST
    if request.method == "POST":
        code = request.POST.get('code')
        email = request.POST.get('email')

        # Try to get the user
        user = get_object_or_404(User, email=email)

        # Check if the user profile exists
        userProfile = UserProfile.objects.filter(user=user).first()

        # Check if the user profile exists and if the verification code matches
        if userProfile is None:
            response = {"error": "User profile not found."}
            return JsonResponse(response, status=404)

        # Check if the verification code is valid
        if userProfile.verificationCode != code:
            response = {"error": "Invalid verification code."}
            return JsonResponse(response, status=400)

        # Check if the verification code is expired
        if userProfile.is_code_expired():
            response = {"error": "Verification code expired."}
            return JsonResponse(response, status=400)

        # Code is valid
        response = {"message": "Verification code is valid and verified.", "email": email}
        return JsonResponse(response, status=200)

    # If the request method is not POST
    else:
        response = {"error": "Invalid request method."}
        return JsonResponse(response, status=400)

def changePasswordPage(request):
    return render(request, 'newPassword.html', {'email':'james@gmail.com'})

#function to change user password after verification code is validated
def changePassword(request):
    # Check if the request method is POST
    if request.method == "POST":
        newPassword = request.POST.get('newPassword')
        confirmPassword = request.POST.get('confirmPassword')
        email = request.POST.get('email')

        # Get the user using the email
        user = get_object_or_404(User, email=email)

        if newPassword == confirmPassword:
            # Change the user's password with the hashed version
            user.set_password(newPassword)
            user.save()

            response = {"message": "Password successfully changed."}
            return JsonResponse(response, status=200)
        else:
            response = {"error": "Passwords do not match."}
            return JsonResponse(response, status=400)

    # If the request method is not POST
    else:
        response = {"error": "Invalid request method."}
        return JsonResponse(response, status=400)
 
#function to display update user role page
def updateRolePage(request):
    return render(request, 'updateUser.html')

#function to update user role


@csrf_exempt  # Disable CSRF protection for this view
def updateRole(request):
    if request.method == "POST":
        try:
            # Load JSON data from the request body
            data = json.loads(request.body)
            user_id = data.get('user_id')
            user_role = data.get('role')

            # Get the user and their profile
            user = get_object_or_404(User, id=user_id)
            userProfile = get_object_or_404(UserProfile, user=user)

            # Update the user's role
            userProfile.role = user_role
            userProfile.save()

            response = {'userRole': user_role}
            return JsonResponse(response, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=405)

#function to return the users Role
def userRole(request):
    # Get the logged-in user
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated.'}, status=401)

    try:
        # Get the user's profile
        userProfile = UserProfile.objects.get(user=user)
        userRole = userProfile.role
        return JsonResponse({'userRole': userRole}, status=200)

    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found.'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
