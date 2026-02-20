from django.http import HttpResponse
from django.shortcuts import render,redirect
from datetime import date,datetime, timedelta
import requests
import random
import string
from django.contrib.auth.hashers import make_password,check_password
from .models import *
from django.core.mail import EmailMessage,send_mail
import re



from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# ---------- AGE CALCULATION -----------
def age(customer):
    today=date.today()
    years = today.year - customer.year
    months = today.month - customer.month
    days = today.day - customer.day
    print('months: ', months)

    if today.month < customer.month:
        years= years-1
        months =  months + 12
        if today.day < customer.day:
            days = days + 31
            months = months - 1 
        print('months---: ', months)
    print('years: ', today.month)

    # return f"your age {years} : year  {months} : month  {days} : days"
    return years

# ---------- RANDOM PASSWORD GENRATOR -----------

def random_password(length):
    password=""
    for i in range(length):
        password+=random.choice(
            [
                str(random.randint(0,9)),
                chr(random.choice([random.randint(65,91),random.randint(97,123)]))
            ]
        )
    # pas=string.ascii_letters+string.digits
    # cho=""
    # for i in range(length):
    #     cho+=random.choice(pas)
    # print("--------",cho)
    return password



           


email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|in)$'
def home(request):
    if request.method == "POST" :

        fn=request.POST.get('fn')
        ln=request.POST.get('ln')

        # FETCH GENDER
        url= f"https://api.genderize.io/?name={ln}"
        res=requests.get(url)
        data=res.json()

        # Random password
        passwords=random_password(6)
        print('passwords: ', passwords)
    
        email=request.POST.get('email')
        mobile=request.POST.get('number')
        
        udate=request.POST.get('dates')
        hobby=request.POST.getlist('check[]')
        print('hobby: ', hobby)
        listof_error=[]
        if not fn:
            error="First name was reqired"
            listof_error.append(error)
        if not ln:
            error="Last name was reqired"
            listof_error.append(error)
        if email:   
            if not re.match(email_pattern, email):
                error="Proper email_Id set"
                listof_error.append(error)
        if CustomerRegister.objects.get(email=email):
            error="Used diffrent email ID "
            listof_error.append(error)

        elif not email :
            error="email required"
            listof_error.append(error)
            

        if not mobile:
            error="pls enter phone number"
            listof_error.append(error)

        elif len(mobile) != 10:
            error="pls enter 10 digit phone number"
            listof_error.append(error)
        
        if not udate :
            error="pls enter date"
            listof_error.append(error)
            
        if  len(hobby) == 0:
            error="At list One hobby select"
            listof_error.append(error)
            
        if len(listof_error) !=  0:         
            x={'error':listof_error}
            return render(request,'home.html',x)
        else:
            x = datetime.strptime(udate, "%Y-%m-%d").date()
            ages=age(x)

            # DATA Save Into Database
            customer = CustomerRegister.objects.create(
                first_name=fn,
                last_name=ln,
                email=email,
                mobile_no=mobile,
                password=make_password(passwords),
                dob=x,
                gender=data['gender']
            )

            Age.objects.create(
                user_id=customer,
                age=ages
            )
            hobby_string = ", ".join(hobby)
            Hobbies.objects.create(
                    user_id=customer,
                    hobby=hobby_string
                )
        

            # for h in hobby:
            #     Hobbies.objects.create(
            #         user_id=customer,
            #         hobby=h
            #     )
            EmailMessage(
                "Verification Mail Login credential",
                f"""
                    Hello User,

                    Your Login Details:

                    Email    : {email}
                    Password : {passwords}

                    Thank You.
                """,
                None,
                [email], 
            ).send()
            
            # x={'fn':fn,'ln':ln,'email':email,'mobile':mobile,'udate':udate,'data':data,'password':password} 
            return render(request,'login.html')
    return render(request,'home.html')

# def login(request):
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')


#         customer = CustomerRegister.objects.filter(
#             email=email,
#             password=password
#         ).first()

#         if customer:
#             request.session['cust_id'] = customer.id

#             # Generate OTP
#             otp = random.randint(100000, 999999)
#             print('otp: ', otp)
#             request.session['otp'] = otp
#             request.session['otp_expire'] = (
#                 datetime.now() + timedelta(seconds=43)
#             ).timestamp()

#             send_mail(
#                 'OTP Verification',
#                 f'Your OTP is {otp}',
#                 None,
#                 [customer.email],
#             )

#             return redirect('/otp')
#         else:
#             return render(request, 'login.html', {'error': 'Invalid credentials'})

