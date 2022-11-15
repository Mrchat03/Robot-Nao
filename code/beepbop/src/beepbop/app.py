"""
Application pour piloter un Robot Nao
"""
import toga
import socket
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class BeepBop(toga.App):
    #UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    def startup(self):
        #-----------Création des boîtes--------------
        main_box = toga.Box(style=Pack(direction=ROW))
        #Trois boîtes principales
        rgb_box = toga.Box(style=Pack(direction=COLUMN))
        btn_box = toga.Box(style=Pack(direction=COLUMN))
        joystick_box = toga.Box(style=Pack(direction=COLUMN))
        #Les sous-boîtes
        
        rgbChoix_box = toga.Box(style=Pack(direction=ROW))
        rgbRouge_box = toga.Box(style=Pack(direction=ROW))
        rgbGreen_box = toga.Box(style=Pack(direction=ROW))
        rgbBlue_box = toga.Box(style=Pack(direction=ROW))
        
        btnPos_box = toga.Box(style=Pack(direction=ROW))
        btnTourne_box = toga.Box(style=Pack(direction=ROW))
        btnAnim_box = toga.Box(style=Pack(direction=ROW))
        btnMsg_box = toga.Box(style=Pack(direction=ROW))
        
        joystickAvance_box = toga.Box(style=Pack(direction=ROW))
        joystickCote_box = toga.Box(style=Pack(direction=ROW))
        joystickRecul_box = toga.Box(style=Pack(direction=ROW))
        
        #Création des labels
        rouge_label = toga.Label('R')
        vert_label = toga.Label('G')
        bleu_label = toga.Label('B')

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


       
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
