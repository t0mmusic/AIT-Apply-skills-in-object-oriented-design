import hashlib
import csv
import os
import getpass

# Array of all Accounts in database
accountArray = []

class Account:
	# initialise an Account object
	def __init__(self, username, password, score, highScore):
		self.username = username
		self.password = password
		self.score = int(score)
		self.highScore = int(highScore)

	# Print Account info
	def __str__(self):
		stars = "****************\n"
		return (stars + 
			f"Username: {self.username}\n"
			f"Current Score: {self.score}\n"
			f"High Score: {self.highScore}\n" + stars)

	# Checks if a username is already registered in database
	def compareUsername(username):
		for x in accountArray:
			if (x.username == username):
				return (x)
		return False

	# Checks if a password is already registered in database
	def comparePassword(password):
		hash_password = hashPassword(password)
		for x in accountArray:
			if (x.password == hash_password):
				return (x)
		return False

	# Imports from database and converts into Account objects.
	# If database does not exist, creates and populates it.
	def importUserData():
		if (os.path.exists('userBase.csv')):
			with open('userBase.csv') as f:
				csv_reader = csv.reader(f, delimiter=',')
				line_count = 0
				for row in csv_reader:
					if line_count == 0:
						line_count += 1
					else:
						currAccount = Account(row[0], row[1], row[2], row[3])
						accountArray.append(currAccount)
		else:
			with open('userBase.csv', 'w', encoding='UTF8', newline='') as f:
				writer = csv.writer(f)
				writer.writerow(["Username", "Password", "Current Score", "High Score"])

	# Updates database when Account is modified
	def updateData():
		with open('userBase.csv', 'w', encoding='UTF8', newline='') as f:
			writer = csv.writer(f)
			writer.writerow(["Username", "Password", "Current Score", "High Score"])
		with open('userBase.csv', 'a', encoding='UTF8', newline='') as f:
			writer = csv.writer(f)
			for x in accountArray:
				account = [x.username, x.password, x.score, x.highScore]
				writer.writerow(account)

	def hashPassword(password):
		return (hashlib.md5(password.encode()).hexdigest())

	# Displays the top 10 accounts by high score, or all accounts if less than
	# 10 are in the database
	def showLeaderboard():
		scoreArray = accountArray
		scoreArray.sort(key=lambda x: x.highScore, reverse=True)
		ret = []
		i = 0
		print("****************************")
		for x in scoreArray:
			i += 1
			print(str(i) + ": " + str(x.username) + ": " + str(x.highScore))
			ret.append(str(i) + ": " + str(x.username) + ": " + str(x.highScore))
			if (i == 10):
				break
		if (i == 0):
			print("No high scores to display!")
		print("****************************")
		return(ret)

	# Selection menu for accounts
	# 1 = login to existing account
	# 2 = create new account
	# 3 = view account leaderboard
	# 4 = exit
	def accountMenu():
		while (True):
			select = input("1. Login\n2. Sign up\n3. View Leaderboard\n4. Exit\n")
			if (select == "1"):
				currUser = UserPassword.login()
				if (currUser != False):
					break
			elif (select == "2"):
				currUser = UserPassword.createAccount()
				if (currUser != False):
					break
			elif (select == "3"):
				Account.showLeaderboard()
			elif (select == "4"):
				exit()
			else:
				print("Invalid Selection!")
		return (currUser)

class UserPassword:
	# Sets a new password, confirms password, then
	# encripts and stores in database
	def setPassword():
		auth1 = getpass.getpass("Enter Password: ")
		auth2 = getpass.getpass("Confirm Password: ")
		if (auth1 == auth2):
			return (Account.hashPassword(auth1))
		else:
			print("Passwords entered do not match.")
			return (False)

	# sets password with hashfunction using matching strings
	def setPassword(p1, p2):
		if (p1 == p2):
			return (Account.hashPassword(p1))
		return (False)

	# Sets username, checks whether same username already
	# exists in database
	def setUsername():
		username = input("Choose a username: ")
		if (Account.compareUsername(username) == False):
			return (username)
		print("Username already exists.")
		return (False)

	# Sets username and password, then adds new Account to
	# database with 0 for both current and high scores
	def createAccount():
		username = UserPassword.setUsername()
		if (username == False):
			return (False)
		password = UserPassword.setPassword()
		if (password == False):
			return (False)
		account = [username, password, 0, 0]
		with open('userBase.csv', 'a', encoding='UTF8', newline='') as f:
			writer = csv.writer(f)
			writer.writerow(account)
		print("Account Successfully Created!")
		ret = Account(username, password, 0, 0)
		accountArray.append(ret)
		return (ret)

	# creates account using verified username and password
	def createAccount(username, password):
		account = [username, password, 0, 0]
		with open('userBase.csv', 'a', encoding='UTF8', newline='') as f:
			writer = csv.writer(f)
			writer.writerow(account)
		ret = Account(username, password, 0, 0)
		accountArray.append(ret)
		return (ret)

	# Username and password are checked against database for validity
	# If either are incorrect, False is returned,
	# otherwise, matching Account is returned.
	def login():
		username = input("Enter Username: ")
		if (Account.compareUsername(username) == False):
			print("No user by that name found.")
			return (False)
		password = getpass.getpass("Enter Password: ")
		if (Account.comparePassword(password) == False):
			print("Password entered was incorrect.")
			return (False)
		ret = Account.compareUsername(username)
		print("Successfully logged in.")
		return (ret)

	# logs in to account once username and password have
	# been verified
	def login(username, password):
		user = Account.compareUsername(username)
		if (user == False):
			return (user)
		if (Account.hashPassword(password) != user.password):
			return False
		return (user)

# populates account array when script is run
Account.importUserData()
