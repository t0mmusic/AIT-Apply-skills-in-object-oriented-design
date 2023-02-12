import login
import fish
import sys
import random
import PySimpleGUI as sg
import os.path
from os import path

# array of all PySimpleGui Themes for randomisation
themes = ['Black', 'BlueMono', 'BluePurple', 'BrightColors', 'BrownBlue',
			'Dark', 'Dark2', 'DarkAmber', 'DarkBlack', 'DarkBlack1', 'DarkBlue',
			'DarkBlue1', 'DarkBlue10', 'DarkBlue11', 'DarkBlue12', 'DarkBlue13',
			'DarkBlue14', 'DarkBlue15', 'DarkBlue16', 'DarkBlue17', 'DarkBlue2',
			'DarkBlue3', 'DarkBlue4', 'DarkBlue5', 'DarkBlue6', 'DarkBlue7',
			'DarkBlue8', 'DarkBlue9', 'DarkBrown', 'DarkBrown1', 'DarkBrown2',
			'DarkBrown3', 'DarkBrown4', 'DarkBrown5', 'DarkBrown6', 'DarkGreen',
			'DarkGreen1', 'DarkGreen2', 'DarkGreen3', 'DarkGreen4', 'DarkGreen5',
			'DarkGreen6', 'DarkGrey', 'DarkGrey1', 'DarkGrey2', 'DarkGrey3',
			'DarkGrey4', 'DarkGrey5', 'DarkGrey6', 'DarkGrey7', 'DarkPurple',
			'DarkPurple1', 'DarkPurple2', 'DarkPurple3', 'DarkPurple4', 'DarkPurple5',
			'DarkPurple6', 'DarkRed', 'DarkRed1', 'DarkRed2', 'DarkTanBlue', 'DarkTeal',
			'DarkTeal1', 'DarkTeal10', 'DarkTeal11', 'DarkTeal12', 'DarkTeal2', 'DarkTeal3',
			'DarkTeal4', 'DarkTeal5', 'DarkTeal6', 'DarkTeal7', 'DarkTeal8', 'DarkTeal9',
			'Default', 'Default1', 'DefaultNoMoreNagging', 'Green', 'GreenMono', 'GreenTan',
			'HotDogStand', 'Kayak', 'LightBlue', 'LightBlue1', 'LightBlue2', 'LightBlue3',
			'LightBlue4', 'LightBlue5', 'LightBlue6', 'LightBlue7', 'LightBrown',
			'LightBrown1', 'LightBrown10', 'LightBrown11', 'LightBrown12', 'LightBrown13',
			'LightBrown2', 'LightBrown3', 'LightBrown4', 'LightBrown5', 'LightBrown6',
			'LightBrown7', 'LightBrown8', 'LightBrown9', 'LightGray1', 'LightGreen',
			'LightGreen1', 'LightGreen10', 'LightGreen2', 'LightGreen3', 'LightGreen4',
			'LightGreen5', 'LightGreen6', 'LightGreen7', 'LightGreen8', 'LightGreen9',
			'LightGrey', 'LightGrey1', 'LightGrey2', 'LightGrey3', 'LightGrey4',
			'LightGrey5', 'LightGrey6', 'LightPurple', 'LightTeal', 'LightYellow',
			'Material1', 'Material2', 'NeutralBlue', 'Purple', 'Reddit', 'Reds',
			'SandyBeach', 'SystemDefault', 'SystemDefault1', 'SystemDefaultForReal',
			'Tan', 'TanBlue', 'TealMono', 'Topanga']

# Sets a random theme from the array
sg.theme(themes[random.randint(0, len(themes) - 1)])
# layout for the login selection screen
layoutLog = [
			[sg.Text("Username", size=(15, 1)), sg.Input(key='USER')],
			[sg.Text("Password", size=(15, 1)), sg.Input(key='PASS', password_char='*')]
		]
# layout for the signup selection screen
layoutSign = [
			[sg.Text("Username", size=(15, 1)), sg.Input(key='USER_LOG')],
			[sg.Text("Password", size=(15, 1)), sg.Input(key='PASS_ONE', password_char='*')],
			[sg.Text("Re-enter Password", size=(15, 1)), sg.Input(key='PASS_TWO', password_char='*')]
		]
# layout for the leaderboard display screen
layoutScore = []
# layout for the game
layoutGame = [
			[sg.Button('Cast a line!', key='THROW'),
			sg.Button('Keep', visible=False, key='KEEP'),
			sg.Button('Release', visible=False, key='RELEASE')],
			[sg.Text("Current Score: 0", key='CURR_SCORE')]
		]
