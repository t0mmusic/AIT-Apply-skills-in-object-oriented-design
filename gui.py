import login
import fish
import PySimpleGUI as sg

sg.theme('DarkRed')
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
# universal layout to display all features of the gui
layout = [
			[sg.Button('Log In', key='LOGIN_MENU'),
			sg.Button('Sign Up', key='SIGNUP_MENU'),
			sg.Button('High Scores', key='SCORE')],
			[sg.Text(key='INFO')],
			[sg.Column(layoutLog, key='COL1'),
			sg.Column(layoutSign, visible=False, key='COL2'),
			sg.Column(layoutScore, visible=False, key='COL3'),
			sg.Column(layoutGame, visible=False, key='COL4')],
			[sg.Button('Start Playing!', key='LOGIN'),
			sg.Button('Start Playing!', key='SIGNUP', visible=False)],
			[sg.Image(key='IMG', visible=False)],
			[sg.Button('Exit', key='EXIT')]
		]

# creates a window gui
# sg.theme_previewer()
window = sg.Window('Hello and thanks for all the fish', layout, size=(500, 500), finalize=True)

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
	scoreString = '\n'.join([str(x) for x in scoreArray])
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
			exit()
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

# updates the image to the appropriate matching fish. If there
# are more than 6 fish, others are given a placeholder image.
def updateImage(fish):
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
	window['IMG'].update(img, size=(500, 300), visible=True)
	

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
	window['INFO'].update("")
	while (True):
		event, values = window.read()
		if (event == sg.WINDOW_CLOSED or event == 'EXIT'):
			break
		# User casts a line to catch a fish, caught fish is displayed
		if (event == 'THROW'):
			window['KEEP'].update(visible=True)
			window['RELEASE'].update(visible=True)
			window['THROW'].update(visible=False)
			catch = fish.Fish.castLine()
			window['INFO'].update("You caught a " + catch.name + "!")
			updateImage(catch.name)
		# User keeps fish, score is updated with points_kept added
		if (event == 'KEEP'):
			currUser.score += int(catch.points_keep)
			window['CURR_SCORE'].update("Current Score: " + str(currUser.score))
			window['INFO'].update("You decided to keep your catch!")
			window['KEEP'].update(visible=False)
			window['RELEASE'].update(visible=False)
			window['THROW'].update(visible=True)
		# User releases fish, score is updated with points_release added
		if (event == 'RELEASE'):
			currUser.score += int(catch.points_release)
			window['CURR_SCORE'].update("Current Score: " + str(currUser.score))
			window['INFO'].update("You decided to release your catch!")
			window['KEEP'].update(visible=False)
			window['RELEASE'].update(visible=False)
			window['THROW'].update(visible=True)
		# if the highscore value is lower than the current score value, it is
		# updated to the current value
		if (currUser.score > currUser.highScore):
			currUser.highScore = currUser.score
		# Displays LeaderBoard
		if (event == 'SCORE'):
			window['SCORE'].update(visible=False)
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
			window['LOGIN_MENU'].update(visible=False)
			currentColumn.update(visible=False)
			window['COL4'].update(visible=True)
			currentColumn = window['COL4']
	# database is updated with new scores
	login.Account.updateData()
	# gui window is closed
	window.close()

# Once user has successfully logged in, they can begin playing game.
def game():
	currUser = preGameMenu()
	gamePlay(currUser)