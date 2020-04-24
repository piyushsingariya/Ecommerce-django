from django.contrib import admin
from .models import Item, OrderItem, Order, Coupon


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    # 'payment',
                    'billing_address',
                    'coupon']
    list_display_links = ['user',
                          # 'payment',
                          'billing_address',
                          'coupon']
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']


admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Coupon)
