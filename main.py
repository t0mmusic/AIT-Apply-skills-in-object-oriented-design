import login
import fish

# User logs into account, then plays the game
def main():
	currUser = login.Account.accountMenu()
	fish.Fish.fishingGame(currUser)

if __name__ == "__main__":
	main()
