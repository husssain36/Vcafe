
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.forms import inlineformset_factory
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .filters import filterVcanteen
import json
import razorpay
from email.message import EmailMessage
from prettytable import PrettyTable
import smtplib
import imghdr
from fpdf import FPDF
import pyfiglet
from datetime import datetime, timedelta
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def RegisterPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                #Sending email of email and password
                msg = EmailMessage()
                customer = username
                msg['Subject'] = 'Your Credentials On vCafe'
                msg['from'] = 'vCafe'
                msg['to'] = str(customer) # user's email address
                creds = 'Username: ' + username + '\n' + 'Password:' + password
                msg.set_content(creds)
                server = smtplib.SMTP_SSL('smtp.gmail.com',465)
                server.login('vcafe.vit@gmail.com','vidyalankar') #email and password
                server.send_message(msg)
                server.quit()
                #Ending email code
                messages.success(request, 'Account was created for ' + username)
                return redirect('login')
            else:
                form = CreateUserForm()    
                messages.error(request, "Your credentials are incorrect or Try using your VIT email")
    context = {'form':form}
    return render(request, 'accounts/createAccount.html', context)


def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Username or Password is incorrect")
    context = {}
    return render(request, 'accounts/index.html', context)

@login_required(login_url='/')
def LogoutUser(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            logout(request)
            return redirect('login')
        else:
            messages.warning(request, 'Password you have entered is incorrect!')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
        


@login_required(login_url='/')
def home(request):
    return render(request, 'accounts/home.html')

@login_required(login_url='/') 
def vcanteen(request):
    menu = VcanteenMenu.objects.all()
    category = Category.objects.all()
    filter = filterVcanteen(request.GET, queryset=menu)
    menu = filter.qs
    vcanteen = 'Vcanteen'
    context = {'menu': menu, 'category': category, 'filter': filter}
    return render(request, 'accounts/vcanteen.html', context)
    
@login_required(login_url='/')
def vlounge(request):
    menu = VcanteenMenu.objects.all()
    category = Category.objects.all()
    filter = filterVcanteen(request.GET, queryset=menu)
    menu = filter.qs
    vlounge = 'Vlounge'
    context = {'menu': menu, 'category': category, 'filter': filter}
    return render(request, 'accounts/vlounge.html', context)

@login_required(login_url='/')
def Cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        order_amount = order.get_cart_total * 100
        if request.method == 'POST':
            order_amount = order.get_cart_total 
            print(order_amount)
            order_currency = 'INR'
            order_id = order.id
            client = razorpay.Client(auth=('rzp_test_Cu99d4JFHKcb5M','DPIuejZbwQZwb89GTUDuVAa6'))
            payment = client.order.create({'order_amount': order_amount, 'currency': order_currency, 'payment_capture': '1', 'order_id': order_id})

    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    vcanteen = 'Vcanteen'
    vlounge = 'Vlounge'
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'order_amount': order_amount, 'vcanteen':vcanteen, 'vlounge':vlounge}
    return render(request, 'accounts/confirmOrder.html', context)

@login_required(login_url='/')
def updateItem(request):
    data = json.loads(request.body)
    menuId = data['menuId']
    action = data['action']
    print('MenuId:', menuId)
    print('Action:', action)

    customer = request.user
    
    menu = VcanteenMenu.objects.get(id=menuId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, vcanteen=menu)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'remove-all':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse("Item is added", safe=False)

