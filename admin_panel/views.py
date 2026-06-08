from django.shortcuts import render

from railway_management.decorators import admin_required
from common.common_util import *
from django.http import *
from railway_management.encryption import *
from railway_app.models import *

@admin_required
def admin_dashboard(request):
    print('admin dashboard========>')
    print("SESSION =", dict(request.session))
    return render(request, 'admin/admin_dashboard.html')


def user_list(request):
    context = {}

    query = """SELECT USER_ID, FULL_NAME, USERNAME, EMAIL, MOBILE, ROLE, PASSWORD, CREATED_AT FROM USERS"""
    print('query ============>', query)
    result = select_query(query)
    print('result ============>', result)

    context['users_result'] = result


    return render(request, 'admin/user_management.html', context)

from cryptography.fernet import Fernet
def user_inline_update(request):
    print('user inline update ==========>')
    if request.method ==  'POST':
        user_id = request.POST.get('USER_ID')
        fullname = request.POST.get('FULL_NAME')
        mobile = request.POST.get('MOBILE')
        role = request.POST.get('ROLE')
        email = request.POST.get('EMAIL')
        password =  request.POST.get('PASSWORD')



        if password:
            encrypted_password = encrypt_data(password)

            query = f"""
            UPDATE USERS
            SET
                FULL_NAME='{fullname}',
                EMAIL='{email}',
                MOBILE='{mobile}',
                ROLE='{role}',
                PASSWORD='{encrypted_password}'
            WHERE USER_ID='{user_id}'
            """
        else:
            query = f"""
            UPDATE USERS
            SET
                FULL_NAME='{fullname}',
                EMAIL='{email}',
                MOBILE='{mobile}',
                ROLE='{role}'
            WHERE USER_ID='{user_id}'
            """
        print('query ============>', query)
        result = execute_query(query)
        print('result ============>', result)

        return JsonResponse({
            'status': 1,
            'msg': 'User Updated Successfully'
        })

    return JsonResponse({
        'status': 0,
        'msg': 'Invalid Request'
    })


def delete_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('USER_ID')

        query = f""" DELETE FROM USERS WHERE USER_ID='{user_id}'"""
        result = execute_query(query)
        return JsonResponse({
            'status':1,
            'msg':'User Deleted Successfully'
        })

    return JsonResponse({
        'status':0,
        'msg':'Invalid Request'
    })


# def add_train_form(request):
#     return render(request, 'admin/train_management/train_form.html')


def add_train_form(request):
    print("User =", request.user)
    print("Authenticated =", request.user.is_authenticated)
    if request.method == "POST":
        response = {
            "status": 200,
            "msg": "Train Added Successfully"
        }
        try:
            train_data = {}
            for field in Train._meta.fields:
                field_name = field.name
                if field_name == "TRAIN_ID":
                    continue
                train_data[field_name] = request.POST.get(field_name)
            Train.objects.create(**train_data)

        except Exception as e:

            response["status"] = 0
            response["msg"] = str(e)

        return JsonResponse(response)

    # ========================= GET ========================= #
    fields = []
    for field in Train._meta.fields:
        if field.name == "TRAIN_ID":
            continue
        fields.append({
            "name": field.name,
            "type": field.get_internal_type()
        })

    context = {
        "fields": fields
    }

    return render(request, 'admin/train_management/train_form.html', context)




# Create your views here.
