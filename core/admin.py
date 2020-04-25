from django.contrib import admin
from .models import Item, OrderItem, Order, Coupon, Payment, Refund

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

make_refund_accepted.short_description = 'Update orders to refund granted'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'payment',
                    'billing_address',
                    'coupon']
    list_display_links = ['user',
                          'payment',
                          'billing_address',
                          'coupon']
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = ['user__username',
                     'ref_code']
    actions = [make_refund_accepted]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'stripe_charge_id']

class RefundAdmin(admin.ModelAdmin):
    list_display = ['pk', 'order', 'accepted']

admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Coupon)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Refund, RefundAdmin)
