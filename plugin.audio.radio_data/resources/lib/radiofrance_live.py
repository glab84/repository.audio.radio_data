import json
import requests
import re
import xbmc
from datetime import datetime

#DEBUG
#from pprint import pprint

# We got only the url stream
# Then we search the radio in the radiodata.json
# And call the good module, to find the data (ie artist, ablum ect..)
# il manque l'image
def get_info_rf_transitor(radio_id):                                                                      
    xbmc.log("Radio_data: get_info transitor id is %s" % radio_id)
    infos = {}
    infos['artist'] = ''
    infos['song'] = ''
    infos['fanart'] = ''
    infos['duration'] = ''
    infos['album'] = ''
    infos['start'] = ''
    infos['end'] = ''
    infos['year'] = ''
    infos['dt_ent'] = ''
    
    try:                   
        # possible de choisr la resolution
        url = "https://api.radiofrance.fr/livemeta/live/%s/transistor_musical_player?preset=400x400" % radio_id
        xbmc.log("Radio_data: get_info transitor url is %s" % url)
        r = requests.get(url)                               
        info = r.json()                                                                                         
        v1 = info["now"]                                
                            
        secondLine = v1.get("secondLine", "") 
        xbmc.log("Radio_data: get_info transitor secondLine is %s" % secondLine)        
        # secondLine : artist . song
        # Sample : IJulia Fischer • Caprice pour violon en mi min op 1 n°15
        m = re.search('(.*) • (.*)', secondLine)
        infos['artist'] = m.group(1)
        infos['song'] = m.group(2)
        xbmc.log("Radio_data: get_info transitor song is %s" % infos['song'])        

        infos['fanart'] = v1.get("cover", "") # Empty !
        infos['start'] = v1.get("startTime", "") 
        infos['end'] = v1.get("endTime", "") 
        infos['dt_end'] = datetime.fromtimestamp(infos['end'])                                 
        infos['duration'] = '0'      
        xbmc.log("Radio_data: get_info transitor end is %s" % infos['end'])        
    
        #infos['duration'] = infos['end'] - infos['start']      
        xbmc.log("Radio_data: get_info transitor Artists is %s" % infos['artist'])        
        xbmc.log("Radio_data: get_info transitor fanart is %s" % infos['fanart'])        
    except:                                                     
        #duration = infos['end'] - infos['start']                            
        infos['dt_end'] = datetime.min                                                                              
    
    return infos   

def retrieve(url):
    data = requests.get(url).json()
    level = data['levels'][0]
    uid = level['items'][level['position']]
    step = data['steps'][uid]
    return step

def get_info_radiofrance_api(radio_id):
    xbmc.log("Radio_data: get_info transitor id is %s" % radio_id)
    infos = {}
    infos['artist'] = ''
    infos['song'] = ''
    infos['fanart'] = ''
    infos['duration'] = ''
    infos['album'] = ''
    infos['start'] = ''
    infos['end'] = ''
    infos['year'] = ''
    infos['dt_ent'] = ''
    
    radiodata_url = "https://api.radiofrance.fr/livemeta/pull/%s" % radio_id
                    
    xbmc.log("Radio_data: get_info api url is %s" % radiodata_url)
    try:
        
        data = retrieve(radiodata_url)
        infos['song'] = data.get("title", "")
        infos['artist'] = data.get("authors", "")
        infos['year'] = data.get("anneeEditionMusique", "")
        infos['album'] = data.get("titreAlbum", "")
        infos['fanart'] = data.get("visual", "")
        infos['start'] = data.get("start", "")
        infos['end'] = data.get("end", "")
        xbmc.log("Radio_data: get_info radiofrance end is %s" % infos['end'])        

        #infos['duration'] = infos['end'] - infos['start']      
        xbmc.log("Radio_data: get_info radiofrance Artists is %s" % infos['artist'])        
        xbmc.log("Radio_data: get_info radiofrance fanart is %s" % infos['fanart'])        
    except:                                                     
        #duration = infos['end'] - infos['start']                            
        infos['dt_end'] = datetime.min                                                                              
    
    return infos
    