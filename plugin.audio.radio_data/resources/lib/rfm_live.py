import json
import requests
import re
import xbmc
from datetime import datetime
import resources.lib.manage_data as manage_data

#DEBUG
#from pprint import pprint

# We got only the url stream
# Then we search the radio in the radiodata.json
# And call the good module, to find the data (ie artist, ablum ect..)

def get_info_rfm(radiodata_id):
    
    rfm_item = manage_data.search_by_radiodata_id(radiodata_id)

    infos = {}
    infos['duration'] = ''
    infos['album'] = ''
    infos['dt_end'] = ''
    infos['year'] = ''
    infos['dt_ent'] = ''

    xbmc.log("Radio_data: get_info rfm url is %s" % rfm_item['radiodata_url'])
    # try ...
    r = requests.get(rfm_item['radiodata_url'])
    info = r.json()
    c1 = info["current"]
    
    infos['song'] = c1.get("title","").encode("utf-8")
    infos['artist'] = c1.get("artist","")
    #    artist.rstrip() # Don't work !
    infos['album'] = ''
    infos['fanart'] = c1.get("cover","")
    infos['duration'] = c1.get("duration")
    
    dt_end = datetime.min
    xbmc.log("Radio_data: get_info transitor song is %s" % infos['song'])        
    
    return infos   