layoutBucket = []
# universal layout to display all features of the gui
layout = [
			[sg.Button('Log In', key='LOGIN_MENU'),
			sg.Button('Sign Up', key='SIGNUP_MENU'),
			sg.Button('High Scores', key='SCORE'),
			sg.Button('Bucket', visible=False, key='BUCKET'),
			sg.Text(key='LOGNAME')],
			[sg.Text(key='INFO')],
			[sg.Column(layoutLog, key='COL1'),
			sg.Column(layoutSign, visible=False, key='COL2'),
			sg.Column(layoutScore, visible=False, key='COL3'),
			sg.Column(layoutGame, visible=False, key='COL4'),
			sg.Multiline(size=(30, 5), visible=False, key='CATCHLIST')],
			[sg.Button('Start Playing!', key='LOGIN'),
			sg.Button('Start Playing!', key='SIGNUP', visible=False)],
			[sg.Image(key='IMG', visible=False)],
			[sg.Button('Exit', key='EXIT')]
		]

# creates a window gui
# sg.theme_previewer()
window = sg.Window('Hello and thanks for all the fish', layout, size=(800, 600), finalize=True)

# if the username and password fields have been filled in, the username
# exists in the database and matches the input password, the user will
# successfully log in to the game and begin playing. Otherwise, an error
# message will be displayed
def	loginGame(values):
	if (values['USER'] == "" or values['PASS'] == ""):
		window['INFO'].update("All fields must be filled in.")
		return (False)
	if (login.Account.compareUsername(values['USER'])):
		currUser = login.UserPassword.login(values['USER'], values['PASS'])
		if (currUser != False):
			return (currUser)
		else:
			window['INFO'].update("incorrect password")
	else:
		window['INFO'].update("username could not be found!")
	return (False)

# If user has entered text into fields, username does not already exist and passwords match,
# they will successfully log in to the game and begin playing. Otherwise, an error message
# will be displayed.
def signUpGame(values):
	if (values['USER_LOG'] == "" or values['PASS_ONE'] == "" or values['PASS_TWO'] == ""):
		window['INFO'].update("All fields must be filled in.")
		return (False)
	if (login.Account.compareUsername(values['USER_LOG']) == False):
		password = login.UserPassword.setPassword(values['PASS_ONE'], values['PASS_TWO'])
		if (password != False):
			currUser = login.UserPassword.createAccount(values['USER_LOG'], password)
			return (currUser)
		else:
			window['INFO'].update("passwords do not match!")
	else:
		window['INFO'].update("Username is already in use!")
	return (False)

# updates the array of users in order of highest to lowest high score. Then places
# this information into a single string which is displayed on the screen.
def updateHighScores():
	scoreArray = login.Account.showLeaderboard()
	scoreString = "Top 10 Scores\n" + '\n'.join([str(x) for x in scoreArray])
	if (scoreString):
		window['INFO'].update(scoreString)
	else:
		window['INFO'].update("There are no high scores to display!")

# displays the login screen when the game is first loaded. User can choose to login,
# signup, or view a leaderboard of high scores.
def preGameMenu():
	# sets the currently visible column to the login screen
	currentColumn = window['COL1']
	window.bind("<Return>", 'LOGIN')
	while (True):
		event, values = window.read()
		# Exits cleanly if user closes window
		if (event == sg.WINDOW_CLOSED or event == 'EXIT'):
			window.close()
			break
		# Displays LeaderBoard
		if (event == 'SCORE'):
			window['INFO'].update("")
			window['LOGIN'].update(visible=False)
			window['SIGNUP'].update(visible=False)
			currentColumn.update(visible=False)
			window['COL3'].update(visible=True)
			currentColumn = window['COL3']
			updateHighScores()
		# Displays log in menu
		if (event == 'LOGIN_MENU'):
			window['INFO'].update("")
			window.bind("<Return>", 'LOGIN')
			window['LOGIN'].update(visible=True)
			window['SIGNUP'].update(visible=False)
			currentColumn.update(visible=False)
			window['COL1'].update(visible=True)
			currentColumn = window['COL1']
		# Displays Sign up menu
		if (event == 'SIGNUP_MENU'):
			window['INFO'].update("")
			window['LOGIN'].update(visible=False)
			window.bind("<Return>", 'SIGNUP')
			window['SIGNUP'].update(visible=True)
			currentColumn.update(visible=False)
			window['COL2'].update(visible=True)
			currentColumn = window['COL2']
		# Logs in user, or displays error
		if (event == 'LOGIN' or event == "_Enter"):
			ret = loginGame(values)
			if (ret != False):
				currentColumn.update(visible=False)
				return (ret)
		# Signs up user, or displays error
		if (event == 'SIGNUP'):
			ret = signUpGame(values)
			if (ret != False):
				currentColumn.update(visible=False)
				return (ret)
	window.close()
	sys.exit()

