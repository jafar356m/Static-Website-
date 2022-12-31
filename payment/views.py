from .models import *
from django.shortcuts import render
import razorpay
from .forms import *
from account.models import *
# from project.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRECT_KEY
# Create your views here.
# client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRECT_KEY))
def payment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        # amount = int(request.POST.get('amount')) * 100
        # property_type=request.POST.get('property_type')
        user=User_Profile.objects.get(user=request.user)
        print(user.id)
        request.session['user']=user.id
        amount=400*100
        client = razorpay.Client(auth=('rzp_test_48Z9LMTDVAN5JU', 'gMxfhwgZ73ANYJQCeblLMy7W'))
        response_payment = client.order.create(dict(amount=amount,
                                                    currency='INR')
                                               )

        order_id = response_payment['id']
        order_status = response_payment['status']

        if order_status == 'created':
            payment = Payment(
                user=request.user,
                name=name,
                amount=4*100,
                order_id=order_id
            )
          
        payment.save()
        response_payment['name'] = name

        form = PaymentForm(request.POST or None)
        return render(request, 'payment.html', {'form': form, 'payment': response_payment})

    form = PaymentForm()
    return render(request, 'payment.html', {'form': form})


def payment_status(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    # client instance
    client = razorpay.Client(auth=('rzp_test_48Z9LMTDVAN5JU', 'gMxfhwgZ73ANYJQCeblLMy7W'))

    try:
        status = client.utility.verify_payment_signature(params_dict)
        payment = Payment.objects.get(order_id=response['razorpay_order_id'])
        payment.payment_id = response['razorpay_payment_id']
        payment.paid = True
        payment.save()
        try:
            user=request.session['user']
            user=User_Profile.objects.get(id=user)
            print(user.paid)
            requirement=User_Profile.objects.update_or_create(id=user.id,
            defaults={'paid':True}
            )
            print(user.paid)
        except:
            pass
        return render(request, 'payment_status.html', {'status': True,'payment_id':payment.payment_id})
    except:
        return render(request, 'payment_status.html', {'status': False})

    

