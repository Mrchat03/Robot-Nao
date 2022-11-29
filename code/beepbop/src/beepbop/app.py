"""
Application pour piloter un Robot Nao
"""
import toga
import sys
import time
import socket
from toga.colors import RED, GREEN, BLUE, rgb
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class BeepBop(toga.App):
    #UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    address = ""


    def startup(self):
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.address = ("0", 0)
        self.configUDPESP()
        self.msgDebout = """zbos/motion/animation/run#{"type":"Posture","animationId":"Stand"}"""
        self.msgStop = """zbox/motion/animaton/stop"""
        
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
        
        #Les boîtes principales
        rgb_box = toga.Box(style=Pack(direction=COLUMN), children=[rgbChoix_box, rgbRouge_box, rgbVert_box, rgbBleu_box])
        btn_box = toga.Box(style=Pack(direction=COLUMN, padding_left=20), children=[btnPos_box, btnTourne_box, btnAnim_box, btnMsg_box])
        joystick_box = toga.Box(style=Pack(direction=COLUMN), children=[joystickAvance_box, joystickCote_box, joystickRecul_box])
        main_box = toga.Box(style=Pack(direction=ROW, padding=5), children=[rgb_box, btn_box, joystick_box])
        
        
        #-----Création des boutons-----
        btn_oreille = toga.Button(text = "👀", style=Pack(font_size=25, width=50, padding_right=10),on_press=self.yeux_action)
        btn_yeux = toga.Button(text="👂", style=Pack(font_size=25, width=50), on_press=self.oreille_action)
        btn_debout = toga.Button(text="🧍", style=Pack(font_size=25, width=50), on_press=self.debout_action)
        btn_assis = toga.Button(text="🧎", style=Pack(font_size=25, width=50), on_press=self.assis_action)
        btn_tourneGauche = toga.Button(text="↶", style=Pack(font_size=25, width=50), on_press=self.tourneGauche_action)
        btn_tourneDroite = toga.Button(text="↷", style=Pack(font_size=25, width=50), on_press=self.tourneDroite_action)
        btn_tourne180 = toga.Button(text="⟲", style=Pack(font_size=25, width=50), on_press=self.tourne180_action)
        btn_animation = toga.Button(text="🕺", style=Pack(font_size=25, width=50), on_press=self.animation_action)
        btn_envoie = toga.Button(text="⏩", style=Pack(font_size=15, width=50), on_press=self.parle_action)
        btn_avance = toga.Button(text="🡹", style=Pack(font_size=25, width=50, padding_top=20, padding_left=50), on_press=self.avance_action)
        btn_gauche = toga.Button(text="🡸", style=Pack(font_size=25, width=50, padding_right=50), on_press=self.gauche_action)
        btn_droite = toga.Button(text="🡺", style=Pack(font_size=25, width=50), on_press=self.droite_action)
        btn_recul = toga.Button(text="🡻", style=Pack(font_size=25, width=50, padding_left = 50), on_press=self.recul_action)
        
        #-----Création des sliders-----
        self.slider_rouge = toga.Slider(range=(0,255), on_change=self.majRouge)
        self.slider_vert = toga.Slider(range=(0,255), on_change=self.majVert)
        self.slider_bleu = toga.Slider(range=(0,255), on_change=self.majBleu)
        
        #-----Ajout du textbox-----
        self.txt_message = toga.TextInput(style=Pack(padding_top=12))
   
        #-----Création des labels------
        lbl_rouge = toga.Label('R', style=Pack(color=RED))
        lbl_vert = toga.Label('G', style=Pack(color=GREEN))
        lbl_bleu = toga.Label('B', style=Pack(color=BLUE))
        self.lbl_rougeValeur = toga.Label(int(self.slider_rouge.value))
        self.lbl_vertValeur = toga.Label(int(self.slider_vert.value))
        self.lbl_bleuValeur = toga.Label(int(self.slider_bleu.value))

        #-----Ajout des items aux boîtes rgb-----
        rgbChoix_box.add(btn_oreille)
        rgbChoix_box.add(btn_yeux)
        rgbRouge_box.add(lbl_rouge)
        rgbRouge_box.add(self.slider_rouge)
        rgbRouge_box.add(self.lbl_rougeValeur)
        rgbVert_box.add(lbl_vert)
        rgbVert_box.add(self.slider_vert)
        rgbVert_box.add(self.lbl_vertValeur)
        rgbBleu_box.add(lbl_bleu)
        rgbBleu_box.add(self.slider_bleu)
        rgbBleu_box.add(self.lbl_bleuValeur)
        
        #Ajout des items aux boîtes btn-----
        btnPos_box.add(btn_debout)
        btnPos_box.add(btn_assis)
        btnTourne_box.add(btn_tourneGauche)
        btnTourne_box.add(btn_tourneDroite)
        btnAnim_box.add(btn_tourne180)
        btnAnim_box.add(btn_animation)
        btnMsg_box.add(self.txt_message)
        btnMsg_box.add(btn_envoie)
    
        #-----Ajout des items aux boîtes joystick-----
        joystickAvance_box.add(btn_avance)
        joystickCote_box.add(btn_gauche)
        joystickCote_box.add(btn_droite)
        joystickRecul_box.add(btn_recul)
        
        
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
    
    def majRouge(self, widget):
        self.lbl_rougeValeur.text=int(self.slider_rouge.value)
        
    def majVert(self, widget):
        self.lbl_vertValeur.text=int(self.slider_vert.value)
        
    def majBleu(self, widget):
        self.lbl_bleuValeur.text=int(self.slider_bleu.value)

    def oreille_action(self, widget):
        #zbos/leds/chestlight/set#
        #{
        #"part": <partie du corps>, ("CHEST" * "MOUTH" * "EYES" * "HEAD" * "SPEECH")
        #"color": <valeur hexa de couleur rgb>, (exemple: "#ff0000")
        #"breath": <valeur bool>, (true, false)
        #"breathDuration": <valeur int>, (exemple: 1500)
        #"duration": <valeur int> (exemple: 1500)
        #}
        msg = """zbos/leds/chestlight/set#{"part": "HEAD", "color": "#"""
        rgb = 0
        rouge = int(self.slider_rouge.value)
        rouge = rouge * 65536
        rgb = rgb + rouge
        vert = int(self.slider_vert.value)
        vert = vert * 256
        rgb = rgb + vert
        bleu = int(self.slider_bleu.value)
        rgb = rgb + bleu
        hex_rgb = format(rgb, 'x')
        msg = msg + hex_rgb + """", "breathDuration": 1500, "duration": -1}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("oreille  //  ", msg)

    def yeux_action(self, widget):
        #zbos/leds/chestlight/set#
        #{
        #"part": <partie du corps>, ("CHEST" * "MOUTH" * "EYES" * "HEAD" * "SPEECH")
        #"color": <valeur hexa de couleur rgb>, (exemple: "#ff0000")
        #"breath": <valeur bool>, (true, false)
        #"breathDuration": <valeur int>, (exemple: 1500)
        #"duration": <valeur int> (exemple: 1500)
        #}
        msg = """zbos/leds/chestlight/set#{"part": "EYES", "color": "#"""
        rgb = 0
        rouge = int(self.slider_rouge.value)
        rouge = rouge * 65536
        rgb = rgb + rouge
        vert = int(self.slider_vert.value)
        vert = vert * 256
        rgb = rgb + vert
        bleu = int(self.slider_bleu.value)
        rgb = rgb + bleu
        hex_rgb = format(rgb, 'x')
        msg = msg + hex_rgb + """", "breathDuration": 1500, "duration": -1}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("yeux  //  ", msg)  
        
    def debout_action(self, widget):
        self.UDPClientSocket.sendto(self.msgDebout.encode('utf-8'), self.address)
        print("debout  //  ", self.msgDebout)
    
    def assis_action(self, widget):
        msg = self.msgDebout + "!" + """zbos/motion/animation/run#{"type":"Posture","animationId":"Crouch"}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("assis  //  ", msg)
        
    def tourneGauche_action(self, widget):
        msg = self.msgDebout + "!" + """zbos/motion/control/movement#{"yaw": 0,"pitch": 0,"angle": {"degree": 180},"force": 50,"distance": 0.1,"relative_rotation": 0}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("tourneGauche  //  ", msg)
        
    def tourneDroite_action(self, widget):
        msg = self.msgDebout + "!" + """zbos/motion/control/movement#{"yaw": 0,"pitch": 0,"angle": {"degree": 180},"force": 50,"distance": 0.1,"relative_rotation": 0}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("tourneDroite  //  ", msg)
        
    def tourne180_action(self, widget):
        msg = self.msgDebout + "!" + """zbos/motion/control/movement#{"yaw": 0,"pitch": 0,"angle": {"degree": 0},"force": 50,"distance": 0,"relative_rotation": 180}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("tourne180  //  ", msg)
        
    def animation_action(self, widget):
        msg = self.msgDebout + "!" + """zbos/motion/animation/run#{"type":"Posture","animationId":"taichisit/taichisit"}"""
        print("animation  //  ", msg)
    
    def avance_action(self, widget):
        msg = """zbos/motion/control/movement#{"yaw": 0,"pitch": 0,"angle": {"degree": 90},"force": 50,"distance": 0.1,"relative_rotation": 0}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("avance  //  ", msg)
        msg = """zbos/motion/control/movement#{"yaw": 0,"pitch": 0,"angle": {"degree": 90},"force": 0,"distance": 0,"relative_rotation": 0}"""
        time.sleep(5)
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("stop   //  ", msg)
        
    def droite_action(self, widget):
        msg = """zbos/motion/control/movement#{"yaw": 0,"pitch": 0,"angle": {"degree": 0},"force": 50,"distance": 0.1,"relative_rotation": 0}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("droite  //  ", msg)
        msg = """zbos/motion/control/movement#{"yaw": 0,"pitch": 0,"angle": {"degree": 0},"force": 0,"distance": 0,"relative_rotation": 0}"""
        time.sleep(5)
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("stop   //", msg)
    
    def gauche_action(self, widget):
        msg = """zbos/motion/control/movement#{"yaw": 0,"pitch": 0,"angle": {"degree": 180},"force": 50,"distance": 0.1,"relative_rotation": 0}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("gauche  //  ", msg)
        msg = """zbos/motion/control/movement#{"yaw": 0,"pitch": 0,"angle": {"degree": 180},"force": 0,"distance": 0,"relative_rotation": 0}"""
        time.sleep(5)
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("stop   //", msg)
        
    def recul_action(self, widget):
        msg = """zbos/motion/control/movement#{"yaw": 0,"pitch": 0,"angle": {"degree": 270},"force": 50,"distance": 0.1,"relative_rotation": 0}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("recul  //  ", msg)
        msg = """zbos/motion/control/movement#{"yaw": 0,"pitch": 0,"angle": {"degree": 270},"force": 0,"distance": 0,"relative_rotation": 0}"""
        time.sleep(5)
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("stop   //", msg)
    
    def parle_action(self, widget):
        #Je vais faire un pas", "language": "fr-FR", "volume": 50}
        msg = """zbos/dialog/set#{"message": """ + '"'+ self.txt_message.value + """ ", "language": "fr-FR", "volume": 50}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("parle  //  ", msg)

    def configUDPESP(self):
        ip = ""
        if len(sys.argv) == 3:
        # Get "IP address of Server" and also the "port number" from
        #argument 1 and argument 2
            ip = sys.argv[1]
        recu = True
        print(ip)
        #Initiation de UDP
        self.UDPClientSocket.bind(initUDP(ip))

        while recu:
            #Attend de recevoir un message
            data, self.address = self.UDPClientSocket.recvfrom(4096)
            messageVerif = data.decode('utf-8')
            if (messageVerif == "allo le monde !"):
            #Confirmation que le message est recu)
                msg = "MAC recu" 
                self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
                recu = False
                #print(recu)

        #fin de config et exemple d'envoie de message par UDP       
        msg = "Configuration terminée."
        self.UDPClientSocket.sendto(msg.encode(), self.address)

def initUDP(ip = "192.168.4.1", port= 4210):
        serverAddressPort = (ip, port)
        return(serverAddressPort)
        ###Fonction connecte automatiquement au ESP de Nath


       
     


def main():

    
    return BeepBop()    
 
