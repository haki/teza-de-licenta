import pygame as pg


def init():  # Initialize the pygame module
    pygame.init()  # Initialize the pygame module
    win = pygame.display.set_mode((100, 100))  # Create a window of size 100x100


def getKey(keyName):  # Get the key pressed
    ans = False  # Initialize the answer
    for eve in pygame.event.get(): pass  # Get the events
    keyInput = pygame.key.get_pressed()  # Get the key pressed
    myKey = getattr(pygame, 'K_{}'.format(keyName))  # Get the key pressed
    if keyInput[myKey]:  # If the key pressed is the key we want
        ans = True  # Set the answer to True
    pygame.display.update()  # Update the display

    return ans  # Return the answer


def main():  # Main function
    if getKey('LEFT'):  # If the left key is pressed
        print('Key Left was pressed')  # Print the message
    if getKey('RIGHT'):  # If the right key is pressed
        print('Key Right was pressed')  # Print the message


if __name__ == '__main__':  # If the file is run directly
    init()  # Initialize the pygame module
    while True:  # Loop forever
        main()  # Run the main function
