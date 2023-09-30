# Importation des bibliothèques (ma librairie graphique (version 2.0.1, qui importe math et pygame) et random)
from mlib import *
from random import *

# Pour comprendre comment fonctionne le code, je vous invite à aller voir la documentation de ma librairie graphique (voir documentation.html)

# Dimensions de la fenetre
largeur = 638
hauteur = 320
TAILLE = (largeur, hauteur)

# Chargement de pygame et mlib
screen = pygame.display.set_mode(TAILLE)
mapp = MApp(screen, "Test", TAILLE[0], TAILLE[1], console=False, printFps=True)

#Permet de normaliser un angle radian ou non
def normaliserAngle(angle, rad = True):
	if rad:
		angle *= 360/(pi*2)

	while angle >= 360: angle -= 360
	while angle < 0: angle += 360

	if rad:
		angle /= 360/(pi*2)

	return angle

# Fonction qui retourne l'angle miroir d'un angle sur l'axe x ou y d'un angle radian ou non
def angleMiroir(angle, axe = "x", rad = True):
	toReturn = 0
	if rad:
		angle *= 360/(pi*2)

	if axe == "x":
		if angle == 0 or angle == 180:
			toReturn = angle
		elif angle < 180:
			toReturn = 180 + (180 - angle)
		else:
			toReturn = 360 - angle
	elif axe == "y":
		if angle == 90 or angle == 270:
			toReturn = angle
		elif angle < 90:
			toReturn = 90 + (90 - angle)
		elif angle > 270:
			toReturn = 270 - (angle - 270)
		elif angle < 180:
			toReturn = 180 - angle
		else:
			toReturn = 270 + (270 - angle)

	if rad:
		toReturn /= 360/(pi*2)

	return toReturn

# Retourne la distance entre 2 points
def distance2D(x1, y1, x2, y2):
	return sqrt((x2-x1)**2+(y2-y1)**2)
	

# Création de la classe des balles
# La classe héritant de MImage, elle affiche la texte de la balle
class Balle:
	# Chargement des constantes de Balle
	BALLE_RAYON = 25
	Z = 100

	# Constructeur d'une balle (qui prend un attribut x et y, mais aussi z pour calculer sa taille en profondeur)
	def __init__(self, rayon, x, y, parent, widgetType="MImage"):

		#Attributs de géométrie (les coordonnées représentent le centre du cercle)
		self.rayon = rayon
		self.x = 0
		self.y = 0

		#Attributs de force
		self.dessinerForce = False
		self.dx = 0
		self.dy = 0

		#Charger la texture
		self.chargerTexture()

		#Bouger la balle et calculer le rétrecissement de la balle par la même occasion
		self.move(x, y)
	
	# Permet de charger la texture de la balle
	def chargerTexture(self):
		self.TEXTURE = image.load("img/balle.png").convert_alpha() #Texture cosntance de référence
		self.texture = image.load("img/balle.png").convert_alpha() #Texture utilisé

	# Retourne l'attribut dx
	def getDX(self):
		return self.dx
	
	# Retourne l'attribut dy
	def getDY(self):
		return self.dy
	
	# Retourne la valeur de la force de la balle
	def getForce(self):
		return self.force
	
	# Retourne la valeur de l'angle (en radian) de la force de la balle sur les axes x et y (pour comprendre comment fonctionne l'angle, voir angle.png)
	def getForceAngleXY(self):
		return self.forceAngleXY
	
	# Retourne la valeur du rayon du cercle
	def getRayon(self):
		return self.rayon
	
	# Retourne la texture à utiliser
	def getTexture(self):
		return self.texture
	
	# Retourne l'attribut x
	def getX(self):
		return self.x
	
	# Retourne l'attribut y
	def getY(self):
		return self.y
	
	# Changer l'attribut x, y et z
	def move(self, x, y):
		self.setX(x)
		self.setY(y)

	# Permet de redimensionner la texture selon le rayon et l'attribut z du cercle
	def redimensionnerTexture(self):
		if (self.getRayon() * 2) / self.TEXTURE.get_width() != 1:
			self.texture = transform.scale_by(self.TEXTURE, ((self.getRayon() * 2) / self.TEXTURE.get_width(), (self.getRayon() * 2) / self.TEXTURE.get_height()))
	
	# Permettre le dessin d'une flèche indiquant l'angle de la force
	def setDessinerForce(self, dessinerForce):
		if self.dessinerForce != dessinerForce:
			self.dessinerForce = dessinerForce
			self.setShouldModify(True)

	# Retourne l'attribut dx
	def setDX(self, dx):
		self.dx = dx
	
	# Retourne l'attribut dy
	def setDY(self, dy):
		self.dy = dy

	# Change la valeur de rayon
	def setRayon(self, rayon):
		if self.getRayon() != rayon:
			self.rayon = rayon
			self.redimensionnerTexture()

	# Change la valeur de l'attribut z
	def setX(self, x):
		if self.x != x:
			self.x = x

	# Change la valeur de l'attribut z
	def setY(self, y):
		if self.y != y:
			self.y = y

	# Vérifie si un cercle rentre en collision avec un autre
	def touche(self, balle):
		return distance2D(self.getX(), self.getY(), balle.getX(), balle.getY()) <= self.getRayon() + balle.getRayon()
	
	def touchePoint(self, x, y, rayon = 0):
		return distance2D(self.getX(), self.getY(), x, y) <= self.getRayon() + rayon

	# Retourner le vecteur vitesse de la balle selon la force et son angle
	def vecteurVitesse(self):
		return (self.getDX(), self.getDY())

