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
mapp = MApp(screen, "Jeu", TAILLE[0], TAILLE[1], console=False, printFps=True)

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

# Création de la classe de l'arme
class Arme:

	# Constructeur d'un objet arme
	def __init__(self, cadenceDeTir, chargeur, semiAutomatique, tempsDeRechargement, texture, type, munitionTexture, munitionVitesse) -> None:
		self.cadenceDeTir = cadenceDeTir #Cadence de tir de l'arme
		self.chargeur = chargeur #Nombre de munitions possible dans le chargeur
		self.chargeurRestant = chargeur #Nombre du munitions restantes dans le chargeur
		self.debutRechargement = 0 #Temps où l'arme à commencer à se recharger
		self.munitionTexture = munitionTexture #Texture d'une munition de l'arme
		self.munitionVitesse = munitionVitesse #Vitesse d'une munition del'arme
		self.semiAutomatique = semiAutomatique #Booléen qui indique si l'arme est semi automatique ou non
		self.seRecharge = False #Booléen qui indique si l'arme est en plein rechargement ou pas
		self.tempsDeRechargement = tempsDeRechargement #Temps de rechargement de l'arme
		self.texture = texture #Texture de l'arme
		self.type = type #Type de l'arme

	# Charge l'arme
	def debuterChargement(self):
		if self.getChargeurRestant() < self.getChargeur() and not self.enChargement():
			self.debutRechargement = time_ns()
			self.seRecharge = True

	# Retourne si l'arme est en plein rechargement ou pas
	def enChargement(self): return self.seRecharge

	# Finir (ou pas) le chargement de l'arme
	def finirChargement(self):
		if (time_ns() - self.debutRechargement)/(10**9) >= self.getTempsDeChargement():
			self.chargeurRestant = self.chargeur
			self.debutRechargement = 0
			self.seRecharge = False
			return 0
		return self.getTempsDeChargement() - (time_ns() - self.debutRechargement)/(10**9)
	
	# Retourne cadenceDeTir
	def getCadenceDeTir(self): return self.cadenceDeTir

	# Retourne chargeur
	def getChargeur(self): return self.chargeur

	# Retourne chargeurRestant
	def getChargeurRestant(self): return self.chargeurRestant

	# Retourne munitionTexture
	def getMunitionTexture(self): return self.munitionTexture

	# Retourne munitionVitesse
	def getMunitionVitesse(self): return self.munitionVitesse

	# Retourne semiAutomatique
	def getSemiAutomatique(self): return self.semiAutomatique

	# Retourne tempsDeRechargement
	def getTempsDeChargement(self): return self.tempsDeRechargement

	# Retourne texture
	def getTexture(self): return self.texture

	# Retourne type
	def getType(self): return self.type

	# Reset l'arme
	def reset(self):
		self.chargeurRestant = self.chargeur
		self.debutRechargement = 0
		self.seRecharge = False

	# Tire avec l'arme
	def tirer(self):
		if self.getChargeurRestant() > 0:
			self.chargeurRestant -= 1
			return True
		return False

