from django.shortcuts import render,redirect
from datetime import date,datetime
import requests
import random
import string
from django.contrib.auth.hashers import make_password,check_password
from .models import *
from django.core.mail import EmailMessage,send_mail
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



           



def home(request):
    if request.method == "POST":
        
        fn=request.POST.get('fn')
        ln=request.POST.get('ln')
        # FETCH GENDER
        url= f"https://api.genderize.io/?name={ln}"
        res=requests.get(url)
        data=res.json()

        # Random password
        passwords=random_password(6)
    
        email=request.POST.get('email')
        mobile=request.POST.get('number')
        
        udate=request.POST.get('dates')
        hobby=request.POST.getlist('check[]')
        print('hobby: ', hobby)
        x = datetime.strptime(udate, "%Y-%m-%d").date()
        ages=age(x)

        # DATA Save Into Database
        customer = CustomerRegister.objects.create(
            first_name=fn,
            last_name=ln,
            email=email,
            mobile_no=mobile,
            password=passwords,
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

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        customer = CustomerRegister.objects.filter(
            email=email,
            password=password
        ).first()

        if customer:
            request.session['cust_id'] = customer.id

            # Generate OTP
            otp = random.randint(10000, 99999)
            request.session['otp'] = otp

            send_mail(
                'OTP Verification',
                f'Your OTP is {otp}',
                None,
                [customer.email],
            )

            return redirect('/otp')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def otp_verify(request):
    cust_id = request.session.get('cust_id')
    customer = CustomerRegister.objects.get(id=cust_id)
    if request.method == 'POST':
        action=request.POST.get('action')
        if action == "verify":
            otp_input = request.POST.get('otpget')
            print('otp_input: ', otp_input)
            
            otp_session = request.session.get('otp')
            print('otp_session: ', otp_session) 

            if otp_session == int(otp_input):
                request.session['otp'] = ''
                return redirect('/')  
            else:
                # raise invalideotp("Invalid OTP")
                return render(request, 'otp.html', {'error': 'Invalid OTP'})  
        elif action == "resend":
            otp = random.randint(10000,99999)
            request.session['otp']=otp
            send_mail(
                'OTP Verification',
                f'Your OTP is {otp}',
                None,
                [customer.email],   
            )
            return render(request, 'otp.html')

    return render(request, 'otp.html')