@login_required(login_url='/')
def success(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        order_amount = order.get_cart_total
        order_id = 'Order ID : ' + str(order.id)
        order_id_copy = order_id
        print(order)
        pdf = FPDF()
        pdf.add_page()
        pt = PrettyTable(["Item", "Quantity", "Price", "Total"])
        pt.align["Item", "Quantity", "Price", "Total"] = "c"
        pt.padding_width = 1
        for item in items:
            pt.add_row([item.vcanteen.item, item.quantity, item.vcanteen.price, item.get_total])

        bill_append = '\n' + str('Total Items: ' + str(order.get_cart_items))
        bill_appendd = '\n' + 'Total Amount: ' + str(order.get_cart_total)
        
        lines = pt.get_string()
        file = open('text.txt','w+')
        with open('text.txt','w') as f:
            f.write(lines)
        pdf.set_font("Arial", size = 10)

        f = open("text.txt", "r")
        now = datetime.now()
        date = now.strftime("%d/%m/%Y")
        time = now.strftime('%I:%M %p')
        ttlItems = int(order.get_cart_items * 5)
        deliveryTime = now +  timedelta(minutes = ttlItems)
        xD = deliveryTime.strftime('%I:%M %p')
        token = now.strftime("%H%M%S")
        token1 = 'Token : ' + str(token)
        # pdf.cell(200, 20, txt = vcafe, ln=1, align='C')
        path = "static/images/logo-01.png"
        path2 = "static/images/VIT-logo.png"
        pdf.image(path, x = None, y = None, w = 0, h = 0, type = 'PNG', link = '')
        pdf.image(path2, x = 150, y = 12, w = 40, h = 18, type = 'PNG', link = '')
        
        pdf.cell(150, 10, txt = order_id, ln=1, align = 'L')
        pdf.cell(150, 10, txt = token1, ln=1, align = 'L')
        
        pdf.cell(150, 10, txt = date, ln=1, align = 'R')
        pdf.cell(150, 10, txt = time, ln=1, align = 'R')
        for x in f:
            pdf.cell(150, 10, txt = x, ln = 2, align = 'C')
        pdf.cell(150, 10, txt = bill_append, ln=2, align='L')
        pdf.cell(150, 10, txt = bill_appendd, ln=2, align='L')
        expDel =  str('Please Collect Your Order By: ' + str(xD))
        pdf.cell(150, 10, txt = expDel, ln=2, align='L')
        pdf.output("reciept.pdf")
        file_type = pdf.output("reciept.pdf")

        Sender_Email = "vcafe.vit@gmail.com"
        Reciever_Email = str(customer)
        Password = 'vidyalankar'
        newMessage = EmailMessage()
        newMessage['Subject'] = "Reciept of your Order" 
        newMessage['From'] = Sender_Email
        newMessage['To'] = str(customer)
        newMessage.set_content('Download your Reciept') 
        files = ['reciept.pdf']
        for file in files:
            with open(file, 'rb') as f:
                file_data = f.read()
                file_name = f.name
            newMessage.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(Sender_Email, Password)
            smtp.send_message(newMessage)
            
            
        
        pdfAdmin = FPDF()
        pdfAdmin.add_page()
        
        ptAdmin = PrettyTable(["Item", "Quantity", "Price", "Total"])
        ptAdmin.align["Item", "Quantity", "Price", "Total"] = "c"
        ptAdmin.padding_width = 1
        for item in items:
            ptAdmin.add_row([item.vcanteen.item, item.quantity, item.vcanteen.price, item.get_total])

        bill_append = '\n' + str('Total Items: ' + str(order.get_cart_items))
        bill_appendd = '\n' + 'Total Amount: ' + str(order.get_cart_total)
        
        lines = ptAdmin.get_string()
        file = open('textAdmin.txt','w+')
        with open('textAdmin.txt','w') as f:
            f.write(lines)
        pdfAdmin.set_font("Arial", size = 10)
        f = open("textAdmin.txt", "r")


        path = "static/images/logo-01.png"
        path2 = "static/images/VIT-logo.png"
        pdfAdmin.image(path, x = None, y = None, w = 0, h = 0, type = 'PNG', link = '')
        pdfAdmin.image(path2, x = 150, y = 12, w = 40, h = 18, type = 'PNG', link = '')
        
        pdfAdmin.cell(150, 10, txt = order_id, ln=1, align = 'L')
        pdfAdmin.cell(150, 10, txt = token1, ln=1, align = 'L')
        
        pdfAdmin.cell(150, 10, txt = date, ln=1, align = 'R')
        pdfAdmin.cell(150, 10, txt = time, ln=1, align = 'R')
        for x in f:
            pdfAdmin.cell(150, 10, txt = x, ln = 2, align = 'C')
        pdfAdmin.cell(150, 10, txt = bill_append, ln=2, align='L')
        pdfAdmin.cell(150, 10, txt = bill_appendd, ln=2, align='L')
        expDel =  str('Expected Delivery Time: ' + str(xD))
        pdfAdmin.cell(150, 10, txt = expDel, ln=2, align='L')
        pdfAdmin.output("recieptAdmin.pdf")
        file_type = pdfAdmin.output("recieptAdmin.pdf")
        
        Sender_Email = "vcafe.vit@gmail.com"
        Reciever_Email = str(customer)
        Password = 'vidyalankar'
        newMessageAdmin = EmailMessage()
        newMessageAdmin['Subject'] = "Order Placed by "+ str(customer) 
        newMessageAdmin['From'] = Sender_Email
        newMessageAdmin['To'] = Sender_Email
        newMessageAdmin.set_content('Record of Reciept') 
        files = ['recieptAdmin.pdf']
        for file in files:
            with open(file, 'rb') as f:
                file_data = f.read()
                file_name = f.name
            newMessageAdmin.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(Sender_Email, Password)
            smtp.send_message(newMessageAdmin)
        
        
        
    return render(request, 'accounts/success.html')



        # msg = EmailMessage()
        # customer = request.user
        # msg['Subject'] = 'Your Order Receipt'
        # msg['from'] = 'vCafe'
        # msg['to'] = str(customer) # user's email address
        # # new_bill = ''
        # x = PrettyTable()
        # x.align = "r"
        # x.field_names = ["Item", "Quantity", "Price", "Total"]

        
        # for item in items:
        #     # bill = str('Item : ' + str(item.vcanteen.item) + ' Quantity: ' + str(item.quantity) + ' Price: ' + str(item.vcanteen.price) + '\n') # Bill Content (Menu items)
        #     # new_bill += bill
        #     x.add_row([item.vcanteen.item, item.quantity, item.vcanteen.price, item.get_total])

        # print(x)
        # bill_append = '\n' + str('Total Items: ' + str(order.get_cart_items) + '\n' + 'Total Amount: ' + str(order.get_cart_total))
        # final_bill = str(x) + bill_append
        # msg.set_content(final_bill)
        # server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        # server.login('vcafe.vit@gmail.com','vidyalankar') #email and password
        # server.send_message(msg)
        # server.quit()
    return render(request, 'accounts/success.html')

    
def get_order_status(request):
    order = Order.objects.filter(customer=request.user).latest('date_ordered')
    cart_items = order.get_cart_items
    if order is None:
        status = "No order has been placed"

    if cart_items is None or cart_items==0:
        status = "No order has been placed"

    elif order.complete == True:
        status = "Your Order is ready!!"
    else:
        if order.complete == False:
            status = "No order has been placed"
        status = "Your order is in progress"
    context = {'status': status}
    return render(request, 'accounts/status.html', context)