# Création de la classe du moteur de jeu
# La classe héritant de MImage, elle affiche l'image de font
class Game(MImage):

	# Constructeur du moteur de jeu
	def __init__(self, typeArme, x, y, parent, widgetType="MImage"):
		super().__init__('img/fond.jpg', x, y, TAILLE[0], TAILLE[1], parent, widgetType)

		self.armes = {} #Dictionnaire qui contient tous les types d'armes
		self.armeActuel = 0 #Contient l'arme actuelle
		self.armePosition = (0, 0) #Position de l'arme dans la fenêtre
		self.creerArme() #Créer tous les objets armes
		self.croixDeVisee = True #Booléen qui indique si une croix de visée est affichée ou non
		self.explosion = [] #Liste des propriétés des explosions dans le jeu
		self.explosionDuree = 0.2 #Durée d'une explosion (en secondes)
		self.explosionTexture = image.load("img/explosion.png") #Texture d'une explosion
		self.munitionTirees = [] #Liste des propriétés des munitions tirées
		self.nbTir = 0 #Nombre de tir total
		self.nbTirReussie = 0 #Nombre de tir réussie
		self.tempsDuDernierTir = 0 #Temps au moment du dernier tir

		self.balles = [] #Liste qui contient toutes les balles du jeu
		self.nbBalleDetruite = 0 #Nombre de balles détruites

		self.calculerCollision = True #Booléen qui indique si on calcule les collisions ou non

		self.fini = False #Booléen qui indique si le jeu est fini
		self.timecodeDebut = time_ns() #Temps au début du jeu
		self.timecodeFin = -1 #Temps à la fin du jeu, ou -1 si le jeu n'est pas fini

		self._isClicked = False #Booléen qui indique si la souris est en train de clicker sur le moteur de jeu
		self._positionSourisActuel = (0, 0) #Position actuel de la souris

		# Texte qui affichera la capacité du chargeur
		WHITE = pygame.Color(255, 255, 255)
		text = MText('0/0', 0, 300, 100, 20, self)
		text.setBackgroundColor((0, 0, 0, 0))
		text.setFont('font/elite.ttf')
		text.setFontSize(16)
		text.setTextColor(WHITE)
		text.setTextVerticalAlignment(1)
		text.ignoreClick = True
		self.armeChargeurTexte = text

		# Chronomètre qui sera affiché en haut à gauche de la fenêtre
		WHITE = pygame.Color(255, 255, 255)
		text = MText('0.0', 0, 0, 100, 20, self)
		text.setBackgroundColor((0, 0, 0, 0))
		#text.setFont('font/elite.ttf')
		text.setFontSize(22)
		text.setTextColor(WHITE)
		text.setTextHorizontalAlignment(1)
		text.setTextVerticalAlignment(1)
		text.ignoreClick = True
		self.chronometre = text

		# Texte qui sera affiché en bas à droite de la fenêtre
		WHITE = pygame.Color(255, 255, 255)
		text = MText('Projet NSI', 490, 300, 100, 20, self)
		text.setBackgroundColor((0, 0, 0, 0))
		text.setFont('font/elite.ttf')
		text.setFontSize(16)
		text.setTextColor(WHITE)
		text.setTextVerticalAlignment(1)
		text.ignoreClick = True
		self.textePub = text

		# Texte qui affichera le déroulé du rechargement
		WHITE = pygame.Color(255, 255, 255)
		text = MText('Rechargement...\n0.0', 0, 0, 150, 40, self)
		text.setBackgroundColor((0, 0, 0, 0))
		text.setFontSize(22)
		text.setTextColor(WHITE)
		text.setTextHorizontalAlignment(1)
		text.setTextVerticalAlignment(1)
		text.setVisible(False)
		text.ignoreClick = True
		self.texteRechargement = text
  
		self.chargerArme(typeArme)

		self.setBackgroundColor((255, 178, 102))

	# Retourne si une balle est présente à une position
	def balleALaPosition(self, x, y, rayon = 0):
		for i in self.balles:
			if i.touchePoint(x, y, rayon):
				return i
		return 0
	
	# Change le texte du chargeur (en bas à gauche)
	def changerArmeChargeurTexte(self):
		aSupprimer = 255 * (self.armeActuel.getChargeurRestant() / self.armeActuel.getChargeur()) #Valeur à supprimer pour tendre vers le rouge
		self.armeChargeurTexte.setTextColor((255, aSupprimer, aSupprimer))
		self.armeChargeurTexte.setText(str(self.armeActuel.getChargeurRestant()) + "/" + str(self.armeActuel.getChargeur()))

	# Charger l'arme à utiliser
	def chargerArme(self, arme):
		if self.armeActuel != 0: #Reset l'ancienne arme
			self.armeActuel.reset()

		self.armeActuel = self.armes[arme]
		self.changerArmeChargeurTexte()

		self.setShouldModify(True)

	# Créer toutes les armes built-in
	def creerArme(self):
		ar15 = Arme(6, 30, True, 5, image.load("img/ar15.png").convert_alpha(), "ar15", image.load("img/ar15Munition.png").convert_alpha(), 1500) #Création de l'ar15
		glock48 = Arme(0, 16, False, 3, image.load("img/glock48.png").convert_alpha(), "glock48", image.load("img/glock48Munition.png").convert_alpha(), 2000) #Création du glock48
		lanceRoquette = Arme(0, 1, False, 8, image.load("img/lanceRoquette.png"), "lanceRoquette", image.load("img/lanceRoquetteMunition.png"), 200)

		self.armes["ar15"] = ar15
		self.armes["glock48"] = glock48
		self.armes["lanceRoquette"] = lanceRoquette

	# Créer nombre balle
	def creerBalle(self, nombre):
		for i in range(nombre):
			# Coordonnees et force de la POSITION initiale de la nouvelle balle (générees aléatoirement)
			fx = (500 * random()) - 250
			fy = (500 * random()) - 250
			x = random()*(largeur-Balle.BALLE_RAYON)
			y = random()*(hauteur-Balle.BALLE_RAYON)

			while self.balleALaPosition(x, y, 50) != 0 and self.getCalculerCollision():
				x = random()*(largeur-Balle.BALLE_RAYON)
				y = random()*(hauteur-Balle.BALLE_RAYON)

			balle = Balle(25, x, y, self)
			balle.setDX(fx)
			balle.setDY(fy)
			self.balles.append(balle)

	# Retourne les données de fin de jeu
	def donneesFinDeJeu(self):
		return {"nbBalleDetruite": self.nbBalleDetruite, "temps": (self.timecodeFin - self.timecodeDebut) / 10 ** 9, "nbTir": self.nbTir, "nbTirReussie": self.nbTirReussie}

	# Fini le jeu
	def fin(self):
		self.fini = True
		self.timecodeFin = time_ns()

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

			if self.getCalculerCollision() and len(self.balles) == 2: #Si on calcule les collisions
				#Données relatives des 2 balles
				balle1 = self.balles[0]
				balle2 = self.balles[1]
				distance = distance2D(balle1.getX(), balle1.getY(), balle2.getX(), balle2.getY())
				
				#On calcule les collisions (élastique) avec les autres balles
				if balle1.touche(balle2): #Si il y a collision
					v1 = (balle1.getDX(), balle1.getDY())
					v2 = (balle2.getDX(), balle2.getDY())
					n = ((balle1.getX() - balle2.getX()) / distance, (balle1.getY() - balle2.getY()) / distance)

					w1 = (v1[0] - ((v1[0] - v2[0]) * n[0] + (v1[1] - v2[1]) * n[1]) * n[0] , v1[1] - ((v1[0] - v2[0]) * n[0] + (v1[1] - v2[1]) * n[1]) * n[1] )
					w2 = (v2[0] - ((v2[0] - v1[0]) * n[0] + (v2[1] - v1[1]) * n[1]) * n[0] , v2[1] - ((v2[0] - v1[0]) * n[0] + (v2[1] - v1[1]) * n[1]) * n[1] )

					# Mise à jour des vitesses des 2 balles
					balle1.setDX(w1[0])
					balle1.setDY(w1[1])

					balle2.setDX(w2[0])
					balle2.setDY(w2[1])

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
				xMunition = self.munitionTirees[j]["pos"][0] + self.armeActuel.getTexture().get_width() / 2
				yMunition = self.munitionTirees[j]["pos"][1] - (self.armeActuel.getTexture().get_height() / 2 + 10)

				if self.munitionTirees[j]["profondeur"] >= 100: #Si la munition est assez éloignée
					#Si la munition touche une balle
					if distance2D(self.balles[i].getX() + self.balles[i].getRayon(), self.balles[i].getY() + self.balles[i].getRayon(), xMunition, yMunition) <= self.balles[i].getRayon():
						self.balles.remove(self.balles[i]) #SUpprimer la munition et la balle touchée
						self.munitionTirees.remove(self.munitionTirees[j])
						self.nbBalleDetruite += 1
						self.nbTirReussie += 1
						i -= 1
						j -= 1
						if self.armeActuel.getType() == "lanceRoquette": #Si la munition tirées est une roquette
							self.explosion.append({"pos": (xMunition, yMunition), "debut": time_ns()})
							k = 0
							while k < len(self.balles):
								#Si la munition est à moins de 150 unités de l'explosion
								if distance2D(self.balles[k].getX() + self.balles[k].getRayon(), self.balles[k].getY() + self.balles[k].getRayon(), xMunition, yMunition) <= 150:
									self.balles.remove(self.balles[k]) #Supprimer les balles proches
									self.nbBalleDetruite += 1
									if k <= i:
										i -= 1
									k -= 1
								k += 1
				j += 1
			i += 1
			j = 0

		self.setShouldModify(True)

	# Retourne si les collisions entre balles sont comptées ou pas
	def getCalculerCollision(self):
		return self.calculerCollision
	
	# Retourne croixDeVisee
	def getCroixDeVisee(self): return self.croixDeVisee
	
	# Retourne les coordonée/taille de la fenêtre de jeu
	def rectFenetreDeJeu(self):
		return (0, 0, self.getWidth(), self.imageSize[1])

	# Change la valeur de croixDeVisee
	def setCroixDeVisee(self, croixDeVisee):
		self.croixDeVisee = croixDeVisee

	# Retourne le temps depuis qu'il n'y a plus de balles dans le jeu
	def tempsDepuisFin(self):
		if len(self.balles) == 0:
			if self.timecodeFin != -1:
				return (time_ns() - self.timecodeFin) / 10 ** 9
			else:
				self.fin()
				return 0
		else: return -1 #Si il y a encore des balles, retourne -1

	# Tire avec l'arme
	def tirer(self, relativePos):
		if self.armeActuel.tirer():
			self.munitionTirees.append({"pos": (relativePos[0], relativePos[1]), "profondeur": 1, "vitesse": self.armeActuel.getMunitionVitesse()})
			self.nbTir += 1
			self.tempsDuDernierTir = time_ns()

			self.changerArmeChargeurTexte()

	# Fonction appelé lorsqu'une touche du clavier est pressée
	def _isKeyGettingPressed(self, key):
		if key == pygame.K_RIGHT:
			self.framePhysique(0.01)
		elif key == pygame.K_r and not self.fini:
			self.armeActuel.debuterChargement()
			self.texteRechargement.setText("Rechargement\n" + str(round(self.armeActuel.getTempsDeChargement(), 1)))
			self.texteRechargement.setVisible(True)

	# Fonction appelée lorsqu'une touche de la souris est clické
	def _isGettingMouseDown(self, button, relativePos):
		if button == 1 and not self.fini: #Si la touche gauche de la souris est clické
			self.tirer(relativePos)
			self._isClicked = True

	# Fonction appelée lorsqu'une touche de la soruis n'est plus clické
	def _isGettingMouseUp(self, button, relativePos):
		if button == 1:
			self._isClicked = False

	# Fonction utilisé quand la souris est bougé sur la zone de jeu
	def _mouseMove(self, buttons, pos, relativeMove):
		self.armePosition = (round(pos[0] - self.armeActuel.getTexture().get_width() / 2), round(pos[1] - self.armeActuel.getTexture().get_height() / 2))
		self._positionSourisActuel = pos
		self.texteRechargement.move(round(pos[0] - self.texteRechargement.getWidth() / 2), round(pos[1] - (self.texteRechargement.getHeight() / 2 + 20)))

	# Dessine sur la surface de jeu
	def _renderBeforeHierarchy(self, surface):
		surface = super()._renderBeforeHierarchy(surface)

		#Dessiner les balles
		for i in self.balles:
			surfaceABlit = i.getTexture()

			surface.blit(surfaceABlit, (i.getX(), i.getY(), surfaceABlit.get_width(), surfaceABlit.get_height()))

		#Dessiner les explosions
		for i in self.explosion:
			ratio = ((time_ns() - i["debut"])/(10**9)) / (self.explosionDuree)
			ratioTaille = 200/self.explosionTexture.get_width()
			surfaceABlit = self.explosionTexture
			surfaceABlit = transform.scale_by(surfaceABlit, (ratio * ratioTaille, ratio * ratioTaille)) #Calculer la taille de l'explosion
			surfaceABlit.set_alpha((1 - ratio) * 255)

			surface.blit(surfaceABlit, (i["pos"][0] - surfaceABlit.get_width() / 2, i["pos"][1] - surfaceABlit.get_height() / 2, surfaceABlit.get_width(), surfaceABlit.get_height()))

		#Dessiner les munitions
		for i in self.munitionTirees:
			surfaceABlit = self.armeActuel.getMunitionTexture()
			coefficientRetrecissement = (200 - i["profondeur"])/200
			if coefficientRetrecissement < 0: coefficientRetrecissement = 0

			if coefficientRetrecissement != 1 and coefficientRetrecissement != 0: #Calculer l'éloignement de la munition
				surfaceABlit = transform.scale_by(surfaceABlit, (coefficientRetrecissement, coefficientRetrecissement))

			if coefficientRetrecissement != 0:
				xMunition = i["pos"][0] - self.armeActuel.getTexture().get_width() / 2 + (self.armeActuel.getTexture().get_width() - surfaceABlit.get_width()) / 2
				yMunition = i["pos"][1] - self.armeActuel.getTexture().get_height() / 2 - 10
				surface.blit(surfaceABlit, (xMunition, yMunition, surfaceABlit.get_width(), surfaceABlit.get_height()))

		#Dessiner la croix de visée
		if self.getCroixDeVisee():
			croixLargeur = 2
			croixLongeur = 15
			#Ligne horizontal
			draw.line(surface, (255, 255, 255), ((self.armePosition[0] + self.armeActuel.getTexture().get_width() / 2 - croixLongeur), (self.armePosition[1] - croixLongeur/4)), ((self.armePosition[0] + self.armeActuel.getTexture().get_width() / 2 + croixLongeur), (self.armePosition[1] - croixLongeur/4)), croixLargeur)
			#Ligne vertical
			draw.line(surface, (255, 255, 255), ((self.armePosition[0] + self.armeActuel.getTexture().get_width() / 2), (self.armePosition[1]) + croixLongeur/4), ((self.armePosition[0] + self.armeActuel.getTexture().get_width() / 2), (self.armePosition[1] - (5/4)*croixLongeur)), croixLargeur)

		#Dessiner l'arme
		surface.blit(self.armeActuel.getTexture(), (self.armePosition[0], self.armePosition[1], self.armeActuel.getTexture().get_width(), self.armeActuel.getTexture().get_height()))

		return surface

	# Fonction appelée à chaque frames par mapp avec deltaTime le temps qu'a duré la dernière frame
	def _update(self, deltaTime):
		if not self.fini: #Si le jeu n'est pas fini
			secondes = (time_ns() - self.timecodeDebut)/10**9 #Gérer le chronomètre
			minute = 0
			while secondes > 60:
				secondes -= 60
				minute += 1
			chrono = str(round(secondes, 1)) #Texte du chronomètre
			if minute != 0: chrono = str(round(minute)) + ":" + str(round(secondes, 1))
			self.chronometre.setText(chrono)

			i = 0
			while i < len(self.explosion): #Gérer les explosions
				e = self.explosion[i]
				if ((time_ns() - e["debut"])/(10**9)) >= self.explosionDuree: #Si une explosions est fini
					self.explosion.remove(e) #Supprimer l'explosions
					del e
					i -= 1
				i += 1

			self.framePhysique(deltaTime)

			if self.armeActuel.enChargement(): #Gérer le rechargement de l'arme
				etat = self.armeActuel.finirChargement()
				if etat <= 0:
					self.changerArmeChargeurTexte()
					self.texteRechargement.setVisible(False)
				else:
					self.texteRechargement.setText("Rechargement\n" + str(round(etat, 1)))

			if self.armeActuel.getSemiAutomatique() and self._isClicked: #Gérer le tir des armes semi automatique
				if (time_ns() - self.tempsDuDernierTir)/(10**9) >= 1/self.armeActuel.getCadenceDeTir():
					self.tirer(self._positionSourisActuel)


