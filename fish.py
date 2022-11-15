import os
import csv
import random
import login

# array containing all Fish Objects
fishArray = []

class Fish:
	# Number of random variables in array
	ranCount = -2

	# create a new Fish with a name, whether to keep,
	# whether it is a fish, points if kept, points if released
	def __init__(self, name, keeper, fish, points_keep, points_release):
		self.name = name
		self.keeper = keeper
		self.fish = fish
		self.points_keep = points_keep
		self.points_release = points_release
	
	# returns a string to print stats about fish object
	def __str__(self):
		stars = "****************\n"
		return (stars + 
			f"Type: {self.name}\n"
			f"Keeper: {self.keeper}\n"
			f"Fish: {self.fish}\n"
			f"Points if kept: {self.points_keep}\n"
			f"Points if released: {self.points_release}\n" + stars)

	# Imports fish information from csv file into array of Fish objects.
	# If the file does not exist, it will create and populate it
	def importData():
		if (os.path.exists('fish.csv') == False):
			with open('fish.csv', 'w', encoding='UTF8', newline='') as f:
				writer = csv.writer(f)
				writer.writerow(["Name", "Keeper", "Fish", "Points if kept", "Points if released"])
				writer.writerow(["King George Whiting", "yes", "yes", "50", "70"])
				writer.writerow(["Lost Bait", "no", "no", "-10", "0"])
				writer.writerow(["Small Mulloway", "no", "yes", "-10", "10"])
				writer.writerow(["Snapper", "yes", "yes", "30", "40"])
				writer.writerow(["Large Mullet", "yes", "yes", "20", "20"])
				writer.writerow(["Seaweed Monster", "yes", "no", "5", "-5"])
		with open('fish.csv') as f:
			csv_reader = csv.reader(f, delimiter=',')
			count = 0
			for row in csv_reader:
					if (count != 0):
						fish = Fish(row[0], row[1], row[2], row[3], row[4])
						fishArray.append(fish)
					count += 1
			Fish.ranCount += count

	# Randomly returns one Fish from the array
	def castLine():
		ran = random.randint(0, Fish.ranCount)
		print(ran)
		return (fishArray[ran])

	# The fishing game. Allows the user to cast a line or exit.
	# Once the user has caught a fish, they can either keep or
	# Release it. Their score will be updated accordingly.
	def fishingGame(currUser):
		currUser.score = int(0)
		currUser.highScore = int(currUser.highScore)
		while (True):
			print(currUser)
			select = input("1. Cast Line\n2. Exit\n")
			if (select == "1"):
				catch = Fish.castLine()
				print(catch)
				select = input("1. Keep\n2. Release\n")
				if (select == "1"):
					currUser.score += int(catch.points_keep)
				elif (select == "2"):
					currUser.score += int(catch.points_release)
				else:
					print("You dropped it!")
					currUser.score += int(catch.points_release)
				if (currUser.highScore < currUser.score):
					currUser.highScore = currUser.score
			elif (select == "2"):
					break
			else:
				print("Invalid Selection!")
			login.Account.updateData()
		print(currUser)
		exit()

# When this script is loaded, this function is called to populate the array.
Fish.importData()
