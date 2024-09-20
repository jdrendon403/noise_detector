from microdot import Microdot
import wifimgr
import uasyncio


from monitor import monitor

#Connect Wlan
wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D

# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
print("ESP OK")



uasyncio.create_task(monitor())

app = Microdot()

@app.route('/')
async def index(request):
    return 'Hello, world!'

print("starting")
app.run(port=80)
print("started")