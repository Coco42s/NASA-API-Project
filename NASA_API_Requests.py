#!/usr/bin/env python3.11

from tkinter import *
from tkinter import ttk, messagebox
from customtkinter import *
from tkVideoPlayer import TkinterVideo
from pydub.playback import play
from moviepy.editor import VideoFileClip
from pytube import YouTube
from requests import get
from urllib.request import getproxies
import requests, json, pygame
from PIL import Image, ImageTk 
from datetime import datetime, timedelta
import os, re
import time

# ----- FONCTION -----#

# Fonction pour le code
def variable_init():
    """ Cette fonction definit tout un ta de variable pour le bonfonctionement de l'application
    """
    if not code_deja_execute.get():
        code_deja_execute.set(True)
        global apod,photo,date_du_hier,name_current_api,choix_MRP_robot,color,ch_col,script_dir,date_du_jour,choice_public_mrp,choice_public_epic,key_api,OpPAR
        apod,photo,name_current_api,choix_MRP_robot,color,ch_col,choice_public_mrp,choice_public_epic,script_dir,OpPAR = False,"",None,"curiosity",[["#FFFFFF"],["#2d2d30"]],0,None,None,os.path.dirname(os.path.abspath(__file__)),False
        
        key_api = ""
        
        aujourdhui = datetime.today()
        hier = aujourdhui - timedelta(days=1)
        date_du_jour,date_du_hier = aujourdhui.strftime("%Y-%m-%d"),hier.strftime("%Y-%m-%d")
        
        fenetre.iconbitmap(os.path.join(script_dir, "assets//icons8-nasa-16.png"))
        image = PhotoImage(file=os.path.join(script_dir, "assets//icons8-nasa-16.png"))
        fenetre.iconphoto(False, image)

def verifie_format_date(chaine):
    """ Cette fonction verifier une une chane de caractaire est au forma XXXX-XX-XX

    Args:
        chaine (_str_): chaine de caractaire a vérifier

    Returns:
        _Bool_: Boleain qui est a True si la chaine a le bon format
    """
    if re.match(re.compile(r'^\d{4}-\d{2}-\d{2}$'), chaine): return True
    return False

def charge_color():
    """ Cette fontion permè de changer les couleur de sertain élément 
    """
    global ch_col
    if ch_col == 0:
        ch_col = 1
        color_change.configure(text="☾")
    else:
        ch_col = 0
        color_change.configure(text="☼")
    fenetre.configure(fg_color=color[ch_col][0])  
    list_API.config(bg=color[ch_col][0])
    
    
    if OpPAR == True:
        ViewPAR.configure(bg=color[ch_col][0])
        Title.configure(bg_color=color[ch_col][0])
        API_KEY_text.configure(bg_color=color[ch_col][0])
        API_KEY_entry.configure(bg_color=color[ch_col][0])
        Applay.configure(bg_color=color[ch_col][0])
        Retour.configure(bg_color=color[ch_col][0])
        FrameView.configure(bg=color[ch_col][0])
    
    if name_current_api == "APOD":
        window_width = fenetre.winfo_width()
        if window_width < 1220: ViewAPI.configure(fg_color=color[ch_col][0])
        else: ViewAPI.configure(bg=color[ch_col][0])
        Title.configure(bg_color=color[ch_col][0])
        FrameView.configure(bg=color[ch_col][0])
        FrameText.configure(bg=color[ch_col][0])
        View.configure(bg=color[ch_col][0])
        Paramètre.configure(bg=color[ch_col][0])
        Entry_p.configure(bg_color=color[ch_col][0])
        ReloadAPOD.configure(bg_color=color[ch_col][0])
        labelText.configure(bg_color=color[ch_col][0])
    
    if name_current_api == "MRP":
        window_width = fenetre.winfo_width()
        if window_width < 1220: ViewAPI.configure(fg_color=color[ch_col][0])
        else: ViewAPI.configure(bg=color[ch_col][0])
        Title.configure(bg_color=color[ch_col][0])
        FrameView.configure(bg=color[ch_col][0])
        View.configure(bg=color[ch_col][0])
        Paramètre.configure(bg=color[ch_col][0])
        Entry_p.configure(bg_color=color[ch_col][0])
        ReloadMRP.configure(bg_color=color[ch_col][0])
        Rover_label.configure(bg_color=color[ch_col][0])
        Camera_label.configure(bg_color=color[ch_col][0])
        Camera_combobox.configure(bg_color=color[ch_col][0])
        Rover_combobox.configure(bg_color=color[ch_col][0])
        
    if name_current_api == "EPIC":
        window_width = fenetre.winfo_width()
        if window_width < 945: ViewAPI.configure(fg_color=color[ch_col][0])
        else: ViewAPI.configure(bg=color[ch_col][0])
        Title.configure(bg_color=color[ch_col][0])
        FrameView.configure(bg=color[ch_col][0])
        View.configure(bg=color[ch_col][0])
        Paramètre.configure(bg=color[ch_col][0])
        Entry_p.configure(bg_color=color[ch_col][0])
        ReloadEPIC.configure(bg_color=color[ch_col][0])