# Création de la classe du moteur de jeu
# La classe héritant de MImage, elle affiche l'image de font
class Game(MImage):

	# Constructeur du moteur de jeu
	def __init__(self, x, y, parent, widgetType="MImage"):
		super().__init__('img/fond.jpg', x, y, TAILLE[0], TAILLE[1], parent, widgetType)

		self.armePosition = (0, 0) #Position de l'arme
		self.armeTexture = 0 #Surface qui contient la texture de l'arme
		self.armeType = "glock48" #Type de l'arme utilisé
		self.balles = [] #Liste qui contient toutes les balles du jeu

		self.chargerArme(self.armeType)

		# Texte qui sera affiché au bas de la fenetre
		WHITE = pygame.Color(255, 255, 255)
		text = MText('Projet NSI', 490, 300, 100, 20, self)
		text.setBackgroundColor((0, 0, 0, 0))
		text.setFont('font/elite.ttf')
		text.setFontSize(16)
		text.setTextColor(WHITE)
		text.setTextVerticalAlignment(1)

	# Charger l'arme à utiliser
	def chargerArme(self, arme):
		self.armeType = arme
		if os.path.exists("img/" + arme + ".png"): #Charger la texture
			self.armeTexture = image.load("img/" + arme + ".png").convert_alpha()
		else:
			self.armeTexture = image.load("img/unknow.png").convert_alpha()
		self.setShouldModify(True)

	# Retourne si une balle est présente à une position
	def balleALaPosition(self, x, y, rayon = 0):
		for i in self.balles:
			if i.touchePoint(x, y, rayon):
				return i
		return 0

	# Créer nombre balle
	def creerBalle(self, nombre):
		for i in range(nombre):
			# Coordonnees de la POSITION initiale de la nouvelle balle (générees aléatoirement)
			angleXY = pi * 2 * random()
			f = 450 * random() + 50
			x = random()*(largeur-Balle.BALLE_RAYON)
			y = random()*(hauteur-Balle.BALLE_RAYON)

			while self.balleALaPosition(x, y, 50) != 0:
				x = random()*(largeur-Balle.BALLE_RAYON)
				y = random()*(hauteur-Balle.BALLE_RAYON)

			balle = Balle(25, x, y, self)
			balle.setDX(cos(angleXY) * f)
			balle.setDY(sin(angleXY) * f)
			self.balles.append(balle)

	# Retourne la taille de la zone de tir (endroit où sont les balles)
	#def tailleZoneDeTir(self):

	# Fonction utilisé quand la souris est bougé sur la zone de jeu
	def _mouseMove(self, buttons, pos, relativeMove):
		self.armePosition = (round(pos[0] - self.armeTexture.get_width() / 2), round(pos[1] - self.armeTexture.get_height() / 2))

	# Dessine sur la surface de jeu
	def _renderBeforeHierarchy(self, surface):
		surface = super()._renderBeforeHierarchy(surface)

		#Dessiner les balles
		for i in self.balles:
			surfaceABlit = i.getTexture()

			surface.blit(surfaceABlit, (i.getX(), i.getY(), surfaceABlit.get_width(), surfaceABlit.get_height()))

		#Dessiner l'arme
		surface.blit(self.armeTexture, (self.armePosition[0], self.armePosition[1], self.armeTexture.get_width(), self.armeTexture.get_height()))

		return surface

	# Fonction appelée à chaque frames par mapp avec deltaTime le temps qu'a duré la dernière frame
	def _update(self, deltaTime):
		for index in range(len(self.balles)):
			i = self.balles[index]

			ancienX = i.getX()
			ancienY = i.getY()

			nouveauX = ancienX + i.getDX() * deltaTime
			nouveauY = ancienY + i.getDY() * deltaTime

			i.move(nouveauX, nouveauY)

			# On calcule les collisions avec les autres joueurs
			for j in self.balles[index + 1:]:
				if i.touche(j):
					i.move(ancienX, ancienY)
					nouveauX = ancienX
					nouveauY = ancienY

					i.setDX(-i.getDX())
					i.setDY(-i.getDY())

					j.setDX(-j.getDX())
					j.setDY(-j.getDY())

			# On prend en compte les rebonds avec le bord
			if nouveauX < 0:
				nouveauX = 0
				i.setDX(-i.getDX())
			elif nouveauX > self.getWidth() - i.getTexture().get_width():
				nouveauX = self.getWidth() - i.getTexture().get_width()
				i.setDX(-i.getDX())

			if nouveauY < 0:
				nouveauY = 0
				i.setDY(-i.getDY())
			elif nouveauY > self.getHeight() - i.getTexture().get_height():
				nouveauY = self.getHeight() - i.getTexture().get_height()
				i.setDY(-i.getDY())

			i.move(nouveauX, nouveauY)

		self.setShouldModify(True)


# Chargement du moteur de jeu
moteurDeJeu = Game(0, 0, mapp)
moteurDeJeu.creerBalle(25)

#  --------------------------------------------------------------------------
#      Boucle exécutée tant que MLib ne reçoit pas d'event "pygame.QUIT"
#  --------------------------------------------------------------------------

while True:
	# Actualiser les évènements pygame et MLib
	mapp.frameEvent()
					
	# Actualisater l'affichage graphique MLib et afficher de l'image
	mapp.frameGraphics()
	pygame.display.update()


#  --------------------------------------------------------------------------
#                              Fin de la boucle 
#  --------------------------------------------------------------------------