# Création de la partie graphique de la page d'accueil
accueil = MWidget(0, 0, TAILLE[0], TAILLE[1], mapp)
titreAccueil = MText("Jeu", 200, 20, TAILLE[0] - 400, 150, accueil)
boutonJouerAccueil = MButton("Jouer", 25, TAILLE[1] - 100, 275, 70, accueil)
boutonCommentJouerAccueil = MButton("Comment jouer", TAILLE[0] - 300, TAILLE[1] - 100, 275, 70, accueil)
commentJouer = MWidget(0, 0, TAILLE[0], TAILLE[1], accueil)
imageCommentJouer = MImage("img/commentJouerGameplay.png", 0, 45, commentJouer.getWidth(), commentJouer.getHeight() - 45, commentJouer)
armeCommentJouer = MButton("Armes", 280, 5, 100, 30, commentJouer)
gameplayCommentJouer = MButton("Gameplay", 120, 5, 150, 30, commentJouer)
retourCommentJouer = MButton("Retour", 10, 5, 100, 30, commentJouer)

# Création de la partie graphique de la page d'option de jeu
optionDeJeu = MWidget(0, 0, TAILLE[0], TAILLE[1], mapp)
titreOptionDeJeu = MText("Options", 200, 0, TAILLE[0] - 400, 100, optionDeJeu)
boutonJouerOptionDeJeu = MButton("Jouer", 50, TAILLE[1] - 100, 200, 70, optionDeJeu)
boutonRetourOptionDeJeu = MButton("Retour", TAILLE[0] - 250, TAILLE[1] - 100, 200, 70, optionDeJeu)
titreArmeOptionDeJeu = MText("Arme", TAILLE[0] - 250, titreOptionDeJeu.getHeight() + 15, 200, 40, optionDeJeu)
ar15ArmeOptionDeJeu = MButton("Ar 15", TAILLE[0] - 250, titreArmeOptionDeJeu.getY() + titreArmeOptionDeJeu.getHeight() + 5, 200, 30, optionDeJeu)
glock48ArmeOptionDeJeu = MButton("Glock 48", TAILLE[0] - 250, ar15ArmeOptionDeJeu.getY() + ar15ArmeOptionDeJeu.getHeight() + 5, 200, 30, optionDeJeu)
lanceRoquetteArmeOptionDeJeu = MButton("Lance roquette", TAILLE[0] - 250, glock48ArmeOptionDeJeu.getY() + glock48ArmeOptionDeJeu.getHeight() + 5, 200, 30, optionDeJeu)
titreNombreDeBalleOptionDeJeu = MText("Nombre de balle", 50, titreOptionDeJeu.getHeight() + 15, 200, 40, optionDeJeu)
texteNombreDeBalleOptionDeJeu = MText("25", 50, titreNombreDeBalleOptionDeJeu.getY() + titreNombreDeBalleOptionDeJeu.getHeight() + 15, 200, 40, optionDeJeu)
erreurNombreDeBalleOptionDeJeu = MText("Veuillez n'entrer que des nombres.", 50, texteNombreDeBalleOptionDeJeu.getY() + texteNombreDeBalleOptionDeJeu.getHeight(), 200, 60, optionDeJeu)

