from django.shortcuts import redirect

def login_required_custom(view_func):

    def wrapper(request,*args,**kwargs):

        if not request.session.get('USER_ID'):

            return redirect('/')

        return view_func(request,*args,**kwargs)

    return wrapper


def admin_required(view_func):
    print('admin requred============>')
    def wrapper(request, *args, **kwargs):
        role = request.session.get('ROLE')
        
        if role == 'Admin':
            return view_func(request, *args, **kwargs)
        return redirect('/admin/user')
    return wrapper

def user_required(view_fucn):
    def wrapper(request, *args, **kwargs):
        role = request.session.get('ROLE')
        allowed_role = [ 'L1', 'L2', 'L3', 'L4', 'L5']
        if role in allowed_role:
            return view_fucn(request, *args, **kwargs)
        return redirect('/')
    return wrapper
        