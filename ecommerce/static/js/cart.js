var updateBtns=document.getElementsByClassName('update-cart')

for(var i=0;i<updateBtns.length;i++)
{
updateBtns[i].addEventListener('click',function ()
{
var productid=this.dataset.product
var action=this.dataset.action
console.log('product:',productid,'action:',action)
console.log('user:',user)
if(user==='AnonymousUser')
{
addcookieitem(productid,action)
}
else
{
updateUserOrder(productid,action)
}
}
)
}
function addcookieitem(productid,action)
{
console.log("not logged in")
if(action=='Add')
{
if(cart[productid]==undefined)
{
cart[productid]={'quantity':1}
}
else{
cart[productid]['quantity']+=1
}
}
if(action=='remove')
{
cart[productid]['quantity']-=1
if((cart[productid]['quantity'])<=0)
{
console.log('remove item')
delete cart[productid]
}
}
console.log('cart:',cart)
document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
location.reload()
}
function updateUserOrder(productid,action)
{
var url='/update_item/'
fetch(url,{
    method:'POST',
    headers:{
    'content-type':'application/json',
    'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify({'productid': productid, 'action': action}),
}
)
.then((response)=>
{
return response.json()
}
)
.then((data)=>{
console.log('data:',data)
location.reload()
}
)
}