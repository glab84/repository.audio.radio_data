import json
import requests
import re
import xbmc
from datetime import datetime
import xml.etree.ElementTree as ET
import resources.lib.manage_data as manage_data

#DEBUG
#from pprint import pprint

# We got only the url stream
# Then we search the radio in the radiodata.json
# And call the good module, to find the data (ie artist, ablum ect..)
def get_info_jazzradio_xml(radiodata_id):
    
    jazzradio_item = manage_data.search_by_radiodata_id(radiodata_id)

    infos = {}
    infos['duration'] = ''
    infos['album'] = ''
    infos['dt_end'] = ''
    infos['year'] = ''
    infos['dt_ent'] = ''

    xbmc.log("Radio_data: get_info jazzradio url is %s" % jazzradio_item['radiodata_url'])
    try:
        r = requests.get(jazzradio_item['radiodata_url'])
        root = ET.fromstring(r.content)

    
        try:
            for child in root:
                for child2 in child:
                    if child2.tag == "chanteur":
                        infos['artist'] = child2.text
                    if child2.tag == "chanson":
                        infos['song'] = child2.text
                    if child2.tag == "pochette":
                        infos['fanart'] = child2.text
                break
        except:
            infos['artist'] = ''
            infos['song'] = ''
            infos['fanart'] = ''

        xbmc.log("Radio_data: Artists is %s" % infos['artist'])
        xbmc.log("Radio_data: Fan Art is %s" % infos['fanart'])
    except:
        infos['artist'] = ''
        infos['song'] = ''
        infos['fanart'] = ''

    #dt_end = datetime.min
    return infos

