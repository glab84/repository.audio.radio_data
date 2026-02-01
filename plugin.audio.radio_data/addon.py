# -*- coding: utf-8 -*-

import os
import xbmc
import xbmcgui
#from resources.lib.mon_scraper import recuperer_infos_stream
import sys
import xbmcplugin
import urllib.parse
#from kodi_six import xbmcvfs, 
import xbmcaddon
import xbmcgui

from resources.lib.manage_data import build_menu_contents, get_info, search_by_radiodata_id, pathfilemenu, build_menu

def start_radio(radio_id):
    # 1. On détermine l'URL du flux selon l'ID
    
    #xbmc.executebuiltin("ActivateWindow(12006)")
    # passe en plein écran
    
    current_item = search_by_radiodata_id(radio_id)
    
    player = xbmc.Player()
    monitor = xbmc.Monitor()

    # Lancement initial
    li = xbmcgui.ListItem(label="Connexion...")
    player.play(current_item["stream_url"], li)

    # 2. Boucle de mise à jour des tags
    last_title = ""
    count = 0
    while not monitor.abortRequested():
        if monitor.waitForAbort(10): # Attendre 10 secondes
            break
        count += 1                        
        if not player.isPlayingAudio():
            break

        # Récupération des infos via votre module
        # (Vous pouvez passer radio_id à votre scraper si besoin)
        infos = get_info(radio_id)

        if player.getPlayingFile() != current_item["stream_url"]:
            xbmc.log("Changement de radio détecté, arrêt de l'ancien script.", xbmc.LOGINFO)
            break
        
        if infos['song'] != last_title:
            
            list_item = xbmcgui.ListItem()
            list_item.setPath(xbmc.Player().getPlayingFile())
            list_item.setArt({"thumb":infos['fanart'], "fanart":infos['fanart']})
            
            list_item.setInfo('music', {
            'title': infos['song'],
            'artist': [infos['artist']], # Artist Slideshow attend souvent une liste
            'album': infos['album'],
            'comment': 'Streaming Radio'
            })

            music_tag = list_item.getMusicInfoTag()
            music_tag.setTitle(infos['song'])
            music_tag.setArtist(infos['artist'])
            music_tag.setAlbum(infos['album'])
            
            xbmc.Player().updateInfoTag(list_item)
            artist_debug = xbmc.Player().getMusicInfoTag().getArtist()
            if artist_debug == "":
                 xbmc.log("Radio_data: Issue artist : %s" % music_tag.setArtist(infos['artist']))

            # Mise à jour de l'image (avec cache-buster)
            li_update = xbmcgui.ListItem()
            li_update.setArt({'thumb': infos['fanart'], 'fanart': infos['fanart']})
            
            # Note: Pour forcer l'affichage sur certains skins :
            xbmc.executebuiltin('ReplaceWindow(busydialog)') # Force un micro-refresh
            xbmc.executebuiltin('Dialog.Close(busydialog)')
            
            last_title = infos['song']

if __name__ == '__main__':
    params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
    if params.get('action') == 'play':
        # Appeler la fonction de lecture (voir étape 2)
        #import playback
        xbmc.log("Radio_data: Play_id is %s" % params.get('id'))
        start_radio(params.get('id'))
        #playback.start_radio(params.get('id'))
    else:
        # menu
        WINDOW = xbmcgui.Window(12006)
        
        mode = params.get("mode", None)
        menuid = params.get("menuid", None)
        xbmc.log("Radio_data: mode id is %s %s" % (mode, menuid))
                
        # initial launch of add-on
        if mode is None:
            if menuid is None:
                build_menu(pathfilemenu())
            else:
                build_menu_contents(pathfilemenu(), menuid)


