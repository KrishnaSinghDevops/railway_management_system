from django.shortcuts import render
from django.core.paginator import Paginator
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
        
        if not password:
            return JsonResponse({
                'status': 0,
                'msg': 'Password is required'
            })



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
    
    print("EMAIL =", request.session.get('EMAIL'))
    print("FULL_NAME =", request.session.get('FULL_NAME'))
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

def train_tracker(request):

    print('train tracker ==========>')
    context={}
    query = """ SELECT TRAIN_ID, TRAIN_NUMBER, TRAIN_NAME, SOURCE_STATION, DESTINATION_STATION, DEPARTURE_TIME, 
            ARRIVAL_TIME, TOTAL_SEATS, AVAILABLE_SEATS FROM TRAINS"""
    print('=========> query ============>', query)
    result = select_query(query)
    # start pagination
    per_page = 10
    paginator = Paginator(result, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # end pagination
    print('result==============>', result)
    if result:
        context['headers'] = result[0].keys()
    else:
        context['headers'] = []
    context['train_data'] = page_obj
    context['page_obj'] = page_obj

    sql =  """ SELECT PASSWORD FROM USERS WHERE USER_id = '2' """
    # result_sql = select_query(decrypt_data(sql))
    print('result_sql ============>', sql)
    sql_result = select_query(sql)
    print('sql_result ============>', sql_result)
    drt = decrypt_data(sql_result[0]['PASSWORD'])

    print('drt ============>', drt)
    enc = sql_result[0]['PASSWORD']

    first = decrypt_data(enc)
    print("First:", first)

    second = decrypt_data(first)
    print("Second:", second)

    return render(request, 'admin/train_management/train_tracker.html', context)






# Create your views here.