#     return render(request, 'login.html')


# def otp_verify(request):
#     cust_id = request.session.get('cust_id')
#     customer = CustomerRegister.objects.get(id=cust_id)
#     if request.method == 'POST':
#         action=request.POST.get('action')
#         if action == "verify":
#             otp_input = request.POST.get('otpget')
#             print('otp_input: ', otp_input)
            
#             otp_session = request.session.get('otp')
#             print('otp_session: ', otp_session) 

#             otp_expire=request.session.get('otp_expire')
#             if  not otp_expire or datetime.now().timestamp() > otp_expire:
#                 request.session['otp_expire']=''
#                 return render(request, 'otp.html', {'error': 'OTP Expired'})


#             if otp_session == int(otp_input):
#                 request.session['otp'] = ''
#                 return redirect('/')  
#             else:
#                 # raise invalideotp("Invalid OTP")
#                 return render(request, 'otp.html', {'error': 'Invalid OTP'})  
#         elif action == "resend":
#             otp = random.randint(100000,999999)
#             print('resend - otp: ', otp)
#             request.session['otp']=otp
#             request.session['otp_expire'] = (
#                 datetime.now() + timedelta(seconds=43)
#             ).timestamp()
  
#             send_mail(
#                 'OTP Verification',
#                 f'Your OTP is {otp}',
#                 None,
#                 [customer.email],   
#             )
#             return render(request, 'otp.html')

#     return render(request, 'otp.html')


def login(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email and not password:
            return render(request, 'login.html', {'error': 'please enter email and password'})
        
        if not email:
            return render(request, 'login.html', {'error': 'please enter email'})
        
        if not password:
            return render(request, 'login.html', {'error': 'please enter password'})
        
        if not re.match(email_pattern, email):
            return render(request, 'login.html', {'error': 'Enter valid email ID'})

        try:
            customer = CustomerRegister.objects.get(email=email)
        except:
            return render(request, 'login.html', {'error': 'Email not found'})
        
        if check_password(customer.password,password):
            return render(request, 'login.html', {'error': 'Invalid password'})

        request.session['cust_id'] = customer.id
        # Generate OTP
        otp = random.randint(100000, 999999)
        print('otp: ', otp)
        request.session['otp'] = otp
        send_mail(
            'OTP Verification',
            f'Your OTP is {otp}',
            None,
            [customer.email],
        )
        return redirect('/otp2')
    return render(request, 'login.html')




def otp_verify2(request):
    c=request.session.get('cust_id')
    cus=CustomerRegister.objects.get(id=c)
    if request.method == "POST":
        
        otp_session=request.session.get('otp')
        print('otp_session: ', type(otp_session))
        otp_input=request.POST.get('otpget')
        print('otp_input: ', type(otp_input))
        if not otp_input:
            return render(request, 'otp2.html', {'error': 'Enter OTP'})
        if int(otp_input) == otp_session:
            request.session['otp'] = ''
            EmailMessage(
                'Successfull register',
                "registration complate",
                None,
                [cus.email]
            ).send()
            return redirect('/dashboard')
        else:
            return render(request, 'otp2.html', {'error': 'Invalid OTP'})
    return render(request, 'otp2.html')


def customer_list(request):
    c=CustomerRegister.objects.prefetch_related('age', 'hobby')
    
    pag=Paginator(c,1)
    page=request.GET.get('page')
    try:
        c=pag.page(page)
        # print('try c: ', c)
    except PageNotAnInteger:
        c=pag.page(1)
        # print('PageNotAnInteger c: ', c)
    except EmptyPage:
        c=pag.page(pag.num_pages)    
        # print('EmptyPage c: ', c)
    x={'customer':c}
    return render(request, 'customer_list.html',x)


def dashboard(request):
    if request.session.get('cust_id'):
        return render(request,'dashboard.html')
    else:
        return redirect('/')

def logout(request):
    request.session.pop('cust_id',None)
    return redirect('/')


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from  .serializers import *
@api_view(['GET'])
@permission_classes([AllowAny])
def rest_frame(request):
    return Response({'status': 200, 'message': 'view successfully'})



@api_view(['GET'])
@permission_classes([AllowAny])
def student_list(request):
    s=Student.objects.all()
    student=StudentSerializer(s,many=True)
    return Response(student.data)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def student_add(request):
    stu=StudentSerializer(data=request.data)

    if stu.is_valid():
        stu.save()
        return Response(stu.data)
    
    return Response(stu.errors)