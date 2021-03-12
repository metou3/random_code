import requests
import json
import time


# data={
# 'grant_type':'refresh_token',
# 'client_id':'303813100189-9gfi3ucu73h085re1ubm9muoeqap77rf.apps.googleusercontent.com',
# 'client_secret':'80iGGtAC7B6M8Diu9MPbrVm0',
# 'refresh_token':'1//043K_9E7ASPD_CgYIARAAGAQSNwF-L9IrfUwNMGR6vLY0IQFE6LJUT68NQ9TxBl2RkmDjbhoT3R0pc_lJiuy0HyisoICkjvUQWMI'
# }
# r = requests.post("https://accounts.google.com/o/oauth2/token",data)
# print(r.status_code, r.reason)
# print(r.text)
#
# result = r.json()
# access_token = result["access_token"]
# print("access_token: ", access_token)
#
#
# token="gojbphfclpdamjfgpfcfbalc.AO-J1Ox7Awjr2u5Wf7Y6f2bqa7HS6EpX54DgGBK3ItqB3kMki6DrUrrZ3FcnZPwhCzCGzFAuVNlkeETHydhXHBHViDnkOASH_mQX3qJZYoRGK_EFTCPRUxSyKE8oqEnnMERvx8XLcAyZ"
# productId="33.99usd_1year_sub"
# packageName="com.everythingsunny.goodnews"
# your_auth_token=access_token
# url = "https://www.googleapis.com/androidpublisher/v3/applications/"+packageName+"/purchases/subscriptions/"+productId+"/tokens/"+token
# headers = {"Authorization": "Bearer "+your_auth_token}
# r=requests.get(url, headers = headers)
# print(r.status_code, r.reason)
# print(r.text)
# result = r.json()
# print(result)


def get_new_access_token():
    data = {
        'grant_type': 'refresh_token',
        'client_id': '303813100189-9gfi3ucu73h085re1ubm9muoeqap77rf.apps.googleusercontent.com',
        'client_secret': '80iGGtAC7B6M8Diu9MPbrVm0',
        'refresh_token': '1//043K_9E7ASPD_CgYIARAAGAQSNwF-L9IrfUwNMGR6vLY0IQFE6LJUT68NQ9TxBl2RkmDjbhoT3R0pc_lJiuy0HyisoICkjvUQWMI'
    }
    r = requests.post("https://accounts.google.com/o/oauth2/token", data)
    print(r.status_code, r.reason)
    print(r.text)

    result = r.json()
    if r.status_code == 200:
        access_token = result["access_token"]
        print("access_token: ", access_token)
        with open('last_access_token.txt', 'w') as outfile:
            json.dump(result, outfile)
            print("stored access_token")
        return access_token


def get_access_token():
    with open('last_access_token.txt') as json_file:
        data = json.load(json_file)
    return data["access_token"]


def get_expired_time(access_token, purchase_token, sub_id):
    token = purchase_token
    packageName = "com.everythingsunny.goodnews"
    your_auth_token = access_token
    url = "https://www.googleapis.com/androidpublisher/v3/applications/" + packageName + "/purchases/subscriptions/" + sub_id + "/tokens/" + token
    headers = {"Authorization": "Bearer " + your_auth_token}
    r = requests.get(url, headers=headers)
    print(r.status_code, r.reason)
    print(r.text)
    result = r.json()
    print(result)

    if r.status_code == 200:
        return result["expiryTimeMillis"]
    else:
        return False


def get_purchase_detail(access_token, purchase_token, sub_id):
    token = purchase_token
    packageName = "com.everythingsunny.goodnews"
    your_auth_token = access_token
    url = "https://www.googleapis.com/androidpublisher/v3/applications/" + packageName + "/purchases/subscriptions/" + sub_id + "/tokens/" + token
    headers = {"Authorization": "Bearer " + your_auth_token}
    r = requests.get(url, headers=headers)
    print(r.status_code, r.reason)
    print(r.text)
    result = r.json()
    print(result)

    if r.status_code == 200:
        return result
    else:
        return False


