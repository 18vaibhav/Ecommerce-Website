import json
from .models import *

def cookiecart(request):
    try:
        cart=json.loads(request.COOKIES['cart'])
    except:
        cart={}

    print('cart:',cart)
    items=[]
    order={'get_cart_total':0,'get_cart_item':0,'shipping':False}
    cartitem=order['get_cart_item']
    
    for i in cart:
        try:
            cartitem+=cart[i]['quantity']
            product=Product.objects.get(id=i)
            total=(product.price*cart[i]['quantity'])
            order['get_cart_total']+=total
            order['get_cart_item']+=cart[i]['quantity']
            item={
            'product':{
                'id':product.id,
                'name': product.name,
                'price':product.price,
                'imageURL':product.imageURL,
            },
                'quantity':cart[i]['quantity'],
                'get_total':total,
                }
            items.append(item)
            if(product.digital==False):
                order['shipping']=True
        except:
            pass
    return {'cartitem':cartitem,'order':order,'items':items}