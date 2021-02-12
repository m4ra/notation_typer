#!/usr/bin/python
import pygame
from pygame.locals import *
import sys, random, os, time

#DATABASE OF KEY MAPPINGS TO SYMBOLS AND THEIR POSITIONS RELATING TO THE STAFF

LEFT = -1
RIGHT=1

keyProps = {
	#directions/ can go everywhere, default in the middle left or middle right
	"q" : ("Diagonal_left_forward_down", LEFT, -1),
	"w" : ("Right_side_up", LEFT, -1), 
	"e" : ("Left_backward_up", LEFT, -1),
	"r" : ("Left_side_up", LEFT, -1),
	"t" : ("Left_forward_up", LEFT, -1),
	"a" : ("Diagonal_left_forward", LEFT, -1),
	"s" : ("Right_side", LEFT, -1), 
	"d" : ("Left_backward", LEFT, -1),
	"f" : ("Left_side", LEFT, -1), 
	"g" : ("Left_forward", LEFT, -1),
	"z" : ("Right_side_down", LEFT, -1),
	"x" : ("Left_backward_down", LEFT, -1),
	"c" : ("Left_side_down", LEFT, -1),
	
	"v" : ("Left_forward_down", LEFT, -1),
	"[" : ("Diagonal_right_backward_up", RIGHT, 0),
	"p" : ("Left_side_up", RIGHT, 0),
	"o" : ("Right_backward_up", RIGHT, 0),
	"i" : ("Right_side_up", RIGHT, 0),
	"u" : ("Right_forward_up", RIGHT, 0),
	"'" : ("Diagonal_right_backward", RIGHT, 0),
	";" : ("Left_side", RIGHT, 0), 
	"l" : ("Right_backward", RIGHT, 0),
	"k" : ("Right_side", RIGHT, 0),
	"j" : ("Right_forward", RIGHT, 0),
	"n" : ("Right_forward_down", RIGHT, 0),
	"m" : ("Right_side_down", RIGHT, 0),
	"," : ("Right_backward_down", RIGHT, 0),
	"." : ("Left_side_down", RIGHT, 0),
	"/" : ("Diagonal_right_backward_down", RIGHT, 0),
	"`" : ("Diagonal_left_forward", LEFT, -1),
	"1" : ("Diagonal_left_forward_up", LEFT, -1),
	"2" : ("Diagonal_left_forward_down", LEFT, -1),
	"3" : ("Pelvis", LEFT, -3),
	"4" : ("Waist", LEFT, -3),
	"5" : ("Chest", LEFT, -3), 
	"6" : ("Chest", RIGHT, 2),
	"7" : ("Waist", RIGHT, 2),
	"8" : ("Pelvis", RIGHT, 2),
	"9" : ("Diagonal_right_forward_down", RIGHT, 0),
	"0" : ("Diagonal_right_forward_up", RIGHT, 0),
	"-" : ("Diagonal_right_forward", RIGHT, 0),
	"y" : ("Rise", None, (-1,0)),
	"h" : ("Centre_middle", None, (-1,0)),
	"b" : ("Sink", None, (-1,0)),

	#body parts/ have fix position but go together with directions
	"f1" : ("Left_hand", LEFT, (-7)),
	"f2" : ("Left_elbow", LEFT, -6),
	"f3" : ("Left_shoulder", LEFT, -5),
	"f4" : ("Left_foot", LEFT, -2),
	"f5" : ("Left_knee", LEFT, -2),

	"f7" : ("Right_knee", RIGHT, 1),
	"f8" : ("Right_foot", RIGHT, 1),
	"f9" : ("Right_shoulder", RIGHT, 3),
	"f10" : ("Right_elbow", RIGHT, 4),
	"f11" : ("Right_hand", RIGHT, 5),
	"\\" : ("Torso", RIGHT, 2),
	"]" : ("Torso", LEFT, -3),
	"f6" : ("Head", None, 7),
	
}

fixKeys=["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "\\","3", "4", "5", "6","7", "8", "]"]
letters="abcdefghijklmnopqrstvyuzxw'/.,;'[901`2 -,["

all=letters
noFixKeys=list(all)

################################

#CLASSES FOR THE SYMBOLS/KEYS, THEIR SIZE AND POSITION IN THE STAFF
class Symbol:
	"""represents an image of movement"""
	
	def __init__(self, name):
		self.name=name
	
	def load(self):
		soundpath ="recordings/%s.wav" % self.name
		imgpath = "symbols/%s.png" % self.name
		surf=pygame.image.load(imgpath).convert_alpha()
		sound=pygame.mixer.Sound(soundpath)
		sound.play()
		return surf

