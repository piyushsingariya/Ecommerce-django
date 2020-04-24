from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, Order, OrderItem, BillingAddress, Coupon, Payment
from django.utils import timezone
from django.contrib import messages
from .forms import CheckoutForm, CouponForm

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class IndexView(ListView):
    model = Item
    paginate_by = 4
    template_name = "index.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This Item quantity has been updated to your Cart")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, "This Item has been added to your Cart")
            order.items.add(order_item)
            return redirect("core:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This Item has been added to your Cart")
    return redirect("core:product", slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This Item has been removed to your Cart")
            return redirect("core:order-summary")
        else:
            # Add a message that order doesn't not contain the order item
            messages.info(request, "This Item isn't in your Cart")
            return redirect("core:product", slug=slug)
    else:
        # Add a message that user doesn't have an order
        messages.info(request, "You do not have an active order!!!")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This Item quantity was updated")
            return redirect("core:order-summary")
        else:
            # Add a message that order doesn't not contain the order item
            messages.info(request, "This Item isn't in your Cart")
            return redirect("core:product", slug=slug)
    else:
        # Add a message that user doesn't have an order
        messages.info(request, "You do not have an active order!!!")
        return redirect("core:product", slug=slug)


@login_required
def add_single_item_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This Item quantity has been updated to your Cart")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This Item has been added to your Cart")
            order.items.add(order_item)
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This Item has been added to your Cart")
    return redirect("core:order-summary")


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            couponform = CouponForm()
            context = {
                'form': form,
                'couponform': couponform,
                'order': order
            }
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:checkout-page")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        # print(self.request.POST)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                # print(form.cleaned_data)
                # print("The form is valid")
                email = form.cleaned_data.get('email')
                address = form.cleaned_data.get('address')
                address2 = form.cleaned_data.get('address2')
                state = form.cleaned_data.get('state')
                district = form.cleaned_data.get('district')
                zipcode = form.cleaned_data.get('zipcode')
                # same_billing_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    email=email,
                    address=address,
                    address2=address2,
                    state=state,
                    district=district,
                    zipcode=zipcode,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                if payment_option == "S":
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(self.request, "Invalid option selected")
                    return redirect('core:checkout-page')
            else:
                messages.warning(self.request, "Invalid parameter")
                return redirect('core:checkout-page')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
            }
            return render(self.request, "payment-page.html", context)
        else:
            messages.warning(self.request, "You have not added a billing address")
            return redirect("core:checkout-page")

    def post(self, *args, **kwargs):
        token = self.request.POST.get('stripeToken')
        order = Order.objects.get(user=self.request.user, ordered=False)
        amount = int(order.get_final_price() * 100)

        try:
            charge_id = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token,
            )
            # Create a payment
            payment = Payment()
            payment.stripe_charge_id = charge_id['id']
            payment.user = self.request.user
            payment.amount = order.get_final_price()
            payment.save()

            # assign payment to order
            order.ordered = True
            order.payment = payment
            order.save()
            messages.success(self.request, "Your order was successful")
            return redirect("/")
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.info(self.request, f"{err.get('message')}")
            return redirect("/")
        except stripe.error.RateLimitError as e:
            messages.info(self.request, "RateLimitError")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            messages.info(self.request, "InvalidRequestError")
            return redirect("/")
        except stripe.error.AuthenticationError as e:
            messages.info(self.request, "AuthenticationError")
            return redirect("/")
        except stripe.error.APIConnectionError as e:
            messages.info(self.request, "APIConnectionError")
            return redirect("/")
        except stripe.error.StripeError as e:
            messages.info(self.request, "Something went wrong!!! You were not charged.")
            return redirect("/")
        except Exception as e:
            messages.info(self.request, "Something went wrong!!!")
            return redirect("/")


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout-page")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code=code)
                order.save()
                messages.info(self.request, "This coupon successfully applied")
                return redirect("core:checkout-page")

            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout-page")
