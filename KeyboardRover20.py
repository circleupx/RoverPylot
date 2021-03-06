'''
CONTROLS:

WASD - Drive
SPACE - Take Picture

J - Camera Up
K - Camera Down

U - Toggle Infrared
I - Toggle Lights


NOTES:

The rover cannot turn while moving forward/backward.

'''
from datetime import date
from random import choice
from string import ascii_lowercase, ascii_uppercase

import pygame
from pygame.locals import *

from rover import Rover20


# must be in interval [-1,1] (vals < 1 yield slower speeds)
MAX_TREAD_SPEED = 1

class KeyboardRover20(Rover20):
	def __init__(self):
		Rover20.__init__(self)	
		
		self.quit = False
		
		self.lightsAreOn = False
		self.stealthIsOn = False
		
		# WASD controls
		self.directionControls = {K_w: False, K_a: False, K_s: False,  K_d: False}
				
		# window must be open and in focus for pygame to take input
		self.windowSize = [640, 480]
		
		# used to only refresh the video and not the unused pixels
		self.imageRect = (160,120,320,240)
		
		# Live video frames per second
		self.fps = 48
		
		# stores what the camera currently sees
		self.currentImage = None
		
		self.displayCaption = "Keyboard Rover 2.0"
				
		pygame.init()
		pygame.display.init()		
		pygame.display.set_caption(self.displayCaption)
		
		self.screen = pygame.display.set_mode(self.windowSize)
		self.clock = pygame.time.Clock()
	
		
	# automagically called by Rover20, overriden to add functionality
	def processVideo(self, jpegbytes, timestamp_10msec):						
			
			if not self.quit:
				self.currentImage = jpegbytes
				self.refreshVideo()
				self.parseControls()
				self.updateTreadState()																		
				

		
	def parseControls(self):
		for event in pygame.event.get():			
			
			if event.type == QUIT:
				self.quit = True
			
			elif event.type == KEYDOWN:								
				# camera
				if event.key in (K_j, K_k, K_SPACE):
					self.updateCameraState(event.key)				
				
				# drive
				elif event.key in self.directionControls.keys():
					self.directionControls[event.key] = True				
				
				# infrared
				elif event.key is K_u:
					self.stealthIsOn = not self.stealthIsOn
					if self.stealthIsOn:
						self.turnStealthOn()						
					else:
						self.turnStealthOff()
										
				# lights
				elif event.key is K_i:
					self.lightsAreOn = not self.lightsAreOn
					if self.lightsAreOn:
						self.turnLightsOn()					
					else:
						self.turnLightsOff()
								
			elif event.type == KEYUP:
				# drive
				if event.key in self.directionControls.keys():
					self.directionControls[event.key] = False
				# camera
				elif event.key in (K_j, K_k):
					self.updateCameraState()
				
			
	# live video feed										
	def refreshVideo(self):
		self.takePicture('tmp.jpg')
		
		#load image, update display
		image = pygame.image.load('tmp.jpg').convert()		
		self.screen.blit(image, (160, 120))
		pygame.display.update(self.imageRect)
		
		#limit fps
		self.clock.tick(self.fps) 
	
	
	# move rover								
	def updateTreadState(self):			
		left, right = 0, 0
		
		# forward
		if self.directionControls[K_w]:
			left, right = MAX_TREAD_SPEED, MAX_TREAD_SPEED		
		# backward
		elif self.directionControls[K_s]:
			left, right = -MAX_TREAD_SPEED, -MAX_TREAD_SPEED
		# left	
		elif self.directionControls[K_a]:
			right = MAX_TREAD_SPEED		
			left = -right
		# right
		elif self.directionControls[K_d]:
			left = MAX_TREAD_SPEED
			right = -left
		
		self.setTreads(left, right)
	
	
	# move camera and take pictures
	def updateCameraState(self, key=None):
		# stationary
		if key is None:
			self.moveCameraVertical(0)
		# up
		elif key is pygame.K_j:
			self.moveCameraVertical(1)
		# down
		elif key is pygame.K_k:
			self.moveCameraVertical(-1)
		# take picture
		elif key is pygame.K_SPACE:
			self.takePicture(self.newPictureName())
	
	
	# save jpegbytes to file
	def takePicture(self, fname):
		fd = open(fname, 'w')
		fd.write(self.currentImage)
		fd.close()
		
				
	# return today's date plus a random string of letters
	def newPictureName(self):
		todaysDate = str(date.today())
		uniqueKey = ''.join(choice(ascii_lowercase + ascii_uppercase) \
							for _ in range(4))
		return todaysDate+'_'+uniqueKey+'.jpg'
		
		
			
def main():	
	
	rover = KeyboardRover20()
	
	while not rover.quit:
		pass
	
	rover.close()
	
			
if __name__ == '__main__':
	main()	
		
