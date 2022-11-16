"""
Application pour piloter un Robot Nao
"""
import toga
import socket
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, JUSTIFY


class BeepBop(toga.App):
    #UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    def startup(self):
        oreille_icon = "icon/oreille.png"
        
        
        
        #-----------Création des boîtes--------------
        
        #Les sous-boîtes
        rgbChoix_box = toga.Box(style=Pack(direction=ROW))
        rgbRouge_box = toga.Box(style=Pack(direction=ROW, padding_top = 10))
        rgbVert_box = toga.Box(style=Pack(direction=ROW))
        rgbBleu_box = toga.Box(style=Pack(direction=ROW))
        
        btnPos_box = toga.Box(style=Pack(direction=ROW))
        btnTourne_box = toga.Box(style=Pack(direction=ROW))
        btnAnim_box = toga.Box(style=Pack(direction=ROW))
        btnMsg_box = toga.Box(style=Pack(direction=ROW))
        
        joystickAvance_box = toga.Box(style=Pack(direction=ROW))
        joystickCote_box = toga.Box(style=Pack(direction=ROW))
        joystickRecul_box = toga.Box(style=Pack(direction=ROW))
        
        rgb_box = toga.Box(style=Pack(direction=COLUMN), children=[rgbChoix_box, rgbRouge_box, rgbVert_box, rgbBleu_box])
        btn_box = toga.Box(style=Pack(direction=COLUMN, padding_left=20), children=[btnPos_box, btnTourne_box, btnAnim_box, btnMsg_box])
        joystick_box = toga.Box(style=Pack(direction=COLUMN), children=[joystickAvance_box, joystickCote_box, joystickRecul_box])
        main_box = toga.Box(style=Pack(direction=ROW, padding=5), children=[rgb_box, btn_box])
        
        
        #-----Création des boutons-----
        btn_oreille = toga.Button(text = "👀", style=Pack(font_size=25, width=50, padding_right=10))
        btn_yeux = toga.Button(text="👂", style=Pack(font_size=25, width=50))
        btn_debout = toga.Button(text="🧍", style=Pack(font_size=25, width=50))
        btn_assis = toga.Button(text="🧎", style=Pack(font_size=25, width=50))
        btn_tourneGauche = toga.Button(text="↶", style=Pack(font_size=25, width=50))
        btn_tourneDroite = toga.Button(text="↷", style=Pack(font_size=25, width=50))
        btn_tourne180 = toga.Button(text="⟲", style=Pack(font_size=25, width=50))
        btn_animation = toga.Button(text="🕺", style=Pack(font_size=25, width=50))
        btn_envoie = toga.Button(text="⏩", style=Pack(font_size=15, width=50))
        
        #-----Création des sliders-----
        slider_rouge = toga.Slider()
        slider_vert = toga.Slider()
        slider_bleu = toga.Slider()
        
        #-----Ajout du textbox-----
        txt_message = toga.TextInput(style=Pack(padding_top=12))
   
        #-----Création des labels------
        lbl_rouge = toga.Label('R')
        lbl_vert = toga.Label('G')
        lbl_bleu = toga.Label('B')
        

        #-----Ajout des items aux boîtes rgb-----
        rgbChoix_box.add(btn_oreille)
        rgbChoix_box.add(btn_yeux)
        rgbRouge_box.add(lbl_rouge)
        rgbRouge_box.add(slider_rouge)
        rgbVert_box.add(lbl_vert)
        rgbVert_box.add(slider_vert)
        rgbBleu_box.add(lbl_bleu)
        rgbBleu_box.add(slider_bleu)
        

        
        #Ajout des items aux boîtes btn-----
        btnPos_box.add(btn_debout)
        btnPos_box.add(btn_assis)
        btnTourne_box.add(btn_tourneGauche)
        btnTourne_box.add(btn_tourneDroite)
        btnAnim_box.add(btn_tourne180)
        btnAnim_box.add(btn_animation)
        btnMsg_box.add(txt_message)
        btnMsg_box.add(btn_envoie)
        
        
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

def oreille_action(widget):
    print("oreille")

       
    ### Fonction pour configurer l'UDP et envoyer des messages###   
def initUDP(ip = "192.168.4.1", port= 4210):
    serverAddressPort = (ip, port)
    return(serverAddressPort)
    


def main():
    #Initiation de UDP
    serverAddressPort = initUDP()
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    #fin de config et exemple d'envoie de message par UDP
    msg = "TATA."
    UDPClientSocket.sendto(msg.encode(), serverAddressPort)
    return BeepBop()
