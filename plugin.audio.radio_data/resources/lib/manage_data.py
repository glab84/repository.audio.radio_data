# -*- coding: utf-8 -*-
import json
import os
from urllib.request import urlopen
import xbmc
import xbmcgui
import xbmcplugin
import sys
from urllib.parse import urlencode
from resources.lib.radiofrance_live import get_info_radiofrance_api
from resources.lib.rfm_live import get_info_rfm
from resources.lib.jazzradio_live import get_info_jazzradio_xml
from resources.lib.radionova_live import get_info_nova
import xbmcaddon

# Manage radio_data json file
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])

def pathfilemenu():
    # Identifiant du plugin
    base_url = sys.argv[0]
    addon_handle = int(sys.argv[1])
    _addon_ = xbmcaddon.Addon()
    filemenu = "radio_data.json"
    path = _addon_.getAddonInfo("path")
    menujson = os.path.join(path, filemenu)
    xbmc.log("Radio_data: json_file is %s" % menujson)
    return menujson

# Get info according to radio type
def get_info(radio_id):

    radio_type = search_by_radiodata_id(radio_id).get("radiodata_type")
    xbmc.log("Radio_data: get_info radio_type %s" % radio_type)

    match radio_type:
        case "radiofrance_api":
            return get_info_radiofrance_api(radio_id)
        
        case "nova":
            return get_info_nova(radio_id)

        case "rfm_json":
            return get_info_rfm(radio_id)

        case "jazzradio_xml":
            return get_info_jazzradio_xml(radio_id)
        
        case None:
            xbmc.log("Radio_data: get_info non trouvé %s" % radio_type)
            return None
            
        case _: # Cas par défaut (wildcard)
            xbmc.log("Radio_data: get_info non prévu %s" % radio_type)
            return None

# Search radio by radiodata_id in radio_data.json
def search_by_radiodata_id(target_id):
    try:
        with open(pathfilemenu(), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Parcourir chaque groupe de radio (Fip, Rfm, etc.)
        for radio in data.get("menu", []):
            # Accéder à la liste des sous-chaînes (menuitem)
            menu_items = radio.get("contents", {}).get("menuitem", [])
            
            for item in menu_items:
                # Vérifier si le radiodata_id correspond
                if item.get("radiodata_id") == str(target_id):
                    xbmc.log("Radio_data: trouvé %s" % item["value"])
                    return item
                
        xbmc.log("Radio_data: non trouvé %s" % target_id)
        return None

    except FileNotFoundError:
        return "Erreur : Fichier JSON introuvable"
    except json.JSONDecodeError:
        return "Erreur : Format JSON invalide"

def build_url(query):
    base_url = sys.argv[0]
    return base_url + "?" + urlencode(query)

def build_menu(menujson):
    xbmcplugin.setPluginCategory(addon_handle, "Main Menu")
    xbmcplugin.setContent(addon_handle, "stream")
    xbmc.log("Radio_data: json_file is %s" % menujson)

    with open(menujson) as json_file:
        menu = json.load(json_file)

    for p in menu["menu"]:
        list_item = xbmcgui.ListItem(label=p["value"])
        list_item.setArt({"thumb": p["fanart"],
                          "icon": p["fanart"],
                          "fanart": p["fanart"]})
        list_item.setInfo("stream", {"title": p["value"],
                                    "genre": p["value"],
                                    "mediatype": "stream"})
        #TODO
        #URL MENU
        url = build_url({"action": "listing", "menuid": p["id"]})
        is_folder = True
        xbmcplugin.addDirectoryItem(addon_handle, url, list_item, is_folder)

    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(addon_handle)

def build_menu_contents(menujson, id):
    with open(menujson) as json_file:
        menu = json.load(json_file)

    song_list = []

    n = 0
    for p1 in menu["menu"]:
        if p1["id"] == id:
            # si json rf n'exite plus ? inutile
            try:
              rf_url_json = p1["rf_url_json"]
              response = urlopen(rf_url_json) 
              data_json = json.loads(response.read()) 
  
              for p2 in data_json:
                 try:
                   n += 1
                   title = p2.get("name").encode("utf-8")
                   flux = p2["streams"]["live"][0]["url"]
                   visual = p2["logo"]["webpSrc"]
                   list_item = xbmcgui.ListItem(label=title)

                   list_item.setArt({"thumb": visual, "fanart": p1["fanart"]})
                   list_item.setProperty("IsPlayable", "true")
                   list_item.setInfo("music", {"title": title, "genre": title})
                   url = build_url({"mode": "stream", "url": flux, "title": title})
                   
                   #url = f"{base_url}?action=play&id={radio['id']}"
                   xbmc.log("Radio_data: Play_url is %s" % url)

                   song_list.append((url, list_item, False))
                 except:
                   flux = ""  
                   # no thing to do, how to check define value ?
            except:
              # sinon
              for p2 in p1["contents"]["menuitem"]:
                 n += 1
                 title = p2.get("value")
                 flux = p2["stream_url"]
                 if p2["fanart"] != "" :
                    visual = p2["fanart"]
                 else:
                    #artist, song, fanart, year, duration, album, dt_end = get_info_playing_file(flux)
                    visual = "void"
                 list_item = xbmcgui.ListItem(label=title)
                 #list_item = xbmcgui.ListItem(label=title, thumbnailImage=visual)
                 # setArt

                 list_item.setArt({"thumb": visual, "fanart": p1["fanart"]})
                 list_item.setProperty("IsPlayable", "true")
                 list_item.setInfo("music", {"title": title, "genre": title})
                 #url = build_url({"mode": "stream", "url": flux, "title": title})
                 url = f"{base_url}?action=play&id={p2['radiodata_id']}"
                 xbmc.log("Radio_data: Play_url is %s" % url)

                 song_list.append((url, list_item, False))

    xbmcplugin.addDirectoryItems(addon_handle, song_list, len(song_list))
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)
