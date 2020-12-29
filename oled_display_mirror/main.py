from oled_display_mirror.gamesense import GameSense
import time
import requests
from PIL import Image
import mss

SCT=mss.mss()
IS_MAIN=(__name__=='__main__')

class OLED_Displayer:
    SLEEP_TIME=0.0 #time to sleep between sending frames (minus time spent processing)

    def __init__(self,screen_bounds:tuple,oled_size:tuple):
        self.screen_bounds=screen_bounds
        self.oled_size=oled_size
        self.calc_arr_size=lambda: int((self.oled_size[0]*self.oled_size[1])/8)
        self.gs:GameSense = None
        self.setup()

    def conv_bitmap_array(self,arr:list):
        """
        Convert a numpy array to the pixel array requested by steelseries engine
        """
        if len(arr)<self.oled_size[0]*self.oled_size[1]:
            rows=[]
            for r in range(0,len(arr),len(arr)//self.oled_size[1]):
                rows.append(arr[r:r+len(arr)//self.oled_size[1]-1])
            for i,r in enumerate(rows):
                if len(r)<self.oled_size[0]:
                    rows[i].extend([0 for i in range(self.oled_size[0]-len(r))])
            if len(rows)<self.oled_size[1]:
                rows.extend([[0 for i in range(self.oled_size[0])] for j in range(self.oled_size[1]-len(rows))])
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
    
    def get_bmp_screenshot(self):
        """
        Capture a screenshot and convert it to a bitmap in an NP array
        """
        #capture
        cap=SCT.grab(self.screen_bounds)
        im = Image.frombytes("RGB", cap.size, cap.bgra, "raw", "BGRX")
        #resize
        im.thumbnail((self.oled_size[0],self.oled_size[1]))
        #conv to bitmap
        bmp=im.convert("1",palette="ADAPTIVE",dither=Image.FLOYDSTEINBERG)

        #conv to array
        data=list(bmp.getdata())
        im.close()
        bmp.close()
        return data
    
    def setup(self):
        """
        Run the gamesense app and capture/send the frames (BLOCKING)
        """
        self.gs = GameSense('GRAPHICS', 'Graphics App', 'Wolfinabox')
        reconnect_seconds=1
        while True:
            try:
                r = self.gs.register_game()
                break
            except requests.ConnectionError as e:
                raise ConnectionError('Could not connect to steelseries engine!')

        empty_bmp=[0 for i in range(self.oled_size[0]*self.oled_size[1])]
        empty_bmp=self.conv_bitmap_array(empty_bmp)
        try:
            r = self.gs.bind_event('DISPLAY', handlers=[
                {
                    "datas": [
                        {
                        
                                "has-text": False,
                                "image-data":empty_bmp
                        }
                    ],

                    "device-type": f"screened-{self.oled_size[0]}x{self.oled_size[1]}",
                    "mode": "screen",
                    "zone": "one"
                }
            ])
        except Exception as e:
            print(f'ERROR in binding EVENT: "{e}""')
    
    def run_frame(self):
        if self.gs is None:
            return
        #MAIN CODE
        start_time=time.time()
        bmp=self.get_bmp_screenshot()
        scrnsht_time=time.time()-start_time

        start_time=time.time()
        new_bmp=self.conv_bitmap_array(bmp)
        conv_time=time.time()-start_time

        start_time=time.time()
        data = {
            "value": next(self.gs.value_cycler),
            "frame": {
                f"image-data-{self.oled_size[0]}x{self.oled_size[1]}":new_bmp
            }
        }
        try:
            res = self.gs.send_event("DISPLAY", data)
        except Exception as e:
            print(f'ERROR in sending EVENT: "{e}""')
        end_time=time.time()-start_time
        
        total_time=scrnsht_time+conv_time+end_time
        if IS_MAIN: print(f'Screenshot: {round(scrnsht_time*1000,2)}ms Convert: {round(conv_time*1000,2)}ms Send: {round(end_time*1000,2)}ms Total: {round(total_time*1000,2)}ms')
        time.sleep(self.SLEEP_TIME-total_time if self.SLEEP_TIME>total_time else 0)
        return scrnsht_time,conv_time,end_time


if IS_MAIN:
    shower=OLED_Displayer((0,0,1920,1080),(128,52))
    print('Running without GUI')
    while True:
        shower.run_frame()