from django.shortcuts import render, redirect
from django.http import JsonResponse
from railway_management.database import get_connection
from railway_management.encryption import encrypt_data
from railway_management.encryption import decrypt_data
from admin_panel.views import admin_dashboard
from railway_app.views import dashboard

def login_page(request):

    role = request.session.get('ROLE')

    if role == 'Admin':
        return admin_dashboard(request)

    elif role in ['L1', 'L2', 'L3', 'L4', 'L5']:
        return dashboard(request)

    return render(request, 'accounts/login.html')

def register_page(request):
    return render(request, 'accounts/register.html')


def register_save(request):

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        role = request.POST.get('role')
        encrypted_password = encrypt_data(password)
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO USERS (FULL_NAME, USERNAME,  EMAIL, MOBILE, PASSWORD, ROLE)
        VALUES (?,?,?,?,?,?)
        """
        cursor.execute(query, (full_name, username, email, mobile, encrypted_password, role) )
        connection.commit()
        cursor.close()
        connection.close()
        return JsonResponse({

            'status': 'success',
            'message': 'Registration Successful'

        })


def login_user(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT USER_ID,USERNAME,PASSWORD,ROLE
        FROM USERS
        WHERE USERNAME=?
        """

        cursor.execute(query, (username,))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:

            db_password = decrypt_data(user[2])
            print("USER DATA =", user)
            print("ROLE =", user[3])
            print("ENTERED PASSWORD =", password)
            print("DB PASSWORD =", db_password)

            

            if password == db_password:

                request.session['USER_ID'] = user[0]
                request.session['USERNAME'] = user[1]
                request.session['ROLE'] = user[3]

                role = user[3]

                if role == 'Admin':

                    return JsonResponse({
                        'status': 'success',
                        'redirect_url': '/'
                    })

                else:

                    return JsonResponse({
                        'status': 'success',
                        'redirect_url': '/'
                    })
                
                

        return JsonResponse({
            'status': 'error'
        })
def logout_user(request):

    request.session.flush()

    return redirect('/')