from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from patientzenapi.models import Patient, Provider


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a user
    Method arguments:
      request -- The full HTTP request object
    '''
    email = request.data['email']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=email, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        user = token.user
        data = {
            'valid': True,
            'token': token.key,
            'staff': authenticated_user.is_staff,
            'user': user.id
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new user for authentication
    Method arguments:
      request -- The full HTTP request object
    '''
    account_type = request.data.get('account_type', None)
    email = request.data.get('email', None)
    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)
    password = request.data.get('password', None)

    if account_type is not None \
        and email is not None\
        and first_name is not None \
        and last_name is not None \
        and password is not None:

        if account_type == 'patient':
            street_name = request.data.get('street_name', None)
            if street_name is None:
                return Response(
                    {'message': 'You must provide full address for a patient'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif account_type == 'provider':
            specialty = request.data.get('specialty', None)
            if specialty is None:
                return Response(
                    {'message': 'You must provide a specialty for an provider'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'message': 'Invalid account type. Valid values are \'patient\' or \'provider\''},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create a new user by invoking the `create_user` helper method
            # on Django's built-in User model
            new_user = User.objects.create_user(
                username=request.data['email'],
                email=request.data['email'],
                password=request.data['password'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name']
            )
        except IntegrityError:
            return Response(
                {'message': 'An account with that email address already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        account = None

        if account_type == 'patient':
            account = Patient.objects.create(
                user=new_user,
                DOB=request.data['DOB'],
                phone_number=request.data['phone_number'],
                street_name=request.data['street_name'],
                city=request.data['city'],
                state=request.data['state'],
                zip_code=request.data['zip_code']
            )
        elif account_type == 'provider':
            new_user.is_staff = True
            new_user.save()

            account = Provider.objects.create(
                user=new_user,
                specialty=request.data['specialty'],
                phone_number=request.data['phone_number']
            )


        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=account.user)
        # Return the token to the client
        data = { 'token': token.key, 'staff': new_user.is_staff, 'user':token.user.id }
        return Response(data)

    return Response({'message': 'You must provide email, password, first_name, last_name and account_type'}, status=status.HTTP_400_BAD_REQUEST)