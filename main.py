from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout


class RecipappApp(App):

    def build (self):
        return FloatLayout()



def callback(instance):
    print ("Why are you geh")

if __name__ == '__main__':

    RecipappApp().run()





