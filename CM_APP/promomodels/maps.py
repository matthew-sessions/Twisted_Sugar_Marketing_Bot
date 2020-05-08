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


def report_map(count, ordercount, ordersum, orderavg):
    data = {
        "version": "v2",
        "content": {
            "messages": [
            {
                "type": "text",
                "text": f"QR codes scanned: {count['psid__count']} \nVouchers redeemed: {ordercount}\nOrder Sum: ${ordersum['order_amount__sum']}\nAverage Order ${orderavg['order_amount__avg']}"
            }
            ],
            "actions": [],
            "quick_replies": []
        }
        }
    return data