# Création de la partie graphique de la page de fin
fin = MWidget(0, 0, TAILLE[0], TAILLE[1], mapp)
titreFin = MText("Fin du jeu", 100, 20, TAILLE[0] - 200, 100, fin)
boutonRejouerFin = MButton("Rejouer", 50, TAILLE[1] - 100, 200, 70, fin)
boutonQuitterFin = MButton("Quitter", TAILLE[0] - 250, TAILLE[1] - 100, 200, 70, fin)
texteBalleDetruiteFin = MText("Balle(s) détruite(s) : 0", 20, 130, 250, 20, fin)
texteTirFin = MText("Tir(s) : 0", TAILLE[0] - 270, 130, 250, 20, fin)
texteTirReussieFin = MText("Tir(s) réussi(s) : 0%", 20, 160, 250, 20, fin)
texteTempsFin = MText("0.0 s", TAILLE[0] - 270, 160, 250, 20, fin)

# Modification des éléments graphiques (voir documentation mlib documentation.html)
accueil.setBackgroundColor((102, 102, 255))
accueil.setVisible(False)

titreAccueil.setAntiAnaliasing(True)
titreAccueil.setBackgroundColor((255, 255, 255, 30))
titreAccueil.setCornerRadius(25)
titreAccueil.setFontSize(75)
titreAccueil.setFrameWidth(3)
titreAccueil.setTextHorizontalAlignment(1)
titreAccueil.setTextVerticalAlignment(1)

