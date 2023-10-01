# Importation des bibliothèques (ma librairie graphique (version 2.0.1, qui importe math et pygame) et random)
from mlib import *
from random import *

# Pour comprendre comment fonctionne le code, je vous invite à aller voir la documentation de ma librairie graphique (voir documentation.html)

# Dimensions de la fenetre
largeur = 638
hauteur = 370
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

		#Attributs de force et de physique
		self.collisions = []
		self.dessinerForce = False
		self.dx = 0
		self.dy = 0
		self.masse = 1

		#Attributs d'affichage
		self.rouge = False

		#Charger la texture
		self.chargerTexture()

		#Bouger la balle et calculer le rétrecissement de la balle par la même occasion
		self.move(x, y)

	# Retourne le point centre entre cette balle et autreBalle
	def centre(self, autreBalle):
		return (autreBalle.getX() - self.getX(), autreBalle.getY() - self.getY())
	
	# Permet de charger la texture de la balle
	def chargerTexture(self):
		self.TEXTURE = image.load("img/balle.png").convert_alpha() #Texture constance de référence
		self.texture = image.load("img/balle.png").convert_alpha() #Texture utilisée
		self.TEXTUREROUGE = image.load("img/balleRouge.png").convert_alpha() #Texture rouge constante de référence
		self.textureRouge = image.load("img/balleRouge.png").convert_alpha() #Texture rouge utilisée

	# Retourne si la balle est en collision avec une autre ou non
	def estEnCollisionAvec(self, balle):
		return not self.collisions.count(balle) == 0

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
	
	# Retourne la masse de la particule
	def getMasse(self):
		return self.masse
	
	# Retourne la valeur du rayon du cercle
	def getRayon(self):
		return self.rayon
	
	# Retourne la valeur de rouge
	def getRouge(self):
		return self.rouge
	
	# Retourne la texture à utiliser
	def getTexture(self):
		return self.texture
	
	# Retourne l'attribut x
	def getX(self):
		return self.x
	
	# Retourne l'attribut y
	def getY(self):
		return self.y
	
	# Retourne l'attribut z (toujours 100)
	def getZ(self):
		return 100
	
	# Changer l'attribut x, y et z
	def move(self, x, y):
		self.setX(x)
		self.setY(y)

	# Permet de rajouter une balle avec laquelle celle la rentre en collision
	def rajouterCollision(self, balle):
		if self.collisions.count(balle) == 0:
			self.collisions.append(balle)

	# Permet de redimensionner la texture selon le rayon et l'attribut z du cercle
	def redimensionnerTexture(self):
		if (self.getRayon() * 2) / self.TEXTURE.get_width() != 1:
			self.texture = transform.scale_by(self.TEXTURE, ((self.getRayon() * 2) / self.TEXTURE.get_width(), (self.getRayon() * 2) / self.TEXTURE.get_height()))

			if self.getRouge():
				self.textureRouge = transform.scale_by(self.TEXTUREROUGE, ((self.getRayon() * 2) / self.TEXTUREROUGE.get_width(), (self.getRayon() * 2) / self.TEXTUREROUGE.get_height()))

		if self.getRouge():
			self.texture.blit(self.textureRouge, (0, 0, self.textureRouge.get_width(), self.textureRouge.get_height()))
	
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

	# Change la valeur de rouge
	def setRouge(self, rouge):
		if self.getRouge() != rouge:
			self.rouge = rouge
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
	
	# Permet de vérifier si toutes les collisions sont toujours bonnes ou non
	def verifierCollisions(self):
		for i in self.collisions:
			if not self.touche(i):
				self.collisions.remove(i)