class Stamp:
	"""represents a specific mark on the page/combination of a symbol with the position, and page"""
	def __init__(self, symbol):
		self.symbol=symbol.load() #pygame surface
	
	def set_pos(self, col, row):
		#list of valid positions
		self.pagex=width/2 + col*IMG_WIDTH
		self.pagey=height-((row+2)*GRIDHEIGHT)
		
	def draw(self, screen):
		screen.blit(self.symbol, (self.pagex, self.pagey))
	
class Page:
	"""list of stamps"""
	def __init__(self, stampsByPos={}):
		self.stampsByPos=stampsByPos
		self.cur_row = 0
		
	def draw(self, screen):
		for s in self.stampsByPos.values():
			s.draw(screen)
#######################################
def clearscreen():
	os.system("clear")

def onKey(key, page):
	"""how to find the position on the page"""
	global cursor_row, cursor_col, symbolsByPos, keylist, pages, count
	for k in keyProps.keys():
		if k!=key:
			pass
		else:
			if key in fixKeys:
				if keylist and keylist[len(keylist)-1] in noFixKeys and keylist[len(keylist)-2] in fixKeys:
					cursor_row+=0.7
					cursor_col= keyProps[key][2]
				elif not keylist:
					cursor_row=0
					cursor_col= keyProps[key][2]
			
				else:
					cursor_col= keyProps[key][2]
				s=Symbol(keyProps[key][0])
				st=Stamp(s)
				print cursor_col, cursor_row
				symbolsByPos[(cursor_col, cursor_row)]=st 
				st.set_pos(cursor_col, cursor_row)
			elif key in noFixKeys:
				if keylist and keylist[len(keylist)-1] in fixKeys:
					print 'body part + direction'
					cursor_row+=0.3
					cursor_col= keyProps[keylist[len(keylist)-1]][2]
				
				elif not keylist or not symbolsByPos:
					cursor_row=0
					if keyProps[key][1]==None:
						for c in keyProps[key][2]:
							cursor_col=random.choice(keyProps[key][2])
							
					else:
						cursor_col= keyProps[key][2]
					
				elif keylist[len(keylist)-2] in fixKeys:
					cursor_row+=0.7
					
					if keyProps[key][1]==None:
						cursor_col=random.choice(keyProps[key][2])
					else:
						cursor_col= keyProps[key][2]
				else:
					if keyProps[key][1]==None:
						cursor_col=random.choice(keyProps[key][2])
					else:
						cursor_col= keyProps[key][2]
					cursor_row+= 1
				s=Symbol(keyProps[key][0])
				st=Stamp(s)
				print cursor_col, cursor_row
				symbolsByPos[(cursor_col, cursor_row)]=st 
				st.set_pos(cursor_col, cursor_row)
						

keylist=[]
(cursor_col, cursor_row) = (0, 0)
symbolsByPos={}
pages=[]
page=Page(symbolsByPos)
count=0

