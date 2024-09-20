import urequests as requests
import time
import uasyncio

from machine import Pin, ADC

place = "Caney+55A+No+18-65"

def sendlevel(level):
    url = "http://172.16.222.43:80/decibels/level"
    data = {"level":level}

    data = requests.post(url, json=data)
    data = data.json()
    print(data)
    return data

def send_level_alert(phone, key, level):
    global place
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text=el+nivel+desonido+en+{place}+es+{level}+MUY+ALTO&apikey={key}"
    print(url)
    sending = True
    while sending:
        try:
            response = requests.get(url)
            
        except Exception as e:
            print(f"error sending: {e}")
            
        if response.status_code == 200:
            print('Success!')
            sending = False
        else:
            print('Error')
            
    print(response.text)
    
def send_level_max(phone, key, level, rephora):
    global place
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text=el+nivel+desonido+maximo+en+{place}+fue+{level}+{rephora}+veces&apikey={key}"
    print(url)
    sending = True
    while sending:
        try:
            response = requests.get(url)
            print(response)
            
        except Exception as e:
            print(f"error sending: {e}")
            
        if response.status_code == 200:
            print('Success!')
            sending = False
        else:
            print('Error')
            
    print(response.text)
    
    
async def monitor():
    p2 = Pin(2, Pin.OUT)
    p2.on()

    adc = ADC(Pin(32), atten=ADC.ATTN_0DB)
    
    maxvol = 200000
    sended = False
    rep = 0
    rephora = 0
    nextreport = time.time() + 10
    maxlevel = 0
    while True:
        prom = 0
        for i in range(0, 100):
            val = adc.read_uv()
            prom = (prom * i + val)/(i + 1)
#         print(str(prom) + ", " + str(rep) + ", " + str(rephora))
        await uasyncio.sleep_ms(100)
        if prom > maxvol:
            rep += 1
            rephora += 1
            if rep > 35:
                rep = 35
        if prom < (maxvol - 10000):
            rep -= 1
            if rep < 0:
                rep = 0
        if (rep > 34 or rephora > 30) and not sended:
            send_level_alert("+573009023621", "4567227", prom)
            print(prom)
            print(rep)
    #         rephora = 0
            sended = True
        if sended and rep <=0 and rephora < 30:
            print(prom)
            print(rep)
            sended = False
            
        if prom > maxlevel:
            maxlevel = prom
        
        if time.time() > nextreport:
            send_level_max("+573009023621", "4567227", maxlevel, rephora)
            print(f"nivel maximo  = {maxlevel}")
            maxlevel = 0
            rephora = 0
            nextreport = time.time() + 3600