boutonJouerAccueil.setAntiAnaliasing(True)
boutonJouerAccueil.setChangeFontSizeOnOnOverflight(True)
boutonJouerAccueil.setCornerRadius(25)
boutonJouerAccueil.setFontSize(35)
boutonJouerAccueil.setFontSizeOnOverflight(45)

boutonCommentJouerAccueil.setAntiAnaliasing(True)
boutonCommentJouerAccueil.setChangeFontSizeOnOnOverflight(True)
boutonCommentJouerAccueil.setCornerRadius(25)
boutonCommentJouerAccueil.setFontSize(30)
boutonCommentJouerAccueil.setFontSizeOnOverflight(40)

commentJouer.setBackgroundColor((102, 102, 255))

armeCommentJouer.setAntiAnaliasing(True)
armeCommentJouer.setCornerRadius(15)
armeCommentJouer.setFontSize(22)

gameplayCommentJouer.setAntiAnaliasing(True)
gameplayCommentJouer.setCornerRadius(15)
gameplayCommentJouer.setFontSize(22)

retourCommentJouer.setAntiAnaliasing(True)
retourCommentJouer.setCornerRadius(15)
retourCommentJouer.setFontSize(22)

optionDeJeu.setBackgroundColor((102, 102, 255))
optionDeJeu.setVisible(False)