filename = "dump.txt"
keydump = open(filename,"a")
keydump.write("----\n")
def notate(name, stamp):	
	global cursor_row, cursor_col, symbolsByPos, keylist, pages, count, page
	while 1:
		#print cursor_col, cursor_row
		#HANDLE EVENTS
		for event in pygame.event.get():
			if event.type == pygame.QUIT or \
			(event.type == KEYDOWN and event.key == K_ESCAPE):
				file=name.join('_') + str('%000d.bmp' % len(pages))
				if pages:
					for page in pages:
						cmnd = "lpr " + page
						print cmnd
						os.system(cmnd)
					pygame.image.save(screen, file)
					os.system('lpr ' + file)
					
				else:
					
					pygame.image.save(screen, file)
					os.system('lpr ' + file)
				keydump.close()
				os.system('mv *bmp prints')
				sys.exit()
			if event.type == KEYDOWN:
				current_key=event.key
				char=pygame.key.name(current_key)
				keydump.write(char)
				if cursor_row >=7:
					if keylist[len(keylist)-1] in fixKeys:
						pass
					else:
						cursor_row=0
						keylist=[]
						symbolsByPos={}
						pageFile=name.join('_') + ('%d.bmp' % count)
						pygame.image.save(screen, pageFile)
						pages.append(pageFile)
						page = Page(symbolsByPos)
						count+=1
						print pages
					
				onKey(char, page)
				keylist.append(char)
				
	    	#DRAW SCREEN
		screen.fill((255, 255, 255))
		# draw cursor
		cursor_width = IMG_WIDTH
		cx = width/2
		pygame.draw.rect(screen, (230, 247, 247), (cx + (cursor_col*IMG_WIDTH), stafftop, IMG_WIDTH, staffheight))
		pygame.draw.rect(screen, (230, 247, 247), (0, (staffbottom-((cursor_row+1)*GRIDHEIGHT)),  width, GRIDHEIGHT))
		#draw staff
		pygame.draw.rect(screen, (0, 0, 0), (cx-2*IMG_WIDTH, stafftop, 4*IMG_WIDTH, staffheight), 1) 
		pygame.draw.line(screen, (0, 0, 0), (cx, staffbottom), (cx, stafftop), 1)	
		#draw bits on the staff
		for row in range(0, 9, 1):
			pygame.draw.line(screen, (0, 0, 0), (cx+0.2*IMG_WIDTH, height-(row+1)*GRIDHEIGHT),( cx-0.2*IMG_WIDTH, height-(row+1)*GRIDHEIGHT), 1)
		#draw body indications
		rside=font.render('right side', True, (20, 150, 50))
		screen.blit(rside, (cx+30, staffbottom+35))	
		
		lside=font.render('left side', True, (255, 0, 0))
		screen.blit(lside, (cx-2*IMG_WIDTH, staffbottom +35))
		
		lleg=font.render('leg', True, (255, 0, 10))
		screen.blit(lleg, (cx-1.6*IMG_WIDTH, staffbottom +3))
		
		lbody=font.render('body areas', True, (255, 0, 20))
		screen.blit(lbody, (cx-4*IMG_WIDTH, staffbottom +3))
		
		larm=font.render('arm', True, (255, 0, 30))
		screen.blit(larm, (cx-6*IMG_WIDTH, staffbottom +3))
		
		rleg=font.render('leg', True, (0, 160, 60))
		screen.blit(rleg, (cx+1.2*IMG_WIDTH, staffbottom +3))
	
		rbody=font.render('body areas', True, (0, 170, 70))
		screen.blit(rbody, (cx+2.5*IMG_WIDTH, staffbottom+3))
	
		rarm=font.render('arm', True, (0, 180, 80))
		screen.blit(rarm, (cx+5.5*IMG_WIDTH, staffbottom +3))
		#draw the name of the copyright holder
		identity=font.render('Copyright '+ name +' 2009', True, (30, 20, 30))
		screen.blit(identity, (10, 22))
		#draw the license of the notation
		licenses=font.render(stamp, True, (90, 90, 90))
		screen.blit(licenses, (10, 5))	
		# draw cur page number
		pnumber=fontSmall.render(str(count+1), True, (100, 100, 100))
		screen.blit(pnumber,(cx+7*IMG_WIDTH, 30))
		
		#DRAW CUR PAGE
		page.draw(screen)
		#refresh frames
		pygame.display.flip()
		clock.tick(FPS)
########################
clearscreen()		

print '\t'+'\t'+'----Notations Under Provisions----'
time.sleep(1.5)
print
print """Make your dance notation by typing the symbols on the keyboard. Please answer the questions before starting notating!"""
time.sleep(1.5)
print
print """ This notation system is based on Rudolf Laban's movement analysis system."""
time.sleep(1.5)
print
questions=[
	'Please type your name: ',
	'Press ENTER to start and ESC to exit the programme. Your notation will be saved to a file and printed if you have set up a printer on your computer.'
]
resp=[]

i=0
while i <= 1:

	inp=raw_input(questions[i])
	resp.append(inp)
	i+=1
if resp[1] != '':
	sys.exit()

else:
	#GET PYGAME READY TO RUN
	pygame.font.init() # we need fonts
	pygame.init()
	pygame.mixer.init() # we need sound
	####################
	#CONSTANTS-TWEAK ME
	fontpath="/Library/Fonts/LiberationSans-Regular.ttf"
	font=pygame.font.Font(fontpath, 15)
	fontSmall=pygame.font.Font(fontpath, 13)

	size = width, height = 1024, 768
	FPS = 50
	IMG_WIDTH=50
	GRIDHEIGHT=80
	VAR=int(height/GRIDHEIGHT)-1 #a whole number => devide the screen height with the grid size and substruct 2 => twice the grid size (once from bottom/once from top)
	staffheight=VAR*GRIDHEIGHT
	staffbottom=height-GRIDHEIGHT
	stafftop= staffbottom-staffheight
	pygame.display.set_caption('Labanotation')

	# open pygame window
	screen = pygame.display.set_mode(size)
	pygame.display.toggle_fullscreen()
	# make a pygame clock
	clock = pygame.time.Clock()	
	#give the name of the user to the notation	
	name=resp[0] 
	
	#copyrright to public domain
	
	stamp='Notation released to Public Domain'
		
	notate(name, stamp)
