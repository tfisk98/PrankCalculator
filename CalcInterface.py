from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout, QStackedWidget, QToolButton, QMenu
import sys
import os 
from Calculator import Calculator
import pygame 
import numpy as np




class CalcInterface(QWidget):
    def __init__(self, calculator=None):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setGeometry(525, 300, 400, 300)
        self.setFixedHeight(400)
        self.setFixedWidth(300)

        self.calculator = calculator if calculator is not None else Calculator()
        self.soundspath = ['/fart.wav','/cow.wav','/duck.wav','/boat.wav']
        self.sound = self.soundspath[0]
        self.sound_prob = 1.

        self.stacked_widget = QStackedWidget(self)
        self.display = self.create_display()
        self.create_pages()
        self.optionBtn = self.create_options(self.stacked_widget)
        self.apply_styles()

        self.button_index = 0  # Start with the first set of buttons

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(12)
        main_layout.addWidget(self.display, alignment=QtCore.Qt.AlignHCenter)
        main_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(self.optionBtn, alignment=QtCore.Qt.AlignRight)
        self.stacked_widget.setCurrentIndex(0)

        pygame.mixer.init()


    def create_display(self):
        display = QLineEdit()
        display.setReadOnly(True)
        display.setAlignment(QtCore.Qt.AlignHCenter)
        display.setFixedSize(250, 50)
        self.display_style(display)
        return display

    def create_pages(self):
        self.ui1 = self.create_page(0)
        self.ui2 = self.create_page(1)

        self.stacked_widget.addWidget(self.ui1)
        self.stacked_widget.addWidget(self.ui2)

    def create_buttons(self, grid_layout, ui_index):
        if ui_index == 0:
            buttons = [
                'C', 'del', '%', 'CI',
                '7', '8', '9', '/',
                '4', '5', '6', '*',
                '1', '2', '3', '-',
                '.', '0', '=', '+'
            ]
        else:
            buttons = [
                'C', '(', ')', 'CI',
                'x^2', 'x^y', 'x^(-1)', '/',
                'cos', 'sin', 'tan', '*',
                'exp', 'log_y', 'ln', '-',
                '.', 'sqrt', '=', '+'
            ]
        row = 1
        col = 0
        for button in buttons:
            btn = QPushButton(button)
            btn.clicked.connect(self.on_button_click)
            grid_layout.addWidget(btn, row, col)
            self.button_style(btn)

            if button in self.calculator.operators + ['.','x^2','x^y','x^(-1)','log_y'] :
                self.operations_style(btn)

            if button in ['C', 'del', 'CI'] : 
                self.red_txt(btn)
            
            if button == '=':
                self.equal_style(btn)

            col += 1
            if col > 3:
                col = 0
                row += 1

    def create_options(self, parent_widget):
        optionBtn = QToolButton(parent_widget)
        optionBtn.setText('Options')
        optionBtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        menu = QMenu(self)
        menu.setMinimumWidth(180)
        menu.setStyleSheet("""
            QMenu {
                background-color: #f0ffff;
                color: #000000;
                border: 1px solid #87ceeb;
            }
            QMenu::item {
                padding: 8px 14px;
            }
            QMenu::item:selected {
                background-color: #87ceeb;
            }
        """)
        sound_options = {
            'bateau / boat': '/boat.wav',
            'canard / duck': '/duck.wav',
            'pet / fart': '/fart.wav',
            'vache / cow': '/cow.wav',
        }
        for label, sound in sound_options.items():
            action = menu.addAction(label)
            action.triggered.connect(
                lambda checked=False, selected_sound=sound: self.change_sound(selected_sound)
            )
        optionBtn.setMenu(menu)
        optionBtn.setPopupMode(QToolButton.InstantPopup)
        optionBtn.clicked.connect(optionBtn.showMenu)
        self.options_style(optionBtn)

        return optionBtn
    
    def create_page(self,ui_index):
        page = QWidget()

        main_layout = QVBoxLayout(page)
        main_layout.setAlignment(QtCore.Qt.AlignHCenter)
        main_layout.setSpacing(12)

        button_panel = QWidget()
        grid_layout = QGridLayout(button_panel)
        grid_layout.setSpacing(8)


        self.create_buttons(grid_layout, ui_index)
        main_layout.addWidget(button_panel, alignment= QtCore.Qt.AlignHCenter)

        page.button_panel = button_panel
        return page

    def apply_styles(self):

        self.setStyleSheet(""" 
        background-color: #262626;
        color: #FFFFFF;
        font-family: Titillium;
        font-size: 18px;
        """)
        pass

    def display_style(self, display):

        display.setStyleSheet("""
            border-radius: 6px;
            background-color : #f0ffff;
            color: #000000; 
            """)
        pass 

    def button_style(self, button):
        button.setStyleSheet(""" 
            height : 30px;
            width : 50px;
            border-radius : 6px;
            background-color : #c1cdcd;
            color: #000000;
            """)
        pass 

    def equal_style(self,button):
        button.setStyleSheet(""" 
            height : 30px;
            width : 50px;
            border-radius : 6px;
            background-color : #ff8c00;
            color: #000000;
        """)
        pass

    def operations_style(self,button):
            button.setStyleSheet(""" 
                height : 30px;
                width : 50px;
                border-radius : 6px;
                background-color : #87ceeb;
                color: #000000;
            """)
            pass

    def red_txt(self,button):
        button.setStyleSheet(""" 
                    height : 30px;
                    width : 50px;
                    border-radius : 6px;
                    background-color : #c1cdcd;
                    color: #dc143c;
                    """)
        pass

    def options_style(self,option):
        option.setStyleSheet(""" 
                    height : 30px;
                    width : 100px;
                    border-radius : 6px;
                    background-color : #c1cdcd;
                    color: #000000;
                    """)
        pass 
        

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()
        display = self.display

        self.play_sound(self.sound_prob)

        if text == '=':
            try:
                result = self.calculator.screen_to_operation(display.text())
                display.setText(str(result))
            except Exception:
                display.setText("Error")
        elif text == 'C':
            display.clear()
        elif text == 'CI':
            self.button_index = 1 - self.button_index  # Update the button index
            self.change_ui(self.button_index)  # Change the UI to the new button set
        elif text == 'del': 
            display.setText(display.text()[:-1])
        elif text == 'x^2':
            display.setText(display.text() + '^2')
        elif text == 'x^y':
            display.setText(display.text() + '^')
        elif text == 'x^(-1)':
            display.setText(display.text() + '^(-1)')
        elif text == 'sqrt': 
            display.setText( display.text() + 'sqrt(')
        elif text == 'log_y':
            display.setText(display.text() + 'log_(')
        elif text == 'ln':
            display.setText(display.text() + 'ln(')
        elif text == 'exp':
            display.setText(display.text() + 'exp(')
        elif text == 'cos':
            display.setText(display.text() + 'cos(')
        elif text == 'sin':
            display.setText(display.text() + 'sin(')
        elif text == 'tan':
            display.setText(display.text() + 'tan(')
        else:
            display.setText(display.text() + text)

    def show(self):
        super().show()

    def closeEvent(self, event):
        event.accept()

    def change_ui(self, ui_index):
        self.stacked_widget.setCurrentIndex(ui_index)

    def change_buttons(self, button_index):
        current_page = self.stacked_widget.currentWidget()
        grid_layout = current_page.button_panel.layout()
        for i in range(grid_layout.count()):
            widget = grid_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                widget.setVisible(False)

        for i in range(grid_layout.count()):
            widget = grid_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                if button_index == 0 and widget.text() in ['C', '(', ')', 'CI', '7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '0', '.', '=', '+']:
                    widget.setVisible(True)
                elif button_index == 1 and widget.text() in ['C', '(', ')', 'CI', 'x^2', 'x^y', 'x^(-1)', '/', 'cos', 'sin', 'tan', '*', 'exp', 'log_y', 'ln', '-', 'sqrt', '.', '=', '+']:
                    widget.setVisible(True)

    def play_sound(self, sound_prob):  
        if np.random.rand() < sound_prob:  # 10% chance to play the sound
            path = os.getcwd() + "/Sounds"
            effect = pygame.mixer.Sound(path + "/" + self.sound)
            effect.play()
            pygame.time.wait(500)

    def change_sound(self, sound):
        self.sound = sound