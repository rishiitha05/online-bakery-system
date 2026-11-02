from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

from .models import Customer, Cake, Cart, Order, Wishlist


# ==========================
# HOME
# ==========================

def home(request):
    cakes = Cake.objects.all()
    return render(request, 'home.html', {'cakes': cakes})


# ==========================
# REGISTER
# ==========================

def register(request):

    if request.method == "POST":

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        if Customer.objects.filter(email=email).exists():

            return render(request, "register.html", {
                "error": "Email already registered."
            })

        Customer.objects.create(
            name=name,
            email=email,
            phone=phone,
            password=password
        )

        return redirect('login')

    return render(request, "register.html")


# ==========================
# LOGIN
# ==========================

def login_view(request):

    if request.method == "POST":

        email = request.POST['email']
        password = request.POST['password']

        user = Customer.objects.filter(
            email=email,
            password=password
        ).first()

        if user:

            request.session['customer_id'] = user.id
            request.session['customer_name'] = user.name

            return redirect('home')

        return render(request, "login.html", {
            "error": "Invalid Email or Password"
        })

    return render(request, "login.html")


# ==========================
# LOGOUT
# ==========================

def logout_view(request):

    request.session.clear()

    return redirect('home')


# ==========================
# CART
# ==========================

def add_to_cart(request, cake_id):

    cake = Cake.objects.get(id=cake_id)

    cart_item = Cart.objects.filter(cake=cake).first()

    if cart_item:

        cart_item.quantity += 1
        cart_item.save()

    else:

        Cart.objects.create(
            cake=cake,
            quantity=1
        )

    return redirect('home')


def cart(request):

    cart_items = Cart.objects.all()

    total = 0

    for item in cart_items:

        item.item_total = item.cake.price * item.quantity

        total += item.item_total

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total
    })


def increase_quantity(request, cart_id):

    cart_item = Cart.objects.get(id=cart_id)

    cart_item.quantity += 1

    cart_item.save()

    return redirect("cart")


def decrease_quantity(request, cart_id):

    cart_item = Cart.objects.get(id=cart_id)

    if cart_item.quantity > 1:

        cart_item.quantity -= 1

        cart_item.save()

    else:

        cart_item.delete()

    return redirect("cart")


def remove_from_cart(request, cart_id):

    cart_item = Cart.objects.get(id=cart_id)

    cart_item.delete()

    return redirect("cart")


# ==========================
# CHECKOUT
# ==========================

       
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
# Import your Order model here if it isn't already (e.g., from .models import Order)

def checkout(request):
    if request.method == 'POST':
        # 1. Capture the data sent from the HTML form
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        total = request.POST.get('total')
        payment_method = request.POST.get('payment_method')

        # 2. Your existing code that saves the order to the database goes here
        # Example: order = Order.objects.create(name=name, email=email, ...)
        
        # 3. SEND EMAIL (This matches your layout perfectly)
        send_mail(
            subject="Order Confirmation",
            message=f"""
Hello {name},

Thank you for shopping with Online Bakers System.

Your order has been placed successfully.

Customer Name: {name}
Phone: {phone}
Delivery Address:
{address}

Total Amount: {total}
Payment Method: {payment_method}
Order Status: Pending

Thank you for choosing us.

Online Bakers System
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],  # Sends the email directly to the customer's input
            fail_silently=False,
        )

        # 4. Redirect the user to a success page so the page doesn't freeze
        return redirect('orders')
    # If it's a GET request, just display the checkout page normally
    return render(request, 'checkout.html')  # Make sure this matches your template path


# ==========================
# ORDERS
# ==========================

def orders(request):

    orders = Order.objects.all().order_by("-id")

    return render(request, "orders.html", {
        "orders": orders
    })


# ==========================
# WISHLIST
# ==========================

def add_to_wishlist(request, cake_id):

    if "customer_id" not in request.session:
        return redirect("login")

    customer = Customer.objects.get(
        id=request.session["customer_id"]
    )

    cake = Cake.objects.get(id=cake_id)

    if not Wishlist.objects.filter(
        customer=customer,
        cake=cake
    ).exists():

        Wishlist.objects.create(
            customer=customer,
            cake=cake
        )

    return redirect("home")


def wishlist(request):

    if "customer_id" not in request.session:
        return redirect("login")

    customer = Customer.objects.get(
        id=request.session["customer_id"]
    )

    wishlist_items = Wishlist.objects.filter(
        customer=customer
    )

    return render(request, "wishlist.html", {
        "wishlist_items": wishlist_items
    })


def remove_from_wishlist(request, wishlist_id):

    wishlist_item = Wishlist.objects.get(
        id=wishlist_id
    )

    wishlist_item.delete()

    return redirect("wishlist")


# ==========================
# CONTACT
# ==========================

def contact(request):

    return render(request, "contact.html")


# ==========================
# ABOUT
# ==========================

def about(request):

    return render(request, "about.html")