#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: MatthieuF44
"""
import time
import requests

def init(c) :
    """Init the Freebox Player to the first menu Télévision --> Freebox TV

    Parameters
    ----------
    c : int
        Remote control code find in Réglages --> Système --> Informations Freebox Player et Server --> Player --> Code télécommande réseau
    """
    request_result = 0
    res = requests.get('http://hd1.freebox.fr/pub/remote_control?code=%i&key=home&repeat=3' %c)
    request_result = request_result + res.status_code
    time.sleep(2)
    res = requests.get('http://hd1.freebox.fr/pub/remote_control?code=%d&key=swap' %c)
    request_result = request_result + res.status_code
    time.sleep(2)
    if request_result == 400:
        print("Initialisation : OK")
    else:
        print("Initialisation : Erreur !")

def tv(c) :
    """Lauch Freebox TV menu

    Parameters
    ----------
    c : int
        Remote control code find in Réglages --> Système --> Informations Freebox Player et Server --> Player --> Code télécommande réseau
    """
    request_result = 0
    res = requests.get('http://hd1.freebox.fr/pub/remote_control?code=%i&key=ok' %c)
    request_result = request_result + res.status_code
    time.sleep(4)
    if request_result == 200:
        print("Lancement menu 'TV' : OK")
    else:
        print("Lancement menu 'TV' : Erreur !")

def radio(c) :
    """Lauch Radio menu

    Parameters
    ----------
    c : int
        Remote control code find in Réglages --> Système --> Informations Freebox Player et Server --> Player --> Code télécommande réseau
    """
    request_result = 0
    res = requests.get('http://hd1.freebox.fr/pub/remote_control?code=%i&key=right&repeat=2' %c)
    request_result = request_result + res.status_code
    time.sleep(0.2)
    res = requests.get('http://hd1.freebox.fr/pub/remote_control?code=%i&key=down&repeat=3' %c)
    request_result = request_result + res.status_code
    time.sleep(0.2)
    res = requests.get('http://hd1.freebox.fr/pub/remote_control?code=%i&key=ok' %c)
    request_result = request_result + res.status_code
    time.sleep(4)
    if request_result == 600:
        print("Lancement menu 'Radio' : OK")
    else:
        print("Lancement menu 'Radio' : Erreur !")

def button(c,t,r=1,l=False) :
    """Press button defined in parameters

    Parameters
    ----------
    c : int
        Remote control code find in Réglages --> Système --> Informations Freebox Player et Server --> Player --> 
        Code télécommande réseau
    t : string
        Name of touch in lowercase : ok, down, up, left, right
    r : int, optional
        Number of the button repetition (default is 1)
    l : bool, optional
        Make a long press on the button when is true (default is False)
    """
    delay = 0
    if t == "ok":
        delay = 4
    if t == "down" or t == "up" or t == "left" or t == "right" :
        delay = 0.5
    if t == "red" or t == "green" or t == "blue" or t == "yellow" :
        delay = 0.5
    if t == "power" or t == "list" or t == "tv" :
        delay = 0.5
    if t == "1" or t == "2" or t == "3" or t == "4" or t == "5" or t == "6" or t == "7" or t == "8" or t == "9" or t == "0" :
        delay = 0.5
    if t == "back" or t == "swap" :
        delay = 0.5
    if t == "info" or t == "epg" or t == "mail" or t == "media" or t == "help" or t == "options" or t == "pip" :
        delay = 1
    if t == "vol_inc" or t == "vol_dec" :
        delay = 0.5
    if t == "prgm_inc" or t == "prgm_dec" :
        delay = 0.5
    if t == "mute" or t == "home"  or t == "rec" :
        delay = 0.5
    if t == "bwd" or t == "prev"  or t == "play"  or t == "fwd"  or t == "next" :
        delay = 0.5

    if delay > 0:
        if l == False:
            if r > 1:
                if r > 10:
                    delay = delay + 0.2
                res = requests.get('http://hd1.freebox.fr/pub/remote_control?code=%i&key=%s&repeat=%i' %(c,t,r))
            else:
                res = requests.get('http://hd1.freebox.fr/pub/remote_control?code=%i&key=%s' %(c,t))
        elif l == True:
            res = requests.get('http://hd1.freebox.fr/pub/remote_control?code=%i&key=%s&long=true' %(c,t))
        time.sleep(delay)
        if res.status_code == 200:
            print("Appui sur la touche '%s' %i fois : OK" %(t,r))
        else:
            print("Appui sur la touche '%s' %i fois : Erreur !" %(t,r))
    else:
        print("La touche %s n'est pas connue !" %t)