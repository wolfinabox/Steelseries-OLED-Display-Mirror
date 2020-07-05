from gamesense import GameSense
import time
from systray import create_system_tray
import requests
import pyscreenshot
from PIL import Image


SLEEP_TIME=0.1 #time to sleep between sending frames (minus time spent processing)
WIDTH,HEIGHT=128,52 #dimensions of OLED screen. affects image scaling and targetted devices
SCREEN_BOUNDS=(0,0,1920,1080) #bounds of PC screen to screenshot
ARR_SIZE=int((WIDTH*HEIGHT)/8)

def conv_bitmap_array(arr:list):
    if len(arr)<WIDTH*HEIGHT:
        rows=[]
        for r in range(0,len(arr),len(arr)//HEIGHT):
            rows.append(arr[r:r+len(arr)//HEIGHT-1])
        for i,r in enumerate(rows):
            if len(r)<WIDTH:
                rows[i].extend([0 for i in range(WIDTH-len(r))])
        if len(rows)<HEIGHT:
            rows.extend([[0 for i in range(WIDTH)] for j in range(HEIGHT-len(rows))])
        arr=[a for b in rows for a in b]
                

    new_arr=[]
    temp_byte=''
    for c in arr:
        if int(c)>1:c=1
        temp_byte+=str(c)
        if len(temp_byte)==8:
            new_arr.append(int(temp_byte,2))
            temp_byte=''

    
    return new_arr

def get_bmp_screenshot():
    #capture
    im:Image.Image=pyscreenshot.grab(SCREEN_BOUNDS)
    #resize
    im.thumbnail((WIDTH,HEIGHT))
    #conv to bitmap
    bmp=im.convert("1",palette="ADAPTIVE",colors=2)
    #conv to array
    data=list(bmp.getdata())
    im.close()
    bmp.close()
    return data

STOP=False
def _on_quit(systray):
    global STOP
    STOP=True
tray=create_system_tray(on_quit=_on_quit,title="Graphics OLED")
gs = GameSense('GRAPHICS', 'Graphics App', 'Wolfinabox')
reconnect_seconds=1
while True:
    try:
        r = gs.register_game(reset=True)
        break
    except requests.ConnectionError as e:
        print(f'Could not connect to steelseries engine! Reconnecting in {reconnect_seconds}s...')
        time.sleep(reconnect_seconds)
        gs.req_url=gs.get_req_url()

empty_bmp=[0 for i in range(WIDTH*HEIGHT)]
empty_bmp=conv_bitmap_array(empty_bmp)
try:
    r = gs.bind_event('DISPLAY', handlers=[
        {
            "datas": [
                {
                   
                        "has-text": False,
                        "image-data":empty_bmp
                }
            ],

            "device-type": f"screened-{WIDTH}x{HEIGHT}",
            "mode": "screen",
            "zone": "one"
        }
    ])
except Exception as e:
    print(f'ERROR in binding EVENT: "{e}""')




#MAIN CODE
while not STOP:
    start_time=time.time()
    bmp=get_bmp_screenshot()
    scrnsht_time=time.time()-start_time

    start_time=time.time()
    new_bmp=conv_bitmap_array(bmp)
    conv_time=time.time()-start_time

    start_time=time.time()
    data = {
        "value": next(gs.value_cycler),
        "frame": {
             f"image-data-{WIDTH}x{HEIGHT}":new_bmp
        }
    }
    try:
        res = gs.send_event("DISPLAY", data)
    except Exception as e:
        print(f'ERROR in sending EVENT: "{e}""')
    end_time=time.time()-start_time
    
    total_time=scrnsht_time+conv_time+end_time
    print(f'Screenshot: {round(scrnsht_time*1000,2)}ms Convert: {round(conv_time*1000,2)}ms Send: {round(end_time*1000,2)}ms Total: {round(total_time*1000,2)}ms')
    time.sleep(SLEEP_TIME-total_time if SLEEP_TIME>total_time else 0)