boutonJouerOptionDeJeu.setAntiAnaliasing(True)
boutonJouerOptionDeJeu.setChangeFontSizeOnOnOverflight(True)
boutonJouerOptionDeJeu.setCornerRadius(25)
boutonJouerOptionDeJeu.setFontSize(35)
boutonJouerOptionDeJeu.setFontSizeOnOverflight(45)

boutonRetourOptionDeJeu.setAntiAnaliasing(True)
boutonRetourOptionDeJeu.setChangeFontSizeOnOnOverflight(True)
boutonRetourOptionDeJeu.setCornerRadius(25)
boutonRetourOptionDeJeu.setFontSize(35)
boutonRetourOptionDeJeu.setFontSizeOnOverflight(45)

titreOptionDeJeu.setAntiAnaliasing(True)
titreOptionDeJeu.setBackgroundColor((255, 255, 255, 0))
titreOptionDeJeu.setFontSize(75)
titreOptionDeJeu.setTextHorizontalAlignment(1)
titreOptionDeJeu.setTextVerticalAlignment(1)

titreArmeOptionDeJeu.setBackgroundColor((255, 255, 255, 0))
titreArmeOptionDeJeu.setFontSize(22)
titreArmeOptionDeJeu.setTextHorizontalAlignment(1)
titreArmeOptionDeJeu.setTextVerticalAlignment(1)

glock48ArmeOptionDeJeu.setFrameColor((255, 0, 0))

titreNombreDeBalleOptionDeJeu.setBackgroundColor((255, 255, 255, 0))
titreNombreDeBalleOptionDeJeu.setFontSize(22)
titreNombreDeBalleOptionDeJeu.setTextHorizontalAlignment(1)
titreNombreDeBalleOptionDeJeu.setTextVerticalAlignment(1)

texteNombreDeBalleOptionDeJeu.setAntiAnaliasing(True)
texteNombreDeBalleOptionDeJeu.setBackgroundColor((255, 255, 255))
texteNombreDeBalleOptionDeJeu.setFontSize(22)
texteNombreDeBalleOptionDeJeu.setFrameWidth(2)
texteNombreDeBalleOptionDeJeu.setInput(True)
texteNombreDeBalleOptionDeJeu.setTextHorizontalAlignment(1)
texteNombreDeBalleOptionDeJeu.setTextVerticalAlignment(1)

