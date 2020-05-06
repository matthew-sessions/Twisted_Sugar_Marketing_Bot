import requests

def optin_map(coupon, redeem):
    data = {'has_voucher': coupon, 'redeemed_voucher': redeem}
    return data

def send_confirmation(id, flow, key):
    body = {
    "subscriber_id": int(id),
    "flow_ns": flow
    }
    requests.post('https://api.manychat.com/fb/sending/sendFlow', 
    headers = {"Authorization": "Bearer " + key}, data=body).json()
