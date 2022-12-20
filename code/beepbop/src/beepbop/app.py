"""
@file   app.py
@author Nathanaël Amaridon, Jacob Turcotte, Eric Gingras
@date   6 decembre 2022
@brief  Application pour piloter un Robot Nao
@version 1.0

Environnement: Visual Studio Code
"""
import toga
import sys
import time
import socket
from toga.colors import RED, GREEN, BLUE, rgb
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class BeepBop(toga.App):
    
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def startup(self):
        self.address = ("", 4210)

        #-----------Création des boîtes--------------
        
        #Les sous-boîtes
        
        btnPos_box = toga.Box(style=Pack(direction=ROW))
        btnTourne_box = toga.Box(style=Pack(direction=ROW))
        btnAnim_box = toga.Box(style=Pack(direction=ROW))
        btnMsg_box = toga.Box(style=Pack(direction=ROW))
        
        joystickAvance_box = toga.Box(style=Pack(direction=ROW))
        joystickCote_box = toga.Box(style=Pack(direction=ROW))
        joystickRecul_box = toga.Box(style=Pack(direction=ROW))
        
        connexion_box = toga.Box(style=Pack(direction=ROW))
        
        #Les boîtes principales
        btn_box = toga.Box(style=Pack(direction=COLUMN, padding_right=20, padding_left=50), children=[btnPos_box, btnTourne_box, btnAnim_box, btnMsg_box])
        joystick_box = toga.Box(style=Pack(direction=COLUMN), children=[joystickAvance_box, joystickCote_box, joystickRecul_box])
        main_box = toga.Box(style=Pack(direction=ROW, padding=5), children=[btn_box, joystick_box, connexion_box])
        
        
        #-----Création des boutons-----
        btn_debout = toga.Button(text="🧍", style=Pack(font_size=25, width=50), on_press=self.debout_action)
        btn_assis = toga.Button(text="🧎", style=Pack(font_size=25, width=50), on_press=self.assis_action)
        btn_tourneGauche = toga.Button(text="↶", style=Pack(font_size=25, width=50), on_press=self.tourneGauche_action)
        btn_tourneDroite = toga.Button(text="↷", style=Pack(font_size=25, width=50), on_press=self.tourneDroite_action)
        btn_tourne180 = toga.Button(text="⟲", style=Pack(font_size=25, width=50), on_press=self.tourne180_action)
        btn_animation = toga.Button(text="🕺", style=Pack(font_size=25, width=50), on_press=self.animation_action)
        btn_envoie = toga.Button(text="💬", style=Pack(font_size=15, width=50), on_press=self.parle_action)
        btn_avance = toga.Button(text="🡹", style=Pack(font_size=25, width=50, padding_top=20, padding_left=50), on_press=self.avance_action)
        btn_gauche = toga.Button(text="🡸", style=Pack(font_size=25, width=50, padding_right=50), on_press=self.gauche_action)
        btn_droite = toga.Button(text="🡺", style=Pack(font_size=25, width=50), on_press=self.droite_action)
        btn_recul = toga.Button(text="🡻", style=Pack(font_size=25, width=50, padding_left = 50), on_press=self.recul_action)
        btn_connexion = toga.Button(text="📶", style=Pack(font_size=25, width=50), on_press=self.connect_action)
        btn_stop = toga.Button(text="❌", style=Pack(font_size=25, width=50), on_press=self.animation_stop)
        
        
        #-----Création du textbox-----
        self.txt_message = toga.TextInput(style=Pack(padding_top=12))
        
        #Ajout des items aux boîtes btn-----
        btnPos_box.add(btn_debout)
        btnPos_box.add(btn_assis)
        btnTourne_box.add(btn_tourneGauche)
        btnTourne_box.add(btn_tourneDroite)
        btnAnim_box.add(btn_tourne180)
        btnAnim_box.add(btn_animation)
        btnAnim_box.add(btn_stop)
        btnMsg_box.add(self.txt_message)
        btnMsg_box.add(btn_envoie)
    
        #-----Ajout des items aux boîtes joystick-----
        joystickAvance_box.add(btn_avance)
        joystickCote_box.add(btn_gauche)
        joystickCote_box.add(btn_droite)
        joystickRecul_box.add(btn_recul)
        
        connexion_box.add(btn_connexion)
        
        
        
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
    
        
    def connect_action(self, widget):
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.address = ("0", 0)
        self.configUDPESP()
        
        widget.enabled = False

        
    #Place le robot en position debout
    def debout_action(self, widget):
        msg = """{"animation":{"topic":"zbos/motion/animation/run","payload":{"type":"Posture","animationId":"Stand"}}}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("debout  //  ", msg)
    
    # Place le robot en position assis
    def assis_action(self, widget):
        msg = """{"animation":{"topic":"zbos/motion/animation/run","payload":{"type":"Posture","animationId":"Crouch"}}}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("assis  //  ", msg)

    #Tourne le robot vers la gauche de 15 degrés
    def tourneGauche_action(self, widget):
        msg = """{"movement":{"topic":"zbos/motion/control/movement","payload":{"angle":{"radian":2.2448158576504826,"degree":128.61847442741285},"force":100}}}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("tourneGauche  //  ", msg)
        msg = """{"movement":{"topic":"zbos/motion/control/movement", "payload":{"yaw": 0,"pitch": 0,"angle": {"degree": 0},"force": 0,"distance": 0,"relative_rotation": 0}}}"""
        time.sleep(3.5)
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("stop   //", msg)
      
    #Tourne le robot vers la droite de 15 degrés  
    def tourneDroite_action(self, widget):
        msg = """{"movement":{"topic":"zbos/motion/control/movement","payload":{"angle":{"radian":0.6939980604270402,"degree":39.763159852734475},"force":100}}}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("tourneDroite  //  ", msg)
        msg = """{"movement":{"topic":"zbos/motion/control/movement", "payload":{"yaw": 0,"pitch": 0,"angle": {"degree": 0},"force": 0,"distance": 0,"relative_rotation": 0}}}"""
        time.sleep(3)
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("stop   //", msg)
        
    #Tourne le robot 180 degrés
    def tourne180_action(self, widget):
        msg = """{"movement":{"topic":"zbos/motion/control/movement","payload":{"angle":{"radian":0.6939980604270402,"degree":39.763159852734475},"force":100}}}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("tourne180  //  ", msg)
        msg = """{"movement":{"topic":"zbos/motion/control/movement", "payload":{"yaw": 0,"pitch": 0,"angle": {"degree": 0},"force": 0,"distance": 0,"relative_rotation": 0}}}"""
        time.sleep(5)
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("stop   //", msg)
        
    #Fonction pour faire danser le robot
    def animation_action(self, widget):
        msg = """{"dance":{"topic":"zbos/motion/dance/start", "payload":"chickendance/chickendance"}}""" 
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("animation  //  ", msg)
        
    def animation_stop(self, widget):
        msg = """{"dance":{"topic":"zbos/motion/dance/stop"}}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("stop  //  ", msg)
    
    #Avance le robot de quelques pas
    def avance_action(self, widget):
        msg = """{"movement":{"topic":"zbos/motion/control/movement","payload":{"yaw": 0,"pitch": 0,"angle": {"degree": 90},"force": 50,"distance": 0.1,"relative_rotation": 0}}}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("avance  //  ", msg)
        msg = """{"movement":{"topic":"zbos/motion/control/movement","payload":{"yaw": 0,"pitch": 0,"angle": {"degree": 0},"force": 0,"distance": 0,"relative_rotation": 0}}}"""
        time.sleep(5)
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("stop   //  ", msg)
        
    #Le robot marche vers la droite pour quelques pas
    def droite_action(self, widget):
        msg = """{"movement":{"topic":"zbos/motion/control/movement","payload":{"yaw": 0,"pitch": 0,"angle": {"degree": 0},"force": 50,"distance": 0.1,"relative_rotation": 0}}}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("droite  //  ", msg)
        msg = """{"movement":{"topic":"zbos/motion/control/movement","payload":{"yaw": 0,"pitch": 0,"angle": {"degree": 0},"force": 0,"distance": 0,"relative_rotation": 0}}}"""
        time.sleep(5)
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("stop   //", msg)
    
    #Le robot marche vers la gauche pour quelques pas
    def gauche_action(self, widget):
        msg = """{"movement":{"topic":"zbos/motion/control/movement", "payload":{"yaw": 0,"pitch": 0,"angle": {"degree": 180},"force": 50,"distance": 0.1,"relative_rotation": 0}}}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("gauche  //  ", msg)
        msg = """{"movement":{"topic":"zbos/motion/control/movement", "payload":{"yaw": 0,"pitch": 0,"angle": {"degree": 0},"force": 0,"distance": 0,"relative_rotation": 0}}}"""
        time.sleep(5)
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("stop   //", msg)
        
    #Le robot recule de quelques pas
    def recul_action(self, widget):
        msg = """{"movement":{"topic":"zbos/motion/control/movement", "payload":{"yaw": 0,"pitch": 0,"angle": {"degree": 270},"force": 50,"distance": 0.1,"relative_rotation": 0}}}"""
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("recul  //  ", msg)
        msg = """{"movement":{"topic":"zbos/motion/control/movement", "payload":{"yaw": 0,"pitch": 0,"angle": {"degree": 0},"force": 0,"distance": 0,"relative_rotation": 0}}}"""
        time.sleep(5)
        self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        print("stop   //", msg)
    
    #Le robot dit ce qui a été saisi dans le textbox
    def parle_action(self, widget):
        #Je vais faire un pas", "language": "fr-FR", "volume": 50}
        if "mqtt set " in self.txt_message.value:
            index = self.txt_message.value.find('set') + 4
            mqtt = self.txt_message.value[index:len(self.txt_message.value)]
            msg = """{"commande":{"mqtt":{"set":""" +'"' + mqtt + """"}}}"""
            self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        elif "wifi set" in self.txt_message.value:
            index = self.txt_message.value.find('set') + 4
            ssidPwd = self.txt_message.value[index:len(self.txt_message.value)]
            infoWifi = ssidPwd.split(' ')
            msg = """{"commande":{"wifi":{"set":{"ssid":""" + '"' + infoWifi[0] + """", "pwd":""" + '"' + infoWifi[1] + """"}}}}"""
            self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        elif "ip set " in self.txt_message.value:
            index = self.txt_message.value.find('set') + 4
            ip = self.txt_message.value[index:len(self.txt_message.value)]
            self.address = (ip, 4210) #erreur bizarre ici acause du if, Nenregistra pas bien dans la variable address, voir ligne 221 pour la solution
            msg = self.address
        else:
            msg = """{"dialog":{"topic":"zbos/dialog/set","payload":{"message":""" + '"' + self.txt_message.value + """", "language": "fr-FR", "volume": 50}}}"""
            self.UDPClientSocket.sendto(msg.encode('utf-8'), self.address)
        
        
        print("parle  //", msg)
        
    def configUDPESP(self):
        hostname = socket.gethostname()
        ip = get_private_ip()
        if "ip set " in self.txt_message.value:
            index = self.txt_message.value.find('set') + 4
            ip_esp = self.txt_message.value[index:len(self.txt_message.value)]
            self.address = (ip_esp, 4210)
            print(self.address)
        print(ip)
        #Initiation de UDP
        print(self.address)
        self.UDPClientSocket.bind((ip, 4210))
        print(self.UDPClientSocket)
        msg = "Configuration terminée."
        self.UDPClientSocket.sendto(msg.encode(), self.address)
        

        #self.x.abort()


def get_private_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as st:
        st.settimeout(0.0)
        try:
            st.connect(('8.8.8.8', 80))
            ip = st.getsockname()[0]
        except socket.error:
            ip = '127.0.0.1'
    return ip



def main():

    
    return BeepBop()    
 #10.240.3.139
