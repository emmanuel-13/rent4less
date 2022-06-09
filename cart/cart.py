from django.conf import settings 
from decimal import Decimal

from House.models import Room

class Cart(object):
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_KEY)
        if not cart:
            cart = self.session[settings.CART_SESSION_KEY] = {}
        self.cart = cart
 

    def add(self,room):
        room_id = str(room.id)
        print(room_id)
        '''
        'product_cart":{
                '1': {'quantity:3,price:400},
                2: {'quantity:3,price:400},
                3: {'quantity:3,price:400},
                4: {'quantity:3,price:400},
            }
        '''
    
        if not room_id in self.cart:
            self.cart[room_id] = {'price':str(room.price)}
        
        self.save()
        
    def save(self):
        self.session.modified = True

# {'3': {'quantity': 1, 'price': '3455.00'}, '4': {'quantity': '111', 'price': '2800.00'}}

    def list(self):
        carts = []
        for room_id in self.cart.keys():
            obj = Room.objects.get(id=room_id)
            tmp_cart = {
                'id':obj.id,
                'room_image': obj.image1.url,
                'room_id': obj.room_id,
                'room_types':obj.room_types,
                'price': Decimal(int (obj.price))
            }
            carts.append(tmp_cart)
        print("carts...")
        return carts

    def get_total_amount(self):
        return sum(float(v['price']) for v in self.cart.values())

        '''
        cart = {'3': {'quantity': 8.0, 'price': '3455.00'}}
        cart[3] = {'quantity': 8.0, 'price': '3455.00'}
        cart[3]['quantity'] = 8.0
        '''
#     def update(self,room_id):
#         pid = str(room_id)
#         '''
# dct = {'1':"idnesa','2':"dont knwo"}
# dct['1'] = 'fjdsfk'
#         '''
#         # print(self.cart)s
#         # self.cart[pid]['quantity'] = quantity
#         self.save()
#         print(self.cart)

    def delete(self,room_id):
        pid = str(room_id)
        del self.cart[pid]
        self.save()

    def clearcart(self):
        del self.session[settings.CART_SESSION_KEY]
        self.save()