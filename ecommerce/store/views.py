from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cookiecart

def store(request):
    if request.user.is_authenticated: 
        customer=request.user.customer
        order, created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartitem=order.get_cart_item
    else:
        cookiedata=cookiecart(request)
        cartitem=cookiedata['cartitem']
        
    products=Product.objects.all()
    context={'products':products,'cartitem':cartitem}
    return render(request , 'store/store.html' , context)

def cart(request):
    if request.user.is_authenticated: 
        customer=request.user.customer
        order, created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartitem=order.get_cart_item
    else:
        cookiedata=cookiecart(request)
        cartitem=cookiedata['cartitem']
        order=cookiedata['order']
        items=cookiedata['items']
    context={'items':items ,'order':order,'cartitem':cartitem}
    return render(request , 'store/cart.html' , context)

def checkout(request):
    if request.user.is_authenticated: 
        customer=request.user.customer
        order, created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartitem=order.get_cart_item
    else:
        cookiedata=cookiecart(request)
        cartitem=cookiedata['cartitem']
        order=cookiedata['order']
        items=cookiedata['items']
    context={'items':items ,'order':order,'cartitem':cartitem}
    return render(request , 'store/checkout.html' , context)

def updateitem(request):
    data  =  json.loads(request.body)
    productid=data['productid']
    action=data['action']
    print(productid)
    customer=request.user.customer
    product=Product.objects.get(id=productid )
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,created=Orderitem.objects.get_or_create(order=order,product=product)
    if(action=='Add'):
        orderitem.quantity=(orderitem.quantity+1)
    elif(action=='remove'):
        orderitem.quantity=(orderitem.quantity-1)
    
    orderitem.save()
    if(orderitem.quantity<=0):
        orderitem.delete()
    return JsonResponse('item is added',safe=False)

def processorder(request):

    transaction_id=datetime.datetime.now().timestamp()
    print('data:',request.body)
    data=json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
    
    else:
        print("user is not logged in")

        print('COOKIES:',request.COOKIES)
        name=data['form']['name']
        email=data['form']['name']
        cookiedata=cookiecart(request)
        items=cookiedata['items']

        customer,created=Customer.objects.get_or_create(
            email=email,
        )
        customer.name=name
        customer.save()
        order=Order.objects.create(
            customer=customer,
            complete=False,
        )
        
        for item in items:
            product=Product.objects.get(id=item['product']['id'])
            orderitem=Orderitem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity'],
            )
    
    total=float(data['form']['total'])
    order.transaction_id=transaction_id

    if total==float(order.get_cart_total):
        order.complete=True
    order.save()
    if order.shipping==True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            )
    return JsonResponse('payment complete',safe=False)
