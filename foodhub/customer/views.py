from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail
from .models import MenuItem, OrderModel

import json

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')
    
class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        main_course = MenuItem.objects.filter(category__name__contains='Main Course')
        sides = MenuItem.objects.filter(category__name__contains='Sides')
        
        desserts = MenuItem.objects.filter(category__name__contains='Desserts')

        # pass into context
        context = {
            'main_course': main_course,
            'sides': sides,
            'desserts': desserts,
        }

        # render the template
        return render(request, 'customer/order.html', context)
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip')

        order_items = {
            'items': []
        }
        # gets list of id of selected menu items
        items = request.POST.getlist('items[]')
        # loop trough each selected item id
        for item in items:
            # get the menu item object using its id
            menu_item = MenuItem.objects.get(pk=int(item))
            # create a dictionary to store details of the menu item
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }
            # append the item data to the order items list
            order_items['items'].append(item_data)

            price = 0
            item_ids = []
        
        # calculate the total price and collect item ids
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        # create an order object with the total price and add the items to it
        # objects.create() adds a new record to the database
        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            country=country,
            zip_code=zip_code
            )
        # link all the selected items to the order using many to many relationship
        order.items.add(*item_ids)

        # After everything is done, send a confirmation email to the user
        body = (f"Thank you for your order! Your food is being prepared.\nYour total: {price}")
        
        send_mail(
            'Thank you for your order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )
            
        # prepare context to display in the order confirmation page
        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)

        

class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        tracking_number = f"FH-{1000 + pk}"

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price
        }

        return render(request, 'customer/order_confirmation.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        # Parse the JSON data sent from the frontend
        data = json.loads(request.body)

        # Check the 'isPaid' value sent via fetch
        if data.get('isPaid'):
            order = OrderModel.objects.get(pk=pk)
            # Update the database record
            order.is_paid = True
            order.save() # Save the payment status to the database

        # Redirect to the payment confirmation page defined in urls.py
        return redirect('order-pay-confirmation')
    
class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')

class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        category = request.GET.get('category')

        if category:
            menu_items = menu_items.filter(category__name__icontains=category)

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)

class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) | 
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items,
        }

        return render(request, 'customer/menu.html', context)



        