# Création de la classe du moteur de jeu
# La classe héritant de MImage, elle affiche l'image de font
class Game(MImage):

	# Constructeur du moteur de jeu
	def __init__(self, x, y, parent, widgetType="MImage"):
		super().__init__('img/fond.jpg', x, y, TAILLE[0], TAILLE[1], parent, widgetType)

		# Configurer l'arme utilisé
		self.armePosition = (0, 0) #Position de l'arme
		self.armeTexture = 0 #Surface qui contient la texture de l'arme
		self.armeType = "glock48" #Type de l'arme utilisé
		self.munitionTexture = 0 #Surface qui contient la texture d'une munition de l'arme
		self.munitionTirees = [] #Liste de données sur les munitions tirées
		self.munitionVitesse = 0

		self.balles = [] #Liste qui contient toutes les balles du jeu

		self.chargerArme(self.armeType)

		self.setBackgroundColor((255, 178, 102))

		# Texte qui sera affiché au bas de la fenetre
		WHITE = pygame.Color(255, 255, 255)
		text = MText('Projet NSI', 490, 300, 100, 20, self)
		text.setBackgroundColor((0, 0, 0, 0))
		text.setFont('font/elite.ttf')
		text.setFontSize(16)
		text.setTextColor(WHITE)
		text.setTextVerticalAlignment(1)
		text.ignoreClick = True

	# Retourne si une balle est présente à une position
	def balleALaPosition(self, x, y, rayon = 0):
		for i in self.balles:
			if i.touchePoint(x, y, rayon):
				return i
		return 0

	# Charger l'arme à utiliser
	def chargerArme(self, arme):
		self.armeType = arme
		if self.armeType == "glock48": #Si l'arme est un glock 48
			self.armeTexture = image.load("img/glock48.png").convert_alpha() #Charger la texture de l'arme
			self.munitionTexture = image.load("img/glock48Munition.png").convert_alpha() #Charger la texture d'une munition
			self.munitionVitesse = 2000 #Charger la vitesse d'une munition

		self.setShouldModify(True)

	# Créer nombre balle
	def creerBalle(self, nombre):
		for i in range(nombre):
			# Coordonnees et force de la POSITION initiale de la nouvelle balle (générees aléatoirement)
			fx = (500 * random()) - 250
			fy = (500 * random()) - 250
			x = random()*(largeur-Balle.BALLE_RAYON)
			y = random()*(hauteur-Balle.BALLE_RAYON)

			while self.balleALaPosition(x, y, 50) != 0:
				x = random()*(largeur-Balle.BALLE_RAYON)
				y = random()*(hauteur-Balle.BALLE_RAYON)

			balle = Balle(25, x, y, self)
			balle.setDX(fx)
			balle.setDY(fy)
			self.balles.append(balle)

	# Simule une frame physique
	def framePhysique(self, deltaTime):
		#Simuler la physique des munitions
		for i in self.munitionTirees:
			if i["profondeur"] > 200: #Supprimer si la balle est trop éloignée
				self.munitionTirees.remove(i)
			i["profondeur"] += i["vitesse"] * deltaTime #Calculer la profondeur (coordonnée X) de la balle

		#Simuler la physique des balles
		for index in range(len(self.balles)):
			i = self.balles[index]

			ancienX = i.getX()
			ancienY = i.getY()

			nouveauX = ancienX + i.getDX() * deltaTime
			nouveauY = ancienY + i.getDY() * deltaTime

			i.move(nouveauX, nouveauY)


			if self.getCalculerCollision(): #Si on calcule les collisions (pour l'instant pas optionnel)
				# On calcule les collisions (élastique) avec les autres balles
				for j in self.balles[index + 1:]:
					i.verifierCollisions()
					if i.touche(j) and not i.estEnCollisionAvec(j): #Si il y a collision et qu'elle n'as pas été encore traitée
						i.rajouterCollision(j) #On signala à la balle qu'une collision est en train d'avoir lieu
						j.rajouterCollision(i)

						#Calcul de l'énergie final
						v = (j.getDX() - i.getDX(), j.getDY() - i.getDY())

						#Normalisation de v pour que la norme de v soit égal à la somme de celle de dv1 et dv2
						sommeVAttendu = abs(i.getDX()) + abs(i.getDY()) + abs(j.getDX()) + abs(j.getDY())
						if abs(v[0]) + abs(v[1]) != sommeVAttendu:
							ratioManquant = (sommeVAttendu / (abs(v[0]) + abs(v[1])))
							if abs(v[0]) > abs(v[1]):
								ratioV = abs(v[1])/abs(v[0])
								if ratioV == 0: ratioV = 0.0000001
								v = (v[0] * (ratioManquant * ratioV), v[1] * (ratioManquant * (1 / ratioV)))
							else:
								ratioV = abs(v[0])/abs(v[1])
								if ratioV == 0: ratioV = 0.0000001
								v = (v[0] * (ratioManquant * (1 / ratioV)), v[1] * (ratioManquant * ratioV))

						v1 = (j.getMasse()/(i.getMasse()+j.getMasse())*v[0], j.getMasse()/(i.getMasse()+j.getMasse())*v[1])
						v2 = ((-j.getMasse())/(i.getMasse()+j.getMasse())*v[0], (-j.getMasse())/(i.getMasse()+j.getMasse())*v[1])

						# Mise à jour des vitesses des 2 balles
						i.setDX(v1[0])
						i.setDY(v1[1])

						j.setDX(v2[0])
						j.setDY(v2[1])

			# On prend en compte les rebonds avec le bord
			if nouveauX < self.rectFenetreDeJeu()[0]:
				nouveauX = self.rectFenetreDeJeu()[0]
				i.setDX(-i.getDX())
			elif nouveauX > self.rectFenetreDeJeu()[2] - i.getTexture().get_width():
				nouveauX = self.rectFenetreDeJeu()[2] - i.getTexture().get_width()
				i.setDX(-i.getDX())

			if nouveauY < self.rectFenetreDeJeu()[1]:
				nouveauY = self.rectFenetreDeJeu()[1]
				i.setDY(-i.getDY())
			elif nouveauY > self.rectFenetreDeJeu()[3] - i.getTexture().get_height():
				nouveauY = self.rectFenetreDeJeu()[3] - i.getTexture().get_height()
				i.setDY(-i.getDY())

			i.move(nouveauX, nouveauY)

		i, j = 0, 0
		while i < len(self.balles): #Vérifier si une balle touche une munition
			while j < len(self.munitionTirees):
				xMunition = self.munitionTirees[j]["pos"][0] + self.armeTexture.get_width() / 2
				yMunition = self.munitionTirees[j]["pos"][1] - (self.armeTexture.get_height() / 2 + 10)

				if distance2D(self.balles[i].getX() + self.balles[i].getRayon(), self.balles[i].getY() + self.balles[i].getRayon(), xMunition, yMunition) <= self.balles[i].getRayon():
					self.balles.remove(self.balles[i])
					self.munitionTirees.remove(self.munitionTirees[j])
					i -= 1
					j -= 1
				j += 1
			i += 1
			j = 0

		self.setShouldModify(True)

	# Retourne si les collisiosn entre balles sont comptées ou pas
	def getCalculerCollision(self):
		return False
	
	# Retourne les coordonée/taille de la fenêtre de jeu
	def rectFenetreDeJeu(self):
		return (0, 0, self.getWidth(), self.imageSize[1])

	# Fonction appelé lorsqu'une touche du clavier est pressée
	def _isKeyGettingPressed(self, key):
		if key == pygame.K_RIGHT:
			self.framePhysique(0.01)

	# Fonction appelée lorsqu'une touche de la souris est clické
	def _isGettingMouseDown(self, button, relativePos):
		if button == 1: #Si la touche gauche de la souris est clické
			self.munitionTirees.append({"pos": (relativePos[0], relativePos[1]), "profondeur": 1, "vitesse": self.munitionVitesse})

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

		#Dessiner les munitions
		for i in self.munitionTirees:
			surfaceABlit = self.munitionTexture
			coefficientRetrecissement = (200 - i["profondeur"])/200
			if coefficientRetrecissement < 0: coefficientRetrecissement = 0

			if coefficientRetrecissement != 1 and coefficientRetrecissement != 0: #Calculer l'éloignement de la munition
				surfaceABlit = transform.scale_by(surfaceABlit, (coefficientRetrecissement, coefficientRetrecissement))

			if coefficientRetrecissement != 0:
				xMunition = i["pos"][0] - self.armeTexture.get_width() / 2 + (self.armeTexture.get_width() - surfaceABlit.get_width()) / 2
				yMunition = i["pos"][1] - self.armeTexture.get_height() / 2 - 10
				surface.blit(surfaceABlit, (xMunition, yMunition, surfaceABlit.get_width(), surfaceABlit.get_height()))

		#Dessiner l'arme
		surface.blit(self.armeTexture, (self.armePosition[0], self.armePosition[1], self.armeTexture.get_width(), self.armeTexture.get_height()))

		return surface

	# Fonction appelée à chaque frames par mapp avec deltaTime le temps qu'a duré la dernière frame
	def _update(self, deltaTime):
		self.framePhysique(deltaTime)


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
