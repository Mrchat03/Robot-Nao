"""
Application pour piloter un Robot Nao
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class BeepBop(toga.App):

    def startup(self):
        #-----------Création des boîtes--------------
        
        #Les sous-boîtes
        rgbChoix_box = toga.Box(style=Pack(direction=ROW))
        rgbRouge_box = toga.Box(style=Pack(direction=ROW))
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
        btn_box = toga.Box(style=Pack(direction=COLUMN), children=[btnPos_box, btnTourne_box, btnAnim_box, btnMsg_box])
        joystick_box = toga.Box(style=Pack(direction=COLUMN), children=[joystickAvance_box, joystickCote_box, joystickRecul_box])
        main_box = toga.Box(style=Pack(direction=ROW, padding=5), children=[rgb_box])
   
        #-----Création des boutons-----
        btn_rgbOreilles = toga.Button(
            'O',
            style=Pack(padding=5)
        )
        
        btn_rgbYeux = toga.Button(
            'Y',
            style=Pack(padding=5)
        )
   
        #-----Création des labels------
        lbl_rouge = toga.Label('R', style=Pack(padding=(5)))
        lbl_vert = toga.Label('G', style=Pack(padding=(5)))
        lbl_bleu = toga.Label('B', style=Pack(padding=(5)))

        rgbChoix_box.add(btn_rgbOreilles)
        rgbChoix_box.add(btn_rgbYeux)
        rgbRouge_box.add(lbl_rouge)
        rgbVert_box.add(lbl_vert)
        rgbBleu_box.add(lbl_bleu)
   
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return BeepBop()
