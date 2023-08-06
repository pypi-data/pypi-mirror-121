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

    if delay > 0:
        if l == False:
            if r > 1:
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