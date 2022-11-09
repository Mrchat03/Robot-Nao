"""
Application pour piloter un Robot Nao
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class BeepBop(toga.App):

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


def main():
    return BeepBop()
