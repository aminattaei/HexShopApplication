from .models import Cart, Customer

def cart_items_count(request):
    count = 0
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.filter(email=request.user.email).first()
            if customer:
                cart = Cart.objects.filter(customer=customer).first()
                if cart:
                    count = cart.items.count()
        except:
            count = 0
    return {'cart_items_count': count}