def get_payment_state(purchase_token):
    if get_purchase_detail(get_access_token(), purchase_token) == False:
        details = get_purchase_detail(get_new_access_token(), purchase_token)
    else:
        details = get_purchase_detail(get_access_token(), purchase_token)

    payment_state = details["paymentState"]
    return payment_state


# after expired time 5 hours, check payment state:
# case 0: payment pending > send notification to remind purchase and lock pro features
# case 1: payment received, done, do nothing
# case 2: free trial, wait for more 5 hours and check again
# case 3: Pending deferred upgrade/downgrade, don't know what is this???


def check_order(expired_time, purchase_token):
    if time.time() >= expired_time + 5 * 60 * 60 * 1000:
        payment_state = get_payment_state(purchase_token)
        return {"payment_state": payment_state}
    else:
        return {"payment_state": 99}


import datetime

my_purchase_token = "bapeicmjkbnjekbmmibjcmij.AO-J1OwrpcuKfKMlBvXsmkgFRDEnxsHv2SmzITgXHxZvJqVkx9A4jbNkYOfjLkfEx3ZRKYNoJcXZhj77Rl77Q6DM_YxfMsi8-60gvFCcN4J6fO5gKBH_RFKYusSFzcu1v1ZCmj9yrsuk"

sub_id = "60usd_1year_sub"
def check_state(my_purchase_token, sub_id):
    global payment_state
    r = get_purchase_detail(get_access_token(), my_purchase_token, sub_id)
    if not r:
        r = get_purchase_detail(get_new_access_token(), my_purchase_token, sub_id)
        keys = list(r.keys())
    else:
        keys = list(r.keys())
    #
    # print("start: ", datetime.datetime.fromtimestamp(int(r["startTimeMillis"]) / 1000).strftime('%c'))
    # print("expired: ", datetime.datetime.fromtimestamp(int(r["expiryTimeMillis"]) / 1000).strftime('%c'))
    # print("duration: ", (int(r["expiryTimeMillis"]) / 1000 - int(r["startTimeMillis"]) / 1000) / 60 / 60 / 24, " days")
    # print("is expired: ", time.time() * 1000 > int(r["expiryTimeMillis"]))
    # print("time: ", datetime.datetime.fromtimestamp(time.time()).strftime('%c'), time.time())
    #
    # print("get_next_expired_time: ", get_expired_time(get_new_access_token(), my_purchase_token, sub_id))

    expired_time = int(r["expiryTimeMillis"])
    is_expired = time.time() * 1000 > expired_time
    auto_renew = r["autoRenewing"]
    has_cancel_reason = "cancelReason" in keys
    has_payment_state = "paymentState" in keys
    print("meta_data: ", keys)
    print("is_expired: ", is_expired)
    print("is_auto_renew: ", auto_renew)
    if has_payment_state:
        payment_state = r["paymentState"]
        print("payment_state: ", payment_state)

    print("has_cancel_reason: ", has_cancel_reason)
    print("has_payment_state: ", has_payment_state)

    if has_cancel_reason:
        #add the case when users cancel but still valid sub, not expired yet
        if is_expired:
            return {"state": "cancel", "next_expired_time": expired_time, "auto_renew": auto_renew}
        else:
            return {"state": "cancel_not_expired", "next_expired_time": expired_time, "auto_renew": auto_renew}
    elif not is_expired and has_payment_state and auto_renew:
        if payment_state == 2:
            return {"state": "free_trail", "next_expired_time": expired_time, "auto_renew": auto_renew}
        elif payment_state == 0:
            return {"state": "free_trail_pending_payment", "next_expired_time": expired_time, "auto_renew": auto_renew}
        elif payment_state == 1:
            return {"state": "success_payment", "next_expired_time": expired_time, "auto_renew": auto_renew}
        #dont have update or downgrade payment option


# print(check_state(my_purchase_token, sub_id))


