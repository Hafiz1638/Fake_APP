import subprocess
import optparse
from colorama import *
import time 

init(autoreset=True)
r = Fore.RED + Style.BRIGHT
y = Fore.GREEN
b = Fore.BLUE
s = Fore.YELLOW 
def banner():
    try :
        with open("banner.txt","r") as f:
            print(r+f.read())
    except FileNotFoundError:
        print("dosya yok")        
def parseArgumans():
    parser = optparse.OptionParser()
    parser.add_option("-e", "--essid", dest="essid", help="Sahte erişim noktasının SSID'si")
    parser.add_option("-i", "--interface", dest="interface", help="Arayüz (Örn: wlan0mon)")
    parser.add_option("-s", "--sayi", dest="sayi", type="int", help="Kaç adet sahte WiFi oluşturulsun?")
    
    (options, args) = parser.parse_args()


    if not options.essid or not options.interface or not options.sayi:
        print(r + "\nHata: -e (ad), -i (arayuz) ve -s (sayi) parametrelerini girmelisiniz!")
        exit()
        
    return options.essid, options.interface, options.sayi

def startFakeapp(essid, interface, sayi):
    processes = []
    print(b + f"\n[*] {sayi} adet sahte WiFi oluşturuluyor...")
    
    for num in range(sayi):
        ssid = f"{essid}_{num+1}"

        p = subprocess.Popen(
            ["airbase-ng", "--essid", ssid, interface],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        processes.append(p)
        print(y + f"[+] Sahte WiFi başladı: {ssid}")
        time.sleep(0.5)
    return processes
        
def stopAp(processes):
    print("\n" + r + "[!] Saldırı durduruluyor, süreçler kapatılıyor...")
    for p in processes:
        p.terminate()
    print(y + "[+] Tüm sahte erişim noktaları kapatıldı.")

def main():
    print(banner())
    print(r + "=== SAHTE WIFI OLUSTURUCU BASLADI ===")
    essid, interface, sayi = parseArgumans()
    
    processes = startFakeapp(essid, interface, sayi)
    
    print(b + "\n[!] Çıkmak için CTRL+C tuşlarına basın.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stopAp(processes)

if __name__ == "__main__":
    main()
