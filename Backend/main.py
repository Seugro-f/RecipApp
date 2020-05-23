from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import boto3
from boto3.dynamodb.conditions import Key

# Get the dynamodb resource from AWS server
dynamodb = boto3.resource('dynamodb')

# load dynamodb wiskUsers table from AWS
table = dynamodb.Table('wiskUsers')


# Function to check username and password of user with AWS wiskUsers table
def usercheck(userID, userPass):
    # Generate variables for while/for loops to initialize
    userMatch = []
    userExist = False

    # Scan the AWS dynamodb "wiskUsers" table for existing user
    userInfo = table.query(
        KeyConditionExpression=Key('userID').eq(userID)
    )

    for i in userInfo['Items']:
        userMatch.append(i['userPass'])

    # Check if the username/password combination exists, otherwise returns logic value used in kv file
    if not userMatch or userMatch[0] != userPass:
        print("The username/password is wrong")
    else:
        userExist = True

    # Returns logic value used for if statement in kv file for NewUserScreern on button release action
    return userExist


# Function to add new user to AWS wiskUsers table
def newuser(userID, userPass):

    # Generate variables for while/for loops to initialize
    userMatch = []
    newUserComp = False

    # Scan the AWS dynamodb "wiskUsers" table for existing user
    userInfo = table.query(
        KeyConditionExpression=Key('userID').eq(userID)
    )

    # Append existing usernames into userMatch
    for i in userInfo['Items']:
        userMatch.append(i['userID'])

    # If statement so that new user is created if username doesn't already exist
    if userMatch:
        newUserComp = True
        userExistText = True

    else:
        table.put_item(
            Item={
                'userID': userID,
                'userPass': userPass
            }
        )
    # Returns logic value used for if statement in kv file for NewUserScreern on button release action
    return newUserComp


class MainScreen(Screen):
    pass


class NewUserScreen(Screen):
    # Define new user function for button to be used in NewUserScreen window
    def btnNewUser(self):
        userName = self.newUser.text
        passWord = self.newPass.text
        newUserComp = newuser(userName, passWord)

        # Returns logic value used for if statement of button defined in kv file
        return newUserComp


class LoginScreen(Screen):

    # define user check function for button to be used in LoginScreen Window
    def btnSubmit(self):
        userName = self.userN.text
        passWord = self.passW.text
        userExist = usercheck(userName, passWord)

        # Returns logic value used for if statement of button defined in kv file
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