def download(url, path_file, bool):
    """Cette fonction set a délécharger des fichier et afficher sa progresion 

    Args:
        url (_str_): lien ver la chose a télécharger
        path_file (_str_): chmain ver lequelle le fichier va ètre télécharger
        bool (_Bool_): boolean qui sert a savoir si on doit le mètre sou forme de json 

    Returns:
        _dict, list_: _description_
    """
    global progress_window
    
    progress_window = Toplevel(fenetre)
    progress_window.title("Downloading...")

    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    progress_bar['maximum'] = total_size
    progress_bar['value'] = 0

    with open(path_file, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                progress_bar["value"] += len(chunk)
                fenetre.update()
    progress_window.destroy()
    
    if bool == True:
        with open(path_file, 'r') as json_file: 
            data = json.load(json_file)
        return data

def main_widget():
    """ Cette fonction créé l'interface principal.
    """
    global color_change, list_API
    
    # Header
    Header = Frame(fenetre, bg="#00205B")
    Header.pack(fill="x")

    Title_Header = Label(Header, text="NASA API Request", font=("Nasalization Rg",25, 'bold'), bg="#00205B",fg="white")
    Title_Header.pack(side="left", padx=40)
    
    parametre = CTkButton(Header, text="⚙", font=("Arial",20), width=50 , height=15)
    parametre.bind("<Button-1>", lambda event: (PAR_Toggle()))
    parametre.pack(side="right",padx=(15,40))
    
    color_change = CTkButton(Header, text="☼",font=("Arial",20), width=50 , height=15)
    color_change.bind("<Button-1>", lambda event: (charge_color()))
    color_change.pack(side="right", padx=15)
    
    
    

    #List API
    global name_current_api
    list_API = Frame(fenetre, bg="#FFFFFF")
    list_API.pack(fill="x", anchor=CENTER, pady=20)

    list_API.grid_rowconfigure(0, weight=1)
    for i in range(3): list_API.grid_columnconfigure(i, weight=1)

    MRP = CTkButton(list_API, text="Mars Rover Photos", fg_color="gray", hover_color="#9f9f9f", text_color="white", corner_radius=5, font=("Nasalization Rg",15))
    MRP.bind("<Button-1>", lambda event: (destroy_element(name_current_api),name_api_curent_execute("MRP"),MRP_fonc()))
    MRP.grid(column=0, row=0)

    APOD = CTkButton(list_API, text="Astronomie Picture Of the Day", fg_color="gray",  hover_color="#9f9f9f", text_color="white", corner_radius=5, font=("Nasalization Rg",15))
    APOD.bind("<Button-1>", lambda event: (destroy_element(name_current_api),name_api_curent_execute("APOD"), APOD_fonc()))
    APOD.grid(column=1, row=0)

    EPIC= CTkButton(list_API, text="  Épopée DSCOVR  ", fg_color="gray",  hover_color="#9f9f9f", text_color="white", corner_radius=5, font=("Nasalization Rg",15))
    EPIC.bind("<Button-1>", lambda event: (destroy_element(name_current_api),name_api_curent_execute("EPIC"), EPIC_fonc()))
    EPIC.grid(column=2, row=0)

#Warnings

#Parametres

def PAR_Toggle():
    global OpPAR
    destroy_element(name_current_api)
    if OpPAR == False:
        PAR_Interfaces()
        OpPAR = True
    else:
        destroy_element("PARA")
        OpPAR = False

def PAR_Interfaces():
    global ViewPAR,Title,FrameView,API_KEY_text,API_KEY_entry,Applay,Retour
    ViewPAR = Frame(fenetre, bg=color[ch_col][0]) 
    ViewPAR.pack(anchor=CENTER, pady=20, expand=True)

    Title = CTkLabel(ViewPAR, text="Paramètre", font=("Nasalization Rg",30, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
    Title.pack(anchor='center', padx=40)

    FrameView = Frame(ViewPAR,bg=color[ch_col][0]) 
    FrameView.pack(anchor=CENTER,pady=(70,0))
    
    API_KEY_text = CTkLabel(FrameView, text="API_KEY : ", font=("Nasalization Rg",13, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
    API_KEY_text.grid(column=0,row=0,pady=5)
    
    API_KEY_entry= CTkEntry(FrameView, placeholder_text="Your Nasa API Keys", fg_color="#00205B",text_color="white", corner_radius=5)
    API_KEY_entry.grid(column=1,row=0, padx=5)
    
    Applay = CTkButton(FrameView, text="Apliquer", fg_color="gray", hover_color="#9f9f9f", text_color="white", corner_radius=5, font=("Nasalization Rg",15), command= API_KEY_Change)
    Applay.grid(column=1,row=1,padx=5, pady=3)
    
    Retour = CTkButton(FrameView, text="Retour", fg_color="gray", hover_color="#9f9f9f", text_color="white", corner_radius=5, font=("Nasalization Rg",15), command= PAR_Toggle)
    Retour.grid(column=0,row=1,padx=5)
    
def API_KEY_Change():
    global key_api
    key_api = API_KEY_entry.get()
    PAR_Toggle()
    
    


# Configuration du proxy pour request
def get_active_proxy():
    """ Cette fonction permet de mètre dans un dictionaire les information du proxie actif

    Returns:
        _NoneType, dict_: si il y a un proxi d'activer alors sa renvoie un dictionaire avec le proxies sinon il renvoi None si il y a une ereure demème (None)
    """ 
    try:
        proxies = getproxies()
        active_proxy = None
        for protocol, proxy_url in proxies.items():
            if proxy_url:
                active_proxy = {protocol: proxy_url}
                break
        return active_proxy
    except Exception as e: print(f"Erreur lors de la récupération du proxy actif : {e}")

def proxy_init():
    """ Cette fonction permet d'apliquer un proxy a request si il y a un proxie actif sur la machine. 
    
    IMPORTENT : 
        - le proxie doi ètre noté avec l'ip et le port.
    """
    global API_r
    if not code_deja_execute_proxy.get():
        code_deja_execute_proxy.set(True)
        API_r, active_proxy = requests.Session(), get_active_proxy()
        if active_proxy:
            for protocol in active_proxy:
                API_r.close()
                API_r = requests.Session()
                API_r.proxies.update(active_proxy)
                
# Debut Fonction APOD
def reload_apod(date=None):
    """ Cette fonction permet de recharger APOD avec une nouvelle date

    Args:
        date (_str_, optional): Nouvelle date. Defaults to None.
    """
    global View,labelText
    if date is None: date = Entry_p.get()
    if os.path.exists(os.path.join(script_dir, "assets/APOD/audio_temp.wav")):
        pygame.mixer.music.stop()
        pygame.mixer.quit() 
        os.remove(os.path.join(script_dir, "assets/APOD/audio_temp.wav"))
    API = get_apod(date)
    if API == None: return
    Title.configure(text=API["title"])
    if API["media_type"] ==  "video": APOD_video(API)
    else: APOD_picture(API)

def resize_video(event):
    """ Cette fontion permet a la vido de saficher a la bonne taile

    Args:
        event (_<class 'tkinter.Event'>_): event tkinter
    """
    View.config(width=640, height=360)

def get_apod(date=None):
    """ Cette fonction permet de télécharger le fichier d'unformation de APOD

    Args:
        date (_str_, optional): Data voulu pou APOD. Defaults to None.

    Returns:
        _dict_: fichier d'information télécharger
    """
    API = None
    if date is not None:
        API = download(f"https://api.nasa.gov/planetary/apod?api_key={key_api}&date="+str(date)+"",os.path.join(script_dir, "assets/JSON_DOWNLOAD_ACTUEL.json"),True)
        if "code" in API:
            if "code" != 200:
                messagebox.showinfo("API error", API["msg"])
                API = None
                return
    else:
        API = download(f"https://api.nasa.gov/planetary/apod?api_key={key_api}&date="+str(date_du_jour)+"",os.path.join(script_dir, "assets/JSON_DOWNLOAD_ACTUEL.json"),True)
        if "code" in API:
            API = download(f"https://api.nasa.gov/planetary/apod?api_key={key_api}&date="+str(date_du_hier)+"",os.path.join(script_dir, "assets/JSON_DOWNLOAD_ACTUEL.json"),True)
            if "code" in API:
                if API["code"] != 200:
                    messagebox.showinfo("API error", API["msg"])
                    return
    return API

def APOD_Interfaces():
    """ Cette fonction definie la grand interface de APOD
    """
    if not code_deja_execute_APOD_Interface.get():
        code_deja_execute_APOD_Interface.set(True)
    
        global Title,FrameView,View,FrameText,Paramètre,Entry_p,ReloadAPOD,labelText,ViewAPI
        ViewAPI = Frame(fenetre, bg=color[ch_col][0]) 
        ViewAPI.pack(anchor=CENTER, pady=20, expand=True)#fill=BOTH
        
        Title = CTkLabel(ViewAPI, text="", font=("Nasalization Rg",30, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
        Title.pack(anchor='center', padx=40)

        FrameView = Frame(ViewAPI,bg=color[ch_col][0]) 
        FrameView.pack(anchor=CENTER)
        
        View = Canvas(FrameView, width=640, height=360 ,bg=color[ch_col][0], borderwidth=0, highlightthickness=0)
        View.grid(column = 0,row=0, padx=30, pady=40)

        FrameText = Frame(FrameView, width=460, height=360, bg=color[ch_col][0])
        FrameText.grid(column=1,row=0, padx=30)
         
        Paramètre = Frame(FrameView, bg=color[ch_col][0])
        Paramètre.grid(column=0,row=1, padx=50)
        

        Entry_p = CTkEntry(Paramètre, placeholder_text="Date : YYYY-MM-DD", fg_color="#00205B",text_color="white", corner_radius=5)
        Entry_p.grid(column=0,row=0,padx=5)

        ReloadAPOD = CTkButton(Paramètre, text="Recharger", fg_color="gray", hover_color="#9f9f9f", text_color="white", corner_radius=5, font=("Nasalization Rg",15), command= reload_apod)
        ReloadAPOD.grid(column=1,row=0,padx=5)

        labelText = CTkLabel(FrameText, text = "",font=("Nasalization Rg",13), fg_color="#00205B",text_color="white", corner_radius=5, wraplength=460)
        labelText.pack()

def APOD_Interfaces_low():
    """ Cette fonction definie la petit interface de APOD
    """
    global Title,FrameView,View,FrameText,Paramètre,Entry_p,ReloadAPOD,labelText,ViewAPI
    ViewAPI = CTkScrollableFrame(fenetre, fg_color=color[ch_col][0]) 
    ViewAPI.pack(fill=BOTH, anchor=CENTER, pady=20, expand=True)

    Title = CTkLabel(ViewAPI, text="", font=("Nasalization Rg",30, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
    Title.pack(anchor='center', padx=40, pady=10)

    FrameView = Canvas(ViewAPI, bg=color[ch_col][0],borderwidth=0, highlightthickness=0) 
    FrameView.pack(anchor=CENTER)

    View = Canvas(FrameView, width=640, height=360 ,bg=color[ch_col][0], borderwidth=0, highlightthickness=0)
    View.grid(column = 0,row=1)

    FrameText = Frame(FrameView, width=460, height=360, bg=color[ch_col][0])
    FrameText.grid(column=0,row=0, pady=30)

    Paramètre = Frame(FrameView, bg=color[ch_col][0])
    Paramètre.grid(column=0,row=2, pady=30)

    Entry_p = CTkEntry(Paramètre, placeholder_text="Date : YYYY-MM-DD", fg_color="#00205B",text_color="white", corner_radius=5)
    Entry_p.grid(column=0,row=0)

    ReloadAPOD = CTkButton(Paramètre, text="Recharger", fg_color="gray", hover_color="#9f9f9f", text_color="white", corner_radius=5, font=("Nasalization Rg",15), command= reload_apod)
    ReloadAPOD.grid(column=1,row=0,padx=10)

    labelText = CTkLabel(FrameText, text="",font=("Nasalization Rg",13), fg_color="#00205B",text_color="white", corner_radius=5, wraplength=460)
    labelText.pack()

def APOD_video(API, dl=None):
    """ Cette fonction permet d'afficher la vidéo d'APOD

    Args:
        API (_dict_): fichier d'information en cour
        dl (_type not define_, optional): permet de savoir si on doi télécharger la video ou pas. Defaults to None.
    """
    global View,FrameView,labelText
    View.destroy()
    if dl is None:
        link = API["url"]
        video = YouTube(link)
        stream = video.streams.get_highest_resolution()
        stream.download(filename = os.path.join(script_dir, "assets/APOD/APOD.mp4"))  
    View = TkinterVideo(master=FrameView,width=640, height=360, scaled=True, consistant_frame_rate = True)  
    View.load(os.path.join(script_dir, r"assets/APOD/APOD.mp4"))
    View.set_size((640, 360)) # taille de la video
    View.set_resampling_method(5) # eéchentillonage
    window_width = fenetre.winfo_width()
    if window_width < 1220: View.grid(column = 0,row=1, pady=20)
    else: View.grid(column = 0,row=0, padx=60, pady=40)
    FrameView.bind("<Configure>", resize_video)
    pygame.init()
    video_url = os.path.join(script_dir, "assets/APOD/APOD.mp4")
    audio_file = os.path.join(script_dir, "assets/APOD/audio_temp.wav")
    clip = VideoFileClip(video_url)
    clip.audio.write_audiofile(audio_file)
    pygame.mixer.music.load(audio_file)
    View.play()
    pygame.mixer.music.play()
    labelText.configure(text = API["explanation"]) 

def APOD_picture(API, dl=None):
    """ Cette fonction permet d'afficher l'image d'APOD

    Args:
        API (_dict_): fichier d'information en cour
        dl (_type not define_, optional): permet de savoir si il faut télécharger l'image. Defaults to None.
    """
    global View,photo,FrameView,labelText
    if dl is None: download(API["url"], os.path.join(script_dir, "assets/APOD/APOD_image.jpg"),False)
    View.destroy()
    image = Image.open(os.path.join(script_dir, "assets/APOD/APOD_image.jpg")) 
    image.thumbnail((640,360))
    x,y = (640-image.size[0])/2, (360-image.size[1])/2
    photo = ImageTk.PhotoImage(image)
    View = Canvas(FrameView, width=620, height=360, bg=color[ch_col][0],borderwidth=0, highlightthickness=0)
    window_width = fenetre.winfo_width()
    if window_width < 1220: View.grid(column = 0,row=1)
    else: View.grid(column = 0,row=0, padx=30, pady=40)
    View.create_image(x,y, anchor='nw', image=photo)
    labelText.configure(text = API["explanation"])

def APOD_fonc(API=None):
    """ Cette fonction est la fonction initale d'APOD elle affiche la dergnière image disponible

    Args:
        API (_type_, optional): _description_. Defaults to None.
    """
    API = get_apod()
    download(API["url"], os.path.join(script_dir, "assets/APOD/APOD_image.jpg"),False)
    window_width = fenetre.winfo_width()
    if window_width < 1220: APOD_Interfaces_low(); inf.set(True)
    else: APOD_Interfaces()
    Title.configure(text=API["title"])
    if API["media_type"] ==  "video": APOD_video(API)
    else: APOD_picture(API, 0)
#Fin Fonction APOD

#debut MRP Fonc
def rover_combobox(choice):
    """ Cette fonction permet dafichier les caméra du robo en fonction de la date et du robot

    Args:
        choice (_str_): Choix du robot
    """
    global API, choix_MRP_robot
    choix_MRP_robot = choice
    if verifie_format_date(str(Entry_p.get())) == False:
        messagebox.showinfo("Date error", "Veiller remplir date avec une date de type : YYYY-MM-DD")
        return
    cam,cam_name_dub = [],[]
    date = Entry_p.get().lower()
    API = download(f"https://api.nasa.gov/mars-photos/api/v1/rovers/{choice}/photos?api_key={key_api}&earth_date={date}",os.path.join(script_dir, "assets/JSON_DOWNLOAD_ACTUEL.json"),True)
    for i in range(len(API["photos"])):
        cam_name_dub.append(API["photos"][i]["camera"]["name"])
    cam_doublons = set(cam_name_dub)
    cam = list(cam_doublons)
    Camera_combobox.configure(values=cam)
    Camera_combobox.set("")

def MRP_Interfaces():
    """ Cette fonction definie la grand interface de MRP
    """
    if not code_deja_execute_MRP_Interface.get():
        code_deja_execute_MRP_Interface.set(True)
    
        global Title,FrameView,View,Paramètre,Entry_p,ReloadMRP,Rover_label,Camera_label,Camera_combobox,Rover_combobox,ID_combobox,ViewAPI
        ViewAPI = Frame(fenetre, bg=color[ch_col][0]) 
        ViewAPI.pack(anchor=CENTER, pady=20, expand=True)#fill=BOTH

        Title = CTkLabel(ViewAPI, text="Photo Rover Mars", font=("Nasalization Rg",30, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
        Title.pack(anchor='center', padx=40)

        FrameView = Frame(ViewAPI,bg=color[ch_col][0]) 
        FrameView.pack(anchor=CENTER)

        View = Canvas(FrameView, width=640, height=360 ,bg=color[ch_col][0],borderwidth=0, highlightthickness=0)
        View.grid(column = 0,row=0, padx=30, pady=40)
                
        Paramètre = Frame(FrameView,width=460, height=360, bg=color[ch_col][0])
        Paramètre.grid(column=1,row=0, padx=30)

        Rover_label = CTkLabel(Paramètre, text="Rover : ", font=("Nasalization Rg",13, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
        Rover_label.grid(column=0,row=0,pady=5)
                
        Rover_combobox = CTkComboBox(Paramètre, values=["Curiosity", "Opportunity","Spirit"],font=("Nasalization Rg",13, 'bold'), command=rover_combobox)
        Rover_combobox.grid(column=1,row=0)
                
        Camera_label = CTkLabel(Paramètre, text="Camera : ", font=("Nasalization Rg",13, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
        Camera_label.grid(column=0,row=1,pady=5)
                
        Camera_combobox = CTkComboBox(Paramètre, values=[], font=("Nasalization Rg",13, 'bold'), command=cam_id)
        Camera_combobox.set("")
        Camera_combobox.grid(column=1,row=1)
                
        ID_Label = CTkLabel(Paramètre, text="Photo ID : ", font=("Nasalization Rg",13, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
        ID_Label.grid(column=0,row=2, pady=5)
                
        ID_combobox = CTkComboBox(Paramètre, values=[], font=("Nasalization Rg",13, 'bold'), command=MRP_ID_image)
        ID_combobox.set("")
        ID_combobox.grid(column=1,row=2)
                
        Entry_p = CTkEntry(Paramètre, placeholder_text="Date : YYYY-MM-DD", fg_color="#00205B",text_color="white", corner_radius=5)
        Entry_p.grid(column=0,row=3)

        ReloadMRP = CTkButton(Paramètre, text="Recharger", fg_color="gray", hover_color="#9f9f9f", text_color="white", corner_radius=5, font=("Nasalization Rg",15))
        ReloadMRP.bind("<Button-1>", lambda event: (rover_combobox(choix_MRP_robot)))
        ReloadMRP.grid(column=1,row=3,padx=10, pady=5)
        
def MRP_Interfaces_low():
    """ Cette fonction definie la petit interface de MRP
    """
    global Title,FrameView,View,Paramètre,Entry_p,ReloadMRP,Rover_label,Camera_label,Camera_combobox,Rover_combobox,ID_combobox,ViewAPI    
    ViewAPI = CTkScrollableFrame(fenetre, fg_color=color[ch_col][0]) 
    ViewAPI.pack(fill=BOTH, anchor=CENTER, pady=20, expand=True)
    
    Title = CTkLabel(ViewAPI, text="Photo Rover Mars", font=("Nasalization Rg",30, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
    Title.pack(anchor='center', padx=40)

    FrameView = Frame(ViewAPI,bg=color[ch_col][0]) 
    FrameView.pack(anchor=CENTER)

    View = Canvas(FrameView, width=640, height=360 ,bg=color[ch_col][0],borderwidth=0, highlightthickness=0)
    View.grid(column = 0,row=0, padx=30, pady=40)
                
    Paramètre = Frame(FrameView,width=460, height=360, bg=color[ch_col][0])
    Paramètre.grid(column=0,row=1)

    Rover_label = CTkLabel(Paramètre, text="Rover : ", font=("Nasalization Rg",13, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
    Rover_label.grid(column=0,row=0,pady=5)
                
    Rover_combobox = CTkComboBox(Paramètre, values=["Curiosity", "Opportunity","Spirit"],font=("Nasalization Rg",13, 'bold'), command=rover_combobox)
    Rover_combobox.grid(column=1,row=0)
                
    Camera_label = CTkLabel(Paramètre, text="Camera : ", font=("Nasalization Rg",13, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
    Camera_label.grid(column=0,row=1,pady=5)
                
    Camera_combobox = CTkComboBox(Paramètre, values=[], font=("Nasalization Rg",13, 'bold'), command=cam_id)
    Camera_combobox.set("")
    Camera_combobox.grid(column=1,row=1)
                
    ID_Label = CTkLabel(Paramètre, text="Photo ID : ", font=("Nasalization Rg",13, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
    ID_Label.grid(column=0,row=2, pady=5)
                
    ID_combobox = CTkComboBox(Paramètre, values=[], font=("Nasalization Rg",13, 'bold'), command=MRP_ID_image)
    ID_combobox.set("")
    ID_combobox.grid(column=1,row=2)
                
    Entry_p = CTkEntry(Paramètre, placeholder_text="Date : YYYY-MM-DD", fg_color="#00205B",text_color="white", corner_radius=5)
    Entry_p.grid(column=0,row=3)

    ReloadMRP = CTkButton(Paramètre, text="Recharger", fg_color="gray", hover_color="#9f9f9f", text_color="white", corner_radius=5, font=("Nasalization Rg",15))
    ReloadMRP.bind("<Button-1>", lambda event: (rover_combobox(choix_MRP_robot)))
    ReloadMRP.grid(column=1,row=3,padx=10, pady=5)

def cam_id(choice):
    """ Cette fonction permet d'afichier les id des photo du robot en fonction de la camera

    Args:
        choice (_str_): Choix de la caméra
    """
    if verifie_format_date(str(Entry_p.get())) == False:
        messagebox.showinfo("Date error", "Veiller remplir date avec une date de type : YYYY-MM-DD")
        return
    global ID_combobox
    id_list_str = []
    for i in range(len(API["photos"])):
        if API["photos"][i]["camera"]["name"] == str(choice): id_list_str.append(str(API["photos"][i]["id"]))
    ID_combobox.configure(values= id_list_str)
    ID_combobox.set("")
    
    return

def MRP_ID_image(choice, dl=None, api=None):
    """ Cette fonction affiche l'image choisi de MRP 

    Args:
        choice (_str_): chois de l'image
        dl (_type not define_, optional): permet de savoir si il faut télécharger l'image. Defaults to None.
        api (_dict_, optional): fichier d'information en cour. Defaults to None.
    """
    global View,Rover_combobox,photo,Title,Paramètre,API,choice_public_mrp
    if (verifie_format_date(str(Entry_p.get())) == False) and (dl is None): messagebox.showinfo("Date error", "Veiller remplir date avec une date de type : YYYY-MM-DD"); return
    if choice is None: choice = choice_public_mrp
    else: choice_public_mrp = choice
    if api is not None: API = api
    for i in range(len(API["photos"])):
        if str(API["photos"][i]["id"]) == choice:
            if dl is None: download(API["photos"][i]["img_src"], os.path.join(script_dir, "assets/MRP/MRP_image.jpg"),False)
            View.destroy()
            image = Image.open(os.path.join(script_dir, "assets/MRP/MRP_image.jpg"))
            image.resize((640, 360))
            image.thumbnail((640,360))
            x,y = (640-image.size[0])/2, (360-image.size[1])/2
            photo = ImageTk.PhotoImage(image)
            View = Canvas(FrameView, width=640, height=360, bg=color[ch_col][0],borderwidth=0, highlightthickness=0)
            View.grid(column = 0,row=0, padx=60, pady=40)
            View.create_image(x,y, anchor='nw', image=photo)
      
def MRP_fonc():
    """ Cette fonction initial est la fonction initial de MRP elle génère la première image
    """
    global View,Rover_combobox,photo,Title,Paramètre,choice_public_mrp
    window_width = fenetre.winfo_width()
    if window_width < 1220: MRP_Interfaces_low(); inf.set(True)
    else: MRP_Interfaces()
    API = download(f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?api_key={key_api}&earth_date=2020-12-22",os.path.join(script_dir, "assets/JSON_DOWNLOAD_ACTUEL.json"),True)
    for i in range(len(API["photos"])):
        if str(API["photos"][i]["id"]) == str(784801):
            choice_public_mrp = str(784801)
            download(API["photos"][i]["img_src"], os.path.join(script_dir, "assets/MRP/MRP_image.jpg"),False)
            image = Image.open(os.path.join(script_dir, "assets/MRP/MRP_image.jpg"))
            image.resize((640, 360))
            image.thumbnail((640,360))
            x,y = (640-image.size[0])/2, (360-image.size[1])/2
            photo = ImageTk.PhotoImage(image)
            View.create_image(x,y, anchor='nw', image=photo)
            return
#Fin MRP fonc

#debut EPIC Fonc
def EPIC_date_lim_fonc():
    """ Cette fonction permet de doner les date limite de EPIC
    """
    if not code_deja_execute_EPIC_date_lim.get():
        global EPIC_date_lim
        code_deja_execute_EPIC_date_lim.set(True)
        EPIC_date_lim_ALL = download(f"https://epic.gsfc.nasa.gov/api/natural/available", os.path.join(script_dir, "assets/JSON_DOWNLOAD_ACTUEL.json"), True)
        EPIC_date_lim = [str(EPIC_date_lim_ALL[0]), str(EPIC_date_lim_ALL[-1])]

def EPIC_reload():
    """ Cette fonction permet de recharger APOD avec la date 
    """
    global API
    if verifie_format_date(str(Entry_p.get())) == False: messagebox.showinfo("Date error", "Veiller remplir date avec une date de type : YYYY-MM-DD"); return
    if not (EPIC_date_lim[0] <= str(Entry_p.get()) <= EPIC_date_lim[1]): messagebox.showinfo("Date error", f"date must between {EPIC_date_lim[0]} and {EPIC_date_lim[1]}"); return
    API = download(f"https://epic.gsfc.nasa.gov/api/natural/date/{Entry_p.get()}", os.path.join(script_dir, "assets/JSON_DOWNLOAD_ACTUEL.json"), True)
    id_list_str = []
    for i in range(len(API)):
        str_date = datetime.strptime(str(API[i]["identifier"]), "%Y%m%d%H%M%S").strftime("%Y %m %d / %Hh %Mm %Ss")
        id_list_str.append(f"{i+1}: {str_date}")
    ID_combobox.configure(values= id_list_str)
    ID_combobox.set("")

def EPIC_Interfaces():
    """ Cette fonction definie la grand interface de EPIC
    """
    if not code_deja_execute_EPIC_Interface.get():
        code_deja_execute_EPIC_Interface.set(True)
        
        global Title,FrameView,View,Paramètre,Entry_p,ReloadEPIC,ID_combobox,ViewAPI
        ViewAPI = Frame(fenetre, bg=color[ch_col][0]) 
        ViewAPI.pack(anchor=CENTER, pady=20, expand=True)#fill=BOTH

        Title = CTkLabel(ViewAPI, text="Earth Polychromatic Imaging Camera", font=("Nasalization Rg",30, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
        Title.pack(anchor='center', padx=40)

        FrameView = Frame(ViewAPI,bg=color[ch_col][0]) 
        FrameView.pack(anchor=CENTER)

        View = Canvas(FrameView, width=360, height=360 ,bg=color[ch_col][0],borderwidth=0, highlightthickness=0)
        View.grid(column = 0,row=0, padx=30, pady=40)
                
        Paramètre = Frame(FrameView,width=460, height=360, bg=color[ch_col][0])
        Paramètre.grid(column=1,row=0, padx=30)
                
        ID_Label = CTkLabel(Paramètre, text="Photo ID : ", font=("Nasalization Rg",13, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
        ID_Label.grid(column=0,row=0, pady=5)
                
        ID_combobox = CTkComboBox(Paramètre, values=[],width=265, font=("Nasalization Rg",13, 'bold'), command=EPIC_ID_image)
        ID_combobox.set("")
        ID_combobox.grid(column=1,row=0)
                
        Entry_p = CTkEntry(Paramètre, placeholder_text="Date : YYYY-MM-DD", fg_color="#00205B",text_color="white", corner_radius=5)
        Entry_p.grid(column=0,row=1)

        ReloadEPIC = CTkButton(Paramètre, text="Recharger", fg_color="gray", hover_color="#9f9f9f", text_color="white", corner_radius=5, font=("Nasalization Rg",15), command=EPIC_reload)
        ReloadEPIC.grid(column=1,row=1,padx=10, pady=5)
        return

def EPIC_Interfaces_low():
    """ Cette fonction definie la petit interface de EPIC
    """
    if not code_deja_execute_EPIC_Interface.get():
        code_deja_execute_EPIC_Interface.set(True)
        
        global Title,FrameView,View,Paramètre,Entry_p,ReloadEPIC,ID_combobox,ViewAPI
        ViewAPI = CTkScrollableFrame(fenetre, fg_color=color[ch_col][0]) 
        ViewAPI.pack(fill=BOTH, anchor=CENTER, pady=20, expand=True)

        Title = CTkLabel(ViewAPI, text="Earth Polychromatic Imaging Camera", font=("Nasalization Rg",30, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
        Title.pack(anchor='center', padx=20)

        FrameView = Frame(ViewAPI,bg=color[ch_col][0]) 
        FrameView.pack(anchor=CENTER)

        View = Canvas(FrameView, width=360, height=360 ,bg=color[ch_col][0],borderwidth=0, highlightthickness=0)
        View.grid(column = 0,row=0, padx=30, pady=20)
                
        Paramètre = Frame(FrameView,width=460, height=360, bg=color[ch_col][0])
        Paramètre.grid(column=0,row=1)
                
        ID_Label = CTkLabel(Paramètre, text="Photo ID : ", font=("Nasalization Rg",13, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
        ID_Label.grid(column=0,row=0, pady=5)
                
        ID_combobox = CTkComboBox(Paramètre, values=[],width=265, font=("Nasalization Rg",13, 'bold'), command=EPIC_ID_image)
        ID_combobox.set("")
        ID_combobox.grid(column=1,row=0)
                
        Entry_p = CTkEntry(Paramètre, placeholder_text="Date : YYYY-MM-DD", fg_color="#00205B",text_color="white", corner_radius=5)
        Entry_p.grid(column=0,row=1)

        ReloadEPIC = CTkButton(Paramètre, text="Recharger", fg_color="gray", hover_color="#9f9f9f", text_color="white", corner_radius=5, font=("Nasalization Rg",15), command=EPIC_reload)
        ReloadEPIC.grid(column=1,row=1,padx=10, pady=5)

def EPIC_ID_image(choice, dl=None, api=None):
    """ Cette fonction permet d'afficher limage de EPIC

    Args:
        choice (_str_): Choi de l'image
        dl (_type not define_, optional): permet de savoir si il faut télécharger l'image. Defaults to None.
        api (_lidt_, optional): fichier d'information en cour. Defaults to None.
    """
    global choice_public_epic, API
    if choice is None:
        choice = choice_public_epic
        if choice_public_epic is None: annee, mois, jour, heures, minutes, secondes = re.search(r"(\d{4}) (\d{2}) (\d{2}) / (\d{2})h (\d{2})m (\d{2})s", "1: 2023 05 05 / 18h 59m 58s").groups()
        else: choice = str(choice); annee, mois, jour, heures, minutes, secondes = re.search(r"(\d{4}) (\d{2}) (\d{2}) / (\d{2})h (\d{2})m (\d{2})s", choice).groups()
        choice_simple = f"{annee}{mois}{jour}{heures}{minutes}{secondes}"
    else:
        choice_public_epic = choice
        annee, mois, jour, heures, minutes, secondes = re.search(r"(\d{4}) (\d{2}) (\d{2}) / (\d{2})h (\d{2})m (\d{2})s", choice).groups()
        choice_simple = f"{annee}{mois}{jour}{heures}{minutes}{secondes}"
    if api is not None: API = api
    for i in range(len(API)):
        if API[i]["image"] == f"epic_1b_{choice_simple}":
            global View,photo,FrameView,labelText
            if dl is None: download(f"https://epic.gsfc.nasa.gov/archive/natural/{annee}/{mois}/{jour}/png/epic_1b_{choice_simple}.png", os.path.join(script_dir, "assets/EPIC/EPIC_image.jpg"), False)
            View.destroy()
            image = Image.open(os.path.join(script_dir, "assets/EPIC/EPIC_image.jpg"))
            image.thumbnail((360,360))
            x,y = (360-image.size[0])/2, (360-image.size[1])/2
            photo = ImageTk.PhotoImage(image)
            View = Canvas(FrameView, width=360, height=360, bg=color[ch_col][0],borderwidth=0, highlightthickness=0)
            window_width = fenetre.winfo_width()
            if window_width < 945:
                View.grid(column = 0,row=1, padx=30, pady=20)
            else:
                View.grid(column = 0,row=0, padx=30, pady=40)
            View.grid(column = 0,row=0, padx=60, pady=40)
            View.create_image(x,y, anchor='nw', image=photo)
            return

def EPIC_fonc():
    """ Cette fonction est la fonction inicial de EPIC elle génère la première image
    """
    global API, View,photo,FrameView,labelText
    window_width = fenetre.winfo_width()
    if window_width < 945: EPIC_Interfaces_low(); inf.set(True)
    else: EPIC_Interfaces()
    EPIC_date_lim_fonc()
    API = download(f"https://epic.gsfc.nasa.gov/api/natural/date/2023-05-05", os.path.join(script_dir, "assets/JSON_DOWNLOAD_ACTUEL.json"), True)
    annee, mois, jour, heures, minutes, secondes = re.search(r"(\d{4}) (\d{2}) (\d{2}) / (\d{2})h (\d{2})m (\d{2})s", "1: 2023 05 05 / 18h 59m 58s").groups()
    choice_simple = f"{annee}{mois}{jour}{heures}{minutes}{secondes}"
    for i in range(len(API)):
        if API[i]["image"] == f"epic_1b_{choice_simple}":
            global View,photo,FrameView,labelText
            download(f"https://epic.gsfc.nasa.gov/archive/natural/{annee}/{mois}/{jour}/png/epic_1b_{choice_simple}.png", os.path.join(script_dir, "assets/EPIC/EPIC_image.jpg"), False)
            View.destroy()
            image = Image.open(os.path.join(script_dir, "assets/EPIC/EPIC_image.jpg"))
            image.thumbnail((360,360))
            x,y = (360-image.size[0])/2, (360-image.size[1])/2
            photo = ImageTk.PhotoImage(image)
            View = Canvas(FrameView, width=360, height=360, bg=color[ch_col][0],borderwidth=0, highlightthickness=0)
            window_width = fenetre.winfo_width()
            if window_width < 945: View.grid(column = 0,row=1, padx=30, pady=20)
            else: View.grid(column = 0,row=0, padx=30, pady=40)
            View.grid(column = 0,row=0, padx=60, pady=40)
            View.create_image(x,y, anchor='nw', image=photo)
            return
#Fin EPIC Fonc

#fonc suprime aléméent
def name_api_curent_execute(name):
    """ Permet de maitre dans une variable le nom de l'API qui vient d'ètre executer

    Args:
        name (_str_): nom de l'api
    """
    global name_current_api
    name_current_api = name

def destroy_element(name=None):
    """ Fonction qui permet de détruire les élément d'une interface définie.

    Args:
        name (_str_, optional): nom de linterface a détruire. Defaults to None.
    """
    if name is None: return
    if name == "APOD":
        widgets = fenetre.winfo_children()
        if os.path.exists(os.path.join(script_dir, "assets/APOD/audio_temp.wav")):
            pygame.mixer.music.stop()
            pygame.mixer.quit() 
            os.remove(os.path.join(script_dir, "assets/APOD/audio_temp.wav"))
        for widget in widgets:
            if isinstance(widget, CTkFrame): widget.destroy()
        for inter in [Title,FrameView,View,FrameText,Paramètre,Entry_p,ReloadAPOD,labelText,ViewAPI]: inter.destroy()
        code_deja_execute_APOD_Interface.set(False)
    if name == "MRP":
        widgets = fenetre.winfo_children()
        for widget in widgets: 
            if isinstance(widget, CTkFrame): widget.destroy()
        for inter in [Title,FrameView,View,Paramètre,Entry_p,ReloadMRP,Rover_label,Camera_label,Camera_combobox,Rover_combobox,ViewAPI]: inter.destroy()
        code_deja_execute_MRP_Interface.set(False)
    if name == "EPIC":
        widgets = fenetre.winfo_children()
        for widget in widgets:
            if isinstance(widget, CTkFrame): widget.destroy()
        for inter in [Title,FrameView,View,Paramètre,Entry_p,ReloadEPIC,ViewAPI]: inter.destroy()
        code_deja_execute_EPIC_Interface.set(False)
    
    
    if name == "PARA":
        widgets = fenetre.winfo_children()
        for widget in widgets:
            if isinstance(widget, CTkFrame): widget.destroy()
        for inter in [ViewPAR,Title,FrameView,API_KEY_text,API_KEY_entry,Applay,Retour]: inter.destroy()
    return



    """
    ViewPAR = Frame(fenetre, bg=color[ch_col][0]) 
    ViewPAR.pack(anchor=CENTER, pady=20, expand=True)

    Title = CTkLabel(ViewPAR, text="Paramètre", font=("Nasalization Rg",30, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
    Title.pack(anchor='center', padx=40)

    FrameView = Frame(ViewPAR,bg=color[ch_col][0]) 
    FrameView.pack(anchor=CENTER,pady=(70,0))
    
    API_KEY_text = CTkLabel(FrameView, text="API_KEY : ", font=("Nasalization Rg",13, 'bold'), fg_color="#00205B",text_color="white", corner_radius=5)
    API_KEY_text.grid(column=0,row=0,pady=5)
    
    API_KEY_entry= CTkEntry(FrameView, placeholder_text="Your Nasa API Keys", fg_color="#00205B",text_color="white", corner_radius=5)
    API_KEY_entry.grid(column=1,row=0, padx=5)
    """


#fonc gengement de tail écran
def uptade_interface(boll, name, r_interfaces, interface):
    """Cette fonction remplace une interface grad par une petit et invercement.

    Args:
        boll (_Bool_): si on depasse la limite pour le changemen d'écran
        name (_str_): nom de l'api a changer
        r_interfaces (_BooleanVar_): reègle linterface grand pour l'exécuuter
        interface (_fonction_): fonction de l'interface a mètre en place
    """
    if boll == True:
        if not inf.get():
            inf.set(True)
            destroy_element(name)
            interface() 
            with open(os.path.join(script_dir, "assets/JSON_DOWNLOAD_ACTUEL.json"), 'r') as json_file: API = json.load(json_file)
            if name == "APOD": 
                Title.configure(text=API["title"])
                if API["media_type"] ==  "video": APOD_video(API,0)
                else: APOD_picture(API,0)
            if name == "MRP": MRP_ID_image(None, 0, API) 
            if name == "EPIC": EPIC_ID_image(None, dl=0, api=API)      
    else:
        if inf.get():
            inf.set(False)
            destroy_element(name)
            r_interfaces.set(False)
            interface() 
            with open(os.path.join(script_dir, "assets/JSON_DOWNLOAD_ACTUEL.json"), 'r') as json_file: API = json.load(json_file)
            if name == "APOD":
                Title.configure(text=API["title"])
                if API["media_type"] ==  "video": APOD_video(API,0)
                else: APOD_picture(API,0)
            if name == "MRP": MRP_ID_image(None, 0, API) 
            if name == "EPIC": EPIC_ID_image(None, dl=0, api=API)

def check_window_size(event=None):
    """Cette fonction sert a rediriger les configuration des fenetre
    Args: event (_<class 'tkinter.Event'>_): event tkinter """
    window_width = fenetre.winfo_width()
    if name_current_api == "APOD":
        if window_width < 1220: uptade_interface(True, "APOD", code_deja_execute_APOD_Interface, APOD_Interfaces_low)
        else: uptade_interface(False, "APOD", code_deja_execute_APOD_Interface, APOD_Interfaces)
    if name_current_api == "EPIC":
        if window_width < 945: uptade_interface(True, "EPIC", code_deja_execute_EPIC_Interface, EPIC_Interfaces_low)              
        else: uptade_interface(False, "EPIC", code_deja_execute_EPIC_Interface, EPIC_Interfaces)              
    if name_current_api == "MRP":
        if window_width < 1060: uptade_interface(True, "MRP", code_deja_execute_MRP_Interface, MRP_Interfaces_low)            
        else: uptade_interface(False, "MRP", code_deja_execute_MRP_Interface, MRP_Interfaces)

# ----- MAIN -----#
set_appearance_mode("dark")
global ch_col, color, script_dir
fenetre = CTk()
fenetre.configure(fg_color="#FFFFFF")
fenetre.geometry("1280x720")
fenetre.title("API NASA Request")
fenetre.configure(bg="white")
fenetre.minsize(840, 720)
font_path = "nasalization.ttf"
fenetre.bind("<Configure>", check_window_size)

# Variable de contrôle pour suivre si le code a été exécuté
code_deja_execute = BooleanVar()
code_deja_execute.set(False)

code_deja_execute_proxy = BooleanVar()
code_deja_execute_proxy.set(False)

code_deja_execute_APOD_Interface = BooleanVar()
code_deja_execute_APOD_Interface.set(False)

code_deja_execute_MRP_Interface = BooleanVar()
code_deja_execute_MRP_Interface.set(False)

code_deja_execute_EPIC_Interface = BooleanVar()
code_deja_execute_EPIC_Interface.set(False)

code_deja_execute_EPIC_date_lim = BooleanVar()
code_deja_execute_EPIC_date_lim.set(False)

inf_int = BooleanVar()
inf_int.set(False)

inf = BooleanVar()
inf.set(False)

variable_init()
proxy_init()
main_widget()

if key_api == "":
    messagebox.showinfo("Error Clé API", "Entré votre clé d'API dans les Parametre")
fenetre.mainloop() 