erreurNombreDeBalleOptionDeJeu.setBackgroundColor((255, 255, 255, 0))
erreurNombreDeBalleOptionDeJeu.setDynamicTextCut(True)
erreurNombreDeBalleOptionDeJeu.setFontSize(22)
erreurNombreDeBalleOptionDeJeu.setTextColor((255, 0, 0))
erreurNombreDeBalleOptionDeJeu.setTextHorizontalAlignment(1)
erreurNombreDeBalleOptionDeJeu.setTextVerticalAlignment(1)
erreurNombreDeBalleOptionDeJeu.setVisible(False)

fin.setBackgroundColor((102, 102, 255))
fin.setVisible(False)

titreFin.setAntiAnaliasing(True)
titreFin.setBackgroundColor((255, 255, 255, 30))
titreFin.setCornerRadius(25)
titreFin.setFontSize(75)
titreFin.setFrameWidth(3)
titreFin.setTextHorizontalAlignment(1)
titreFin.setTextVerticalAlignment(1)

boutonRejouerFin.setAntiAnaliasing(True)
boutonRejouerFin.setChangeFontSizeOnOnOverflight(True)
boutonRejouerFin.setCornerRadius(25)
boutonRejouerFin.setFontSize(35)
boutonRejouerFin.setFontSizeOnOverflight(45)

boutonQuitterFin.setAntiAnaliasing(True)
boutonQuitterFin.setChangeFontSizeOnOnOverflight(True)
boutonQuitterFin.setCornerRadius(25)
boutonQuitterFin.setFontSize(35)
boutonQuitterFin.setFontSizeOnOverflight(45)

texteBalleDetruiteFin.setBackgroundColor((0, 0, 0, 0))
texteBalleDetruiteFin.setTextVerticalAlignment(1)
texteBalleDetruiteFin.setFontSize(22)

texteTirFin.setBackgroundColor((0, 0, 0, 0))
texteTirFin.setTextVerticalAlignment(1)
texteTirFin.setFontSize(22)

texteTirReussieFin.setBackgroundColor((0, 0, 0, 0))
texteTirReussieFin.setTextVerticalAlignment(1)
texteTirReussieFin.setFontSize(22)

texteTempsFin.setBackgroundColor((0, 0, 0, 0))
texteTempsFin.setTextVerticalAlignment(1)
texteTempsFin.setFontSize(22)

#  --------------------------------------------------------------------------
#      Boucle exécutée tant que MLib ne reçoit pas d'event "pygame.QUIT"
#  --------------------------------------------------------------------------

