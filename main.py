from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.uix.floatlayout import FloatLayout
import random
import copy


class MastermindGame(FloatLayout):

    def __init__(self,**kwargs):

        super(MastermindGame, self).__init__(**kwargs)

        for j in range(0,8):
            if j!=0:
                self.canvas.add(Rectangle(pos=(470,30+j*65),size=(45,45)))
            for i in range(0,4):
                self.canvas.add(Ellipse(pos= (200+i*65,30+j*65), size=(45, 45)))

        self.canvas.add(Rectangle(pos=(200, 83), size= (240,3)))

        self.marker = Rectangle(pos=(200, 20), size=(45, 3))
        self.canvas.add(self.marker)

        self.canvas.add(Color(1, 0, 0))
        self.canvas.add(Ellipse(pos=(557, 35 + 0 * 50), size=(35, 35)))
        self.canvas.add(Color(1, 1, 0))
        self.canvas.add(Ellipse(pos=(557, 35 + 1 * 50), size=(35, 35)))
        self.canvas.add(Color(1, 0, 1))
        self.canvas.add(Ellipse(pos=(557, 35 + 2 * 50), size=(35, 35)))
        self.canvas.add(Color(0, 1, 0))
        self.canvas.add(Ellipse(pos=(557, 35 + 3 * 50), size=(35, 35)))
        self.canvas.add(Color(0, 0, 1))
        self.canvas.add(Ellipse(pos=(557, 35 + 4 * 50), size=(35, 35)))

        self.colors = ['R', 'Y', 'P', 'G', 'B']
        self.answer = [random.choice(self.colors), random.choice(self.colors), random.choice(self.colors), random.choice(self.colors)]
        print(self.answer)

        self.given_answer = {'200.0': [0, 0, 0], '265.0': [0, 0, 0], '330.0': [0, 0, 0], '395.0': [0, 0, 0]}


    def on_touch_down(self, touch):
        position = self.marker.pos
        rgb = []
        with self.canvas:
            if 557 < touch.x < 592 and 35 < touch.y < 70:
                Color(1, 0, 0)
                rgb = [1, 0, 0]
                Ellipse(pos=(position[0], 30), size=(45, 45))
            elif 557 < touch.x < 592 and 85 < touch.y < 120:
                Color(1, 1, 0)
                rgb = [1, 1, 0]
                Ellipse(pos=(position[0], 30), size=(45, 45))
            elif 557 < touch.x < 592 and 135 < touch.y < 170:
                Color(1, 0, 1)
                rgb = [1,0,1]
                Ellipse(pos=(position[0], 30), size=(45, 45))
            elif 557 < touch.x < 592 and 185 < touch.y < 220:
                Color(0, 1, 0)
                rgb = [0,1,0]
                Ellipse(pos=(position[0], 30), size=(45, 45))
            elif 557 < touch.x < 592 and 235 < touch.y < 270:
                Color(0, 0, 1)
                rgb = [0,0,1]
                Ellipse(pos=(position[0], 30), size=(45, 45))
        if len(rgb) > 0:
            self.given_answer[str(position[0])] = rgb


class MastermindApp(App):

    def move_left(self, obj):
        position = self.game.marker.pos
        if position[0] == 200 :
            self.game.marker.pos = (395, position[1])
        else :
            self.game.marker.pos = (position[0] - 65, position[1])
        self.game.canvas.ask_update()


    def move_right(self, obj):
        position = self.game.marker.pos
        if position[0] == 395 :
            self.game.marker.pos = (200, position[1])
        else :
            self.game.marker.pos = (position[0] + 65, position[1])
        self.game.canvas.ask_update()


    def letter_to_rgb(self, letter):
        if letter == 'R':
            return [1, 0, 0]
        elif letter == 'Y':
            return [1, 1, 0]
        elif letter == 'P':
            return [1, 0, 1]
        elif letter == 'G':
            return [0, 1, 0]
        elif letter == 'B':
            return [0, 0, 1]


    def traduction_answer(self):
        answer_in_letters = self.game.answer
        answer_in_rgb = []
        for element in answer_in_letters:
            answer_in_rgb.append(self.letter_to_rgb(element))

        answer = {'200.0': answer_in_rgb[0], '265.0': answer_in_rgb[1], '330.0': answer_in_rgb[2],
                  '395.0': answer_in_rgb[3]}
        return answer


    def calculate_scores(self, answer, given_answer):
        well_placed = 0
        wrong_placed = 0
        keys = copy.copy(list(answer.keys()))
        for key in keys:
            if answer[key] == given_answer[key]:
                well_placed += 1
                del answer[key]
                del given_answer[key]

        for value in given_answer.values():
            keys = list(answer.keys())
            values = list(answer.values())
            found = 0
            i = 0
            while i < len(keys) and found < 1:
                if value == values[i]:
                    wrong_placed += 1
                    del answer[keys[i]]
                    found = 1
                i += 1
        return well_placed, wrong_placed


    def winning_scenario(self):
        popup = Popup(title='Congratulations !',
                      content=Label(text='You found the Mastermind code !'),
                      size_hint=(None, None), size=(400, 200))
        popup.open()


    def loosing_scenario(self):
        popup = Popup(title='Wrong answer...',
                      content=Label(text="Sorry, the developper hasn't coded this part yet...\n\nYou definitely haven't win though."),
                      size_hint=(None, None), size=(400, 200))
        popup.open()


    def submit_answer(self, obj):
        answer = self.traduction_answer()
        given_answer = self.game.given_answer
        well_placed, wrong_placed = self.calculate_scores(answer, given_answer)

        if well_placed == 4:
            self.winning_scenario()
        else:
            self.loosing_scenario()


    def build(self):
        parent = Widget()
        self.game = MastermindGame()
        parent.add_widget(self.game)

        leftbtn = Button(text="<==", size=(50, 30), pos=(620, 30))
        leftbtn.bind(on_release = self.move_left)
        parent.add_widget(leftbtn)

        rightbtn = Button(text="==>", size=(50, 30), pos=(680, 30))
        rightbtn.bind(on_release = self.move_right)
        parent.add_widget(rightbtn)

        submitbtn = Button(text="Submit", size=(110, 30), pos=(620, 70))
        submitbtn.bind(on_release = self.submit_answer)
        parent.add_widget(submitbtn)

        return parent


if __name__ == '__main__':
    MastermindApp().run()
