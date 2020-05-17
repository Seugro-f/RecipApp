from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import boto3
from boto3.dynamodb.conditions import Key

# Get the dynamodb resource from AWS server
dynamodb = boto3.resource('dynamodb')

# load dynamodb wiskUsers table from AWS
table = dynamodb.Table('wiskUsers')


# Function to check username and password of user with AWS database
def usercheck(userID, userPass):
    userMatch = []
    userExist = False

    # Scan the AWS dynamodb "wiskUsers" table for existing user
    userInfo = table.query(
        KeyConditionExpression=Key('userID').eq(userID)
    )

    for i in userInfo['Items']:
        userMatch.append(i['userPass'])

    if not userMatch:
        print("The username doesn't exist")

    else:
        if userMatch[0] != userPass:
            print("Wrong Password")
        else:
            userExist = True

    return userExist


# Creating a new item in the AWS server for new user
def newuser(userID, userPass):
    table.put_item(
        Item={
            'userID': userID,
            'userPass': userPass
        }
    )


class MainScreen(Screen):
    pass


class NewUserScreen(Screen):
    def btnNewUser(self):
        userName = self.newUser.text
        passWord = self.newPass.text
        newuser(userName, passWord)


class LoginScreen(Screen):

    def btnSubmit(self):
        userName = self.userN.text
        passWord = self.passW.text
        userExist = usercheck(userName, passWord)

        return userExist


class RecipeScreen(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("recipapp.kv")


class RecipappApp(App):

    def build(self):
        return kv


if __name__ == '__main__':
    RecipappApp().run()
