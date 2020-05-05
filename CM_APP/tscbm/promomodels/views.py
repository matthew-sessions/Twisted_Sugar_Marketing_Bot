from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import qrcode
import io
from decouple import config

# Create your views here.

base_url = config('base_url')

def qr_generator(request, code):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(base_url + '?' + code)
    qr.make(fit=True)
    bytes_image = io.BytesIO()
    img = qr.make_image(fill_color="black")
    img.save(bytes_image, format='png')
    bytes_image.seek(0)
    return HttpResponse(bytes_image, content_type="image/png")

def redeem_code(request, code):
    context = {'code':code}
    return render(request, 'redeem.html', context)