# updates the image to the appropriate matching fish. If there
# are more than 6 fish, others are given a placeholder image.
def updateImage(fish):
	if (path.exists('KGW.png') == False):
		return
	if (fish == "King George Whiting"):
		img = 'KGW.png'
	elif (fish == "Lost Bait"):
		img = 'bait.png'
	elif (fish == "Small Mulloway"):
		img = 'mulloway.png'
	elif (fish == "Snapper"):
		img = 'snapper.png'
	elif (fish == "Large Mullet"):
		img = 'mullet.png'
	elif (fish == "Seaweed Monster"):
		img = 'SeaweedMonster.png'
	else:
		img = 'fishing.png'
	window['IMG'].update(img, size=(700, 225), visible=True)


# Gameplay menu for the gui. User can cast a line, then choose to keep
# or release what they have caught.
def gamePlay(currUser):
	# initialises window for gameplay
	currUser.score = 0
	currentColumn = window['COL4']
	window['LOGIN'].update(visible=False)
	window['SIGNUP'].update(visible=False)
	window['LOGIN_MENU'].update(visible=False)
	window['SIGNUP_MENU'].update(visible=False)
	window['COL4'].update(visible=True)
	window['BUCKET'].update(visible=True)
	window['INFO'].update("")
	window['LOGNAME'].update(currUser.username)
	while (True):
		event, values = window.read()
		window.bind("<Return>", 'THROW')
		if (event == sg.WINDOW_CLOSED or event == 'EXIT'):
			break
		# User casts a line to catch a fish, caught fish is displayed
		if (event == 'THROW'):
			window.bind("<Return>", 'KEEP')
			window['KEEP'].update(visible=True)
			window['RELEASE'].update(visible=True)
			window['THROW'].update(visible=False)
			window['CATCHLIST'].update(visible=False)
			catch = fish.Fish.castLine()
			window['INFO'].update("You caught a " + catch.name + "!")
			updateImage(catch.name)
		# User keeps fish, score is updated with points_kept added
		if (event == 'KEEP'):
			currUser.score += int(catch.points_keep)
			window['CATCHLIST'].update(visible=False)
			window['CURR_SCORE'].update("Current Score: " + str(currUser.score))
			window['INFO'].update("You decided to keep your catch!")
			window['KEEP'].update(visible=False)
			window['RELEASE'].update(visible=False)
			window['THROW'].update(visible=True)
			if (window['CATCHLIST'].get() == ""):
				window['CATCHLIST'].update(catch.name)
			else:
				window['CATCHLIST'].update(window['CATCHLIST'].get() + "\n" + catch.name)
		# User releases fish, score is updated with points_release added
		if (event == 'RELEASE'):
			currUser.score += int(catch.points_release)
			window['CATCHLIST'].update(visible=False)
			window['CURR_SCORE'].update("Current Score: " + str(currUser.score))
			window['INFO'].update("You decided to release your catch!")
			window['KEEP'].update(visible=False)
			window['RELEASE'].update(visible=False)
			window['THROW'].update(visible=True)
		# if the highscore value is lower than the current score value, it is
		# updated to the current value
		if (currUser.score > currUser.highScore):
			currUser.highScore = currUser.score
		# displays the bucket of fish caught by the user
		if (event == 'BUCKET'):
			window['CATCHLIST'].update(visible=True)
			window['LOGIN_MENU'].update("Back to game", visible=True)
			window['LOGNAME'].update(visible=False)
			window['BUCKET'].update(visible=False)
			window['SCORE'].update(visible=False)
			window['IMG'].update(visible=False)
			window['INFO'].update("")
			currentColumn.update(visible=False)
		# Displays LeaderBoard
		if (event == 'SCORE'):
			window['SCORE'].update(visible=False)
			window['BUCKET'].update(visible=False)
			window['CATCHLIST'].update(visible=False)
			window['LOGNAME'].update(visible=False)
			window['IMG'].update(visible=False)
			window['LOGIN_MENU'].update("Back to game", visible=True)
			window['INFO'].update("")
			currentColumn.update(visible=False)
			window['COL3'].update(visible=True)
			currentColumn = window['COL3']
			updateHighScores()
		# returns to game from leaderboard
		if (event == 'LOGIN_MENU'):
			window['INFO'].update("")
			window['SCORE'].update(visible=True)
			window['LOGNAME'].update(visible=True)
			window['BUCKET'].update(visible=True)
			window['LOGIN_MENU'].update(visible=False)
			window['CATCHLIST'].update(visible=False)
			currentColumn.update(visible=False)
			window['COL4'].update(visible=True)
			window['CURR_SCORE'].update(visible=True)
			window['INFO'].update(visible=True)
			window['KEEP'].update(visible=True)
			window['RELEASE'].update(visible=True)
			window['IMG'].update(visible=True)
			currentColumn = window['COL4']
		# database is updated with new scores
		login.Account.updateData()
	# gui window is closed
	window.close()

# Once user has successfully logged in, they can begin playing game.
def game():
	currUser = preGameMenu()
	gamePlay(currUser)
