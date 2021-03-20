# NAME HERE
# Works Cited
# adapted from https://replit.com/@MeMyselfAnDie/Turtle-Hangman

###### imports

import turtle

###### constants

# general
COLORS = ["black", "white", "blue", "lightgray", "red"]

# screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_COLOR = COLORS[4]

# keyboard
KEYBOARD_X = -350
KEYBOARD_Y = 100

# keyboard keys
KEY_SIZE = 40
KEY_BORDER_COLOR = COLORS[0]
KEY_FILL_COLOR = COLORS[3]
KEY_SPACING = 5
KEY_LETTER_SIZE = 8
KEY_BORDER_LINE_WIDTH = 1
KEY_FONT_STYLE = "bold"
KEY_FONT = "Arial"

# text display area
DISPLAY_FIELD_LEFT = -350
DISPLAY_FIELD_RIGHT = 220
DISPLAY_FIELD_TOP = 280
DISPLAY_FIELD_BOTTOM = 160

# characters in display area
LETTER_HORIZONTAL_SPACING = 10
LETTER_VERTICAL_SPACING = 15
LETTER_SIZE = 10
LETTER_COLOR = COLORS[4]
LETTER_FONT_STYLE = "bold"
LETTER_FONT = "Arial"


###### variables

# screen
screen = turtle.Screen()
screen.bgcolor(SCREEN_COLOR)
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)

# text
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.speed(0)
pen.color(LETTER_COLOR)

# text display area (cursor location)
textLocationX = DISPLAY_FIELD_LEFT
textLocationY = DISPLAY_FIELD_TOP - LETTER_VERTICAL_SPACING

display = turtle.Turtle()
display.hideturtle()
display.penup()
display.speed(0)
display.goto(DISPLAY_FIELD_LEFT, DISPLAY_FIELD_TOP)
display.pendown()
display.goto(DISPLAY_FIELD_RIGHT, DISPLAY_FIELD_TOP)
display.goto(DISPLAY_FIELD_RIGHT, DISPLAY_FIELD_BOTTOM)
display.goto(DISPLAY_FIELD_LEFT, DISPLAY_FIELD_BOTTOM)
display.goto(DISPLAY_FIELD_LEFT, DISPLAY_FIELD_TOP)
textLocationY -= LETTER_VERTICAL_SPACING

###### functions

class ButtonBuilder(turtle.Turtle):
	# constructor
	def __init__(self):
		turtle.Turtle.__init__(self)
		self.buttons = []
		self.hideturtle()
		self.penup()
		self.speed(0)
		
		# defaults
		self.fillcolor(COLORS[0])
		self.linecolor(COLORS[0])
		self.textcolor(COLORS[0])
		self.width(KEY_BORDER_LINE_WIDTH)
		self.font((KEY_FONT, KEY_LETTER_SIZE, KEY_FONT_STYLE))

		turtle.Screen().onclick(self.click)

	def font(self, font):
		self.__font = font

	def linecolor(self, color):
		self.pencolor(color)
	
	def textcolor(self, color):
		self.__textcolor = color

	def makeButton(self, x, y, width, height, text):
		self.buttons.append(((x, y, x + width, y + height), text))
		self.penup()
		self.goto(x, y)

		self.begin_fill()
		self.goto(x + width, y)
		self.goto(x + width, y + height)
		self.goto(x, y + height)
		self.goto(x, y)
		self.end_fill()

		self.pendown()
		self.goto(x + width, y)
		self.goto(x + width, y + height)
		self.goto(x, y + height)
		self.goto(x, y)
		self.penup()
		self.goto(x + width / 2, y + (height - self.__font[1]) / 2)
		pencolor = self.pencolor()
		fillcolor = self.fillcolor()
		self.color(self.__textcolor)
		self.write(text, align = "center", font = self.__font)
		self.color(pencolor, fillcolor)

	def click(self, x, y):
		print("DEBUGGING: click at (" + str(x) + ", " + str(y) + ")")
		for button in reversed(self.buttons):
			if (self.__contains(button[0], (x, y))):
				buttonPressed(button[1], button[0])
				return

	def __contains(self, rect, point):
		# rect = 	[xMin, yMin, xMax, yMax]
		# point = [x, y]
		return not((point[0] < rect[0]) or (point[0] > rect[2]) or (point[1] < rect[1]) or (point[1] > rect[3]))