#Boucle du programme complet
while True:
	#  -----------------------------------------------------------------------------------------------------------------------------
	#      Boucle exécutée tant que MLib ne reçoit pas d'event "pygame.QUIT" ou que l'utilisateur ne quitte pas la page d'accueil
	#  -----------------------------------------------------------------------------------------------------------------------------

	accueil.setVisible(True)
	commentJouer.setVisible(False)
	ecranDAccueil = True
	imageCommentJouer.setImageLink("img/commentJouerGameplay.png")

	#Affichage de l'écran d'accueil
	while ecranDAccueil:
		# Actualiser les évènements pygame et MLib
		mapp.frameEvent()

		if boutonCommentJouerAccueil.isGettingLeftClicked(): #Afficher la page de comment jouer
			commentJouer.setVisible(True)

		if boutonJouerAccueil.isGettingLeftClicked(): #Lancer le jeu
			ecranDAccueil = False

		if armeCommentJouer.isGettingLeftClicked(): #Mettre la section "arme" de la page "comment jouer"
			imageCommentJouer.setImageLink("img/commentJouerArme.png")

		if gameplayCommentJouer.isGettingLeftClicked(): #Mettre la section "gameplay" de la page "comment jouer"
			imageCommentJouer.setImageLink("img/commentJouerGameplay.png")

		if retourCommentJouer.isGettingLeftClicked(): #Remettre la page d'accueil
			commentJouer.setVisible(False)
					
		# Actualisater l'affichage graphique MLib et afficher de l'image
		mapp.frameGraphics()
		pygame.display.update()

	accueil.setVisible(False)

	#  -----------------------------------------------------------------------------------------------------------------------------
	#                              Fin de la première boucle 
	#  -----------------------------------------------------------------------------------------------------------------------------

	#  -----------------------------------------------------------------------------------------------------------------------------
	#      Boucle exécutée tant que MLib ne reçoit pas d'event "pygame.QUIT" ou que l'utilisateur ne quitte pas la page d'options
	#  -----------------------------------------------------------------------------------------------------------------------------

	optionDeJeu.setVisible(True)
	ecranOption = True
	nombreBalle = ""
	retour = False
	typeArme = "glock48"

	#Affichage de l'écran d'option
	while ecranOption:
		# Actualiser les évènements pygame et MLib
		mapp.frameEvent()

		nombreBalle = texteNombreDeBalleOptionDeJeu.getText()
		nombreSeulement = True
		for i in nombreBalle: #Si seulement des chiffres on été rentrés par l'utilisateur
			if "0123456789".count(i) <= 0:
				nombreSeulement = False
				break

		erreurNombreDeBalleOptionDeJeu.setVisible(not nombreSeulement) #Afficher ou pas une erreur au texte de l'entrée de balle

		if ar15ArmeOptionDeJeu.isGettingLeftClicked(): #Permettre de sélectionner un type d'arme
			ar15ArmeOptionDeJeu.setFrameColor((255, 0, 0))
			glock48ArmeOptionDeJeu.setFrameColor((0, 0, 0))
			lanceRoquetteArmeOptionDeJeu.setFrameColor((0, 0, 0))

			typeArme = "ar15"
		elif glock48ArmeOptionDeJeu.isGettingLeftClicked():
			ar15ArmeOptionDeJeu.setFrameColor((0, 0, 0))
			glock48ArmeOptionDeJeu.setFrameColor((255, 0, 0))
			lanceRoquetteArmeOptionDeJeu.setFrameColor((0, 0, 0))

			typeArme = "glock48"
		elif lanceRoquetteArmeOptionDeJeu.isGettingLeftClicked():
			ar15ArmeOptionDeJeu.setFrameColor((0, 0, 0))
			glock48ArmeOptionDeJeu.setFrameColor((0, 0, 0))
			lanceRoquetteArmeOptionDeJeu.setFrameColor((255, 0, 0))

			typeArme = "lanceRoquette"

		if boutonJouerOptionDeJeu.isGettingLeftClicked() and nombreSeulement and nombreBalle != "" and int(nombreBalle) > 0: #Lancer le jeu
			ecranOption = False

		if boutonRetourOptionDeJeu.isGettingLeftClicked(): #Retourner à l'écran d'accueil
			ecranOption = False
			retour = True
					
		# Actualisater l'affichage graphique MLib et afficher de l'image
		mapp.frameGraphics()
		pygame.display.update()

	optionDeJeu.setVisible(False)

	if retour: continue

	nombreBalle = int(nombreBalle)

	#  -----------------------------------------------------------------------------------------------------------------------------
	#                              Fin de la première boucle 
	#  -----------------------------------------------------------------------------------------------------------------------------

	#  -----------------------------------------------------------------------------------------------------------------------------
	#      Boucle exécutée tant que MLib ne reçoit pas d'event "pygame.QUIT" et que le jeu n'est pas fini
	#  -----------------------------------------------------------------------------------------------------------------------------

	enJeu = True

	# Chargement du moteur de jeu
	moteurDeJeu = Game(typeArme, 0, 0, mapp)
	moteurDeJeu.chargerArme(typeArme)
	moteurDeJeu.creerBalle(nombreBalle)

	mapp.setFocusedWidget(moteurDeJeu)

	#Affichage du jeu
	while enJeu:
		# Actualiser les évènements pygame et MLib
		mapp.frameEvent()

		if moteurDeJeu.tempsDepuisFin() >= 1:
			enJeu = False
					
		# Actualisater l'affichage graphique MLib et afficher de l'image
		mapp.frameGraphics()
		pygame.display.update()

	donneesFinDeJeu = moteurDeJeu.donneesFinDeJeu()
	moteurDeJeu.delete()
	del moteurDeJeu

	#  -----------------------------------------------------------------------------------------------------------------------------
	#                              Fin de la deuxième boucle 
	#  -----------------------------------------------------------------------------------------------------------------------------

	fin.setVisible(True)
	ecranDeFin = True
	texteBalleDetruiteFin.setText("Balle(s) détruite(s) : " + str(donneesFinDeJeu["nbBalleDetruite"]))
	texteTirFin.setText("Tir(s) : " + str(donneesFinDeJeu["nbTir"]))
	texteTirReussieFin.setText("Tir(s) réussie(s) : " + str(round((donneesFinDeJeu["nbTirReussie"]/donneesFinDeJeu["nbTir"])*100, 2)) + "%")
	texteTempsFin.setText("Temps : " + str(round(donneesFinDeJeu["temps"], 2)) + " secondes")

	#Affichage de l'écran d'accueil
	while ecranDeFin:
		# Actualiser les évènements pygame et MLib
		mapp.frameEvent()

		if boutonRejouerFin.isGettingLeftClicked(): #Re-aller à la page d'accueil
			ecranDeFin = False

		if boutonQuitterFin.isGettingLeftClicked(): #Quitter le programme
			pygame.quit()
			exit()
					
		# Actualisater l'affichage graphique MLib et afficher de l'image
		mapp.frameGraphics()
		pygame.display.update()

	fin.setVisible(False)

#  --------------------------------------------------------------------------
#                              Fin de la boucle 
#  --------------------------------------------------------------------------
