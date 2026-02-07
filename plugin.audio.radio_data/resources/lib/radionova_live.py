import json
import requests
import xbmc

#DEBUG
#from pprint import pprint

# Remplacez 'nova.json' par le chemin correct de votre fichier

# We got only the url stream
# Then we search the radio in the radiodata.json
def get_info_nova(radio_id):
# And call the good module, to find the data (ie artist, ablum ect..)
    xbmc.log("Radio_data: get_info nova nova_id is %s" % radio_id)

    url = "https://www.nova.fr/radios-data/www.nova.fr/all.json"
    infos = {}

    try:
        xbmc.log("Radio_data: get_info url is %s" % url)
        r = requests.get(url)                               
        data = r.json()                                                                                         

        infos['artist'] = ''
        infos['song'] = ''
        infos['fanart'] = ''
        infos['duration'] = ''
        infos['album'] = ''
        infos['dt_end'] = ''
        infos['year'] = ''
        infos['dt_ent'] = ''

        # Parcourir la liste des radios
        for item in data:
            radio_info = item.get('radio', {})
            nova_id = radio_info.get('id', 'Inconnu')
            #print(f"nova_id : {nova_id} x")
            #print(f"radio_id : {radio_id} x")
            if nova_id == radio_id: 
                #print(f"CHECK")
                track_info = item.get('currentTrack', {})

                infos['artist'] = track_info.get('artist', 'Artiste inconnu')
                infos['song'] = track_info.get('title', 'Titre inconnu')
                infos['fanart'] = track_info.get('media_url', 'media absent')
                infos['duration'] = track_info.get('duration', 'media absent')
                infos['diffusion_date'] = track_info.get('diffusion_date', 'inconnu')
                break

    except FileNotFoundError:
        xbmc.log("Erreur : Le fichier %s est introuvable." % url)
    except json.JSONDecodeError:
        xbmc.log("Erreur : Le fichier n'est pas un JSON valide.")
    except Exception as e:
        xbmc.log("Erreur : Une erreur inattendue est survenue. %s" % str(e))
        
    return infos

# DEBUG
#infos = get_info_nova('910')
#pprint(infos)