def displayKeyboard(x, y, keySize):  
	# speed up the display of the keyboard
	# tracer(n, delay)
	# n = show 0 incremental refresh updates
	# delay = slow down the display refreshes (millisecond)
	turtle.Screen().tracer(0, 0) 

	# create a button builder object
	buttonBuilder = ButtonBuilder()

	# set the style settings of the buttons
	buttonBuilder.linecolor(KEY_BORDER_COLOR)
	buttonBuilder.fillcolor(KEY_FILL_COLOR)
	buttonBuilder.textcolor(KEY_BORDER_COLOR)

	# inner function
	def buildKeyboard(x, y, keySize):
		# parameters:
		# x = left boundary
		# y = bottom boundary
		# keySize = width / height of keys
		keys = ["1234567890-=c", "QWERTYUIOP[]", "ASDFGHJKL;'¶", "ZXCVBNM,./"]
		yOffset = 0
		rowOffset = 0

		for row in keys:
			xOffset = rowOffset

			for letter in row:
				buttonBuilder.makeButton(x + xOffset, y + yOffset, keySize, keySize, letter)
				xOffset += keySize + KEY_SPACING

			yOffset -= keySize + KEY_SPACING
			rowOffset += keySize / 3
	
	# display the keyboard
	buildKeyboard(x, y, keySize)

	turtle.Screen().tracer(1, 10)

# bounds => (xMin, yMin, xMax, yMax)
def buttonPressed(value, bounds):
	global textLocationX
	global textLocationY

	print("DEBUGGING: buttonPressed", value, bounds)

	# word wrap cursor if within a character's width of the right edge
	if textLocationX > DISPLAY_FIELD_RIGHT - LETTER_HORIZONTAL_SPACING:
		# move cursor to the left edge of the display
		textLocationX = DISPLAY_FIELD_LEFT
		# move cursor down a row
		textLocationY -= LETTER_VERTICAL_SPACING

	

	if value == "c":
		# Clear key was pressed
		# clear the display area
		pen.clear()
		# reset the cursor to the top left corner
		# move cursor to the left edge of the display
		textLocationX = DISPLAY_FIELD_LEFT
		# move cursor to the top edge of the display
		# TODO - refine this vertical placement logic
		textLocationY = DISPLAY_FIELD_TOP - 2 * LETTER_VERTICAL_SPACING
		pen.goto(DISPLAY_FIELD_LEFT, DISPLAY_FIELD_TOP)
	elif value == "¶":
		# Enter/Return key was pressed
		# move cursor down a row
		textLocationY -= LETTER_VERTICAL_SPACING
		# move cursor to left edge of display
		textLocationX = DISPLAY_FIELD_LEFT
	else:
		# moving cursor to the right for the 
		# next character to be displayed
		textLocationX += LETTER_HORIZONTAL_SPACING
		pen.goto(textLocationX, textLocationY)
		# display the next typed character (value)
		pen.write(value, align = "center", font = (LETTER_FONT, LETTER_SIZE, LETTER_FONT_STYLE))

		# TODO - build a logical representation of the current characters in the
		# display area. 
		# Break into tokens (by the spaces) and determine if the 
		# tokens are numbers or words in a known dictionary, 
		# if they are numbers (numeric digits and negative 
		# symbol or decimal point, build a base 10 number to be 
		# used in math expressions
		# (THIS IS A LOT OF WORK)
		

###### main

displayKeyboard(KEYBOARD_X, KEYBOARD_Y, KEY_SIZE)

# def mb(x, y, keysize):
# 	buttonBuilder = ButtonBuilder()
# 	buttonBuilder.linecolor(KEY_BORDER_COLOR)
# 	buttonBuilder.fillcolor(KEY_FILL_COLOR)
# 	buttonBuilder.textcolor(KEY_BORDER_COLOR)
# 	buttonBuilder.makeButton(x, y, keysize, keysize, "OK")
# mb(0, -100, KEY_SIZE)