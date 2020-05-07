from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.db.models import Avg, Count, Sum, Q


import qrcode
import io
from decouple import config
from .models import DoorPromo, Orders
from .maps import optin_map, send_confirmation, report_map

# Create your views here.

base_url = config('base_url')
manychat_key = config('manychat_key')

def qr_generator(request, code):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=6,
    )
    qr.add_data(base_url + 'redeem/in-store/' + code)
    qr.make(fit=True)
    bytes_image = io.BytesIO()
    img = qr.make_image(fill_color="black")
    img.save(bytes_image, format='png')
    bytes_image.seek(0)
    return HttpResponse(bytes_image, content_type="image/png")

def redeem_code(request, code):
    context = {'code':code}
    if request.method == 'GET':
        user = DoorPromo.objects.get(psid=int(code))
        if user.status == True:
            return render(request, 'taken.html')
        else:
            return render(request, 'redeem.html', context)
    elif request.method == 'POST':
        amount = request.POST.get('amount')
        pin = request.POST.get('pin')
        if int(pin) == int(config('pin'))  and amount != '':
            user = DoorPromo.objects.get(psid=int(code))
            if user.status == True:
                print('issue')
                return render(request, 'success.html')
            else:
                place_order = Orders(psid=int(code), order_amount = float(amount), promo_id = user.promo_id)
                place_order.update() 
                place_order.save()
                place_order.save()
                send_confirmation(code, 'content20200506191128_015369', manychat_key)
                return render(request, 'success.html')
        else:
            return render(request, 'formerror.html', context)


def optin(request, code):
    code = int(code)
    try:
        data = DoorPromo.objects.get(psid = code)
    except DoorPromo.DoesNotExist:
        data = None
    if data is None:
        user = DoorPromo(psid = code, source = 'In Store', promo_id = 'instore1')
        user.save()
        res = optin_map(False, False)
        return JsonResponse(res)
    else:
        if data.status == True:
            return JsonResponse(optin_map(True, True))
        else:
            return JsonResponse(optin_map(True, False))



def test(request, id):
    data = {
    "version": "v2",
    "content": {
        "messages": [
        {
            "type": "image",
            "url": base_url + "qr_code/" + id + "/pic.png",
            "buttons": []
        }
        ],
        "actions": [],
        "quick_replies": []
    }
    }
    return JsonResponse(data)
    

def report(request):
    total_users = DoorPromo.objects.all().aggregate(Count('psid'))
    orders = Orders.objects.filter(promo_id='instore1')
    ordercount = orders.count()
    ordersum = orders.aggregate(Sum('order_amount'))
    orderavg = orders.aggregate(Avg('order_amount'))
    data = report_map(total_users, ordercount, ordersum, orderavg)
    return JsonResponse(data)

def home(request):
    return JsonResponse({'status':'Done'})


def clear_db(request):
    b = DoorPromo.objects.all().delete()
    a = Orders.objects.all().delete()
    return JsonResponse({'status':'Done'})
