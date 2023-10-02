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
	def __init__(self, chargeur, tempsDeRechargement, texture, type, munitionTexture, munitionVitesse) -> None:
		self.chargeur = chargeur #Nombre de munitions possible dans le chargeur
		self.chargeurRestant = chargeur #Nombre du munitions restantes dans le chargeur
		self.debutRechargement = 0 #Temps où l'arme à commencer à se recharger
		self.munitionTexture = munitionTexture #Texture d'une munition de l'arme
		self.munitionVitesse = munitionVitesse #Vitesse d'une munition del'arme
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
			return True
		return False

	# Retourne la valeur de chargeur
	def getChargeur(self): return self.chargeur

	# Retourne la valeur de chargeurRestant
	def getChargeurRestant(self): return self.chargeurRestant

	# Retourne la texture de la munition
	def getMunitionTexture(self): return self.munitionTexture

	# Retourne munitionVitesse
	def getMunitionVitesse(self): return self.munitionVitesse

	# Retourne tempsDeRechargement
	def getTempsDeChargement(self): return self.tempsDeRechargement

	# Retourne texture
	def getTexture(self): return self.texture

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
	def __init__(self, x, y, parent, widgetType="MImage"):
		super().__init__('img/fond.jpg', x, y, TAILLE[0], TAILLE[1], parent, widgetType)

		self.armes = {} #Dictionnaire qui contient tous les types d'armes
		self.armeActuel = 0 #Contient l'arme actuelle
		self.armePosition = (0, 0) #Position de l'arme dans la fenêtre
		self.creerArme() #Créer tous les objets armes
		self.croixDeVisee = True #Booléen qui indique si une croix de visée est affichée ou non
		self.munitionTirees = [] #Liste des propriétés des munitions tirées
		self.nbTir = 0 #Nombre de tir total
		self.nbTirReussie = 0 #Nombre de tir réussie

		self.balles = [] #Liste qui contient toutes les balles du jeu
		self.nbBalleDetruite = 0 #Nombre de balles détruites

		self.calculerCollision = False #Booléen qui indique si on calcule les collisions ou non

		self.fini = False #Booléen qui indique si le jeu est fini
		self.timecodeDebut = time_ns() #Temps au début du jeu
		self.timecodeFin = -1 #Temps à la fin du jeu, ou -1 si le jeu n'est pas fini

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
  
		self.chargerArme("glock48")

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
		glock48 = Arme(16, 4, image.load("img/glock48.png").convert_alpha(), "glock48", image.load("img/glock48Munition.png").convert_alpha(), 2000) #Création du glock48

		self.armes["glock48"] = glock48

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

			if self.getCalculerCollision(): #Si on calcule les collisions (pas optimal)
				#On calcule les collisions (élastique) avec les autres balles
				for j in self.balles[index + 1:]:
					i.verifierCollisions()
					if i.touche(j) and not i.estEnCollisionAvec(j): #Si il y a collision et qu'elle n'as pas été encore traitée
						i.rajouterCollision(j) #On signale à la balle qu'une collision est en train d'avoir lieu
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
      
						nouveauX += i.getDX() * deltaTime
						nouveauY += i.getDY() * deltaTime

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

				if self.munitionTirees[j]["profondeur"] >= 100: #Si la balle est assez éloignée
					if distance2D(self.balles[i].getX() + self.balles[i].getRayon(), self.balles[i].getY() + self.balles[i].getRayon(), xMunition, yMunition) <= self.balles[i].getRayon():
						self.balles.remove(self.balles[i])
						self.munitionTirees.remove(self.munitionTirees[j])
						self.nbBalleDetruite += 1
						self.nbTirReussie += 1
						i -= 1
						j -= 1
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

			self.changerArmeChargeurTexte()

	# Fonction appelé lorsqu'une touche du clavier est pressée
	def _isKeyGettingPressed(self, key):
		if key == pygame.K_RIGHT:
			self.framePhysique(0.01)
		elif key == pygame.K_r and not self.fini:
			self.armeActuel.debuterChargement()

	# Fonction appelée lorsqu'une touche de la souris est clické
	def _isGettingMouseDown(self, button, relativePos):
		if button == 1 and not self.fini: #Si la touche gauche de la souris est clické
			self.tirer(relativePos)

	# Fonction utilisé quand la souris est bougé sur la zone de jeu
	def _mouseMove(self, buttons, pos, relativeMove):
		self.armePosition = (round(pos[0] - self.armeActuel.getTexture().get_width() / 2), round(pos[1] - self.armeActuel.getTexture().get_height() / 2))

	# Dessine sur la surface de jeu
	def _renderBeforeHierarchy(self, surface):
		surface = super()._renderBeforeHierarchy(surface)

		#Dessiner les balles
		for i in self.balles:
			surfaceABlit = i.getTexture()

			surface.blit(surfaceABlit, (i.getX(), i.getY(), surfaceABlit.get_width(), surfaceABlit.get_height()))

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
		if not self.fini:
			secondes = (time_ns() - self.timecodeDebut)/10**9 #Gérer le chronomètre
			minute = 0
			while secondes > 60:
				secondes -= 60
				minute += 1
			chrono = str(round(secondes, 2)) #Texte du chronomètre
			if minute != 0: chrono = str(round(minute)) + ":" + str(round(secondes, 2))
			self.chronometre.setText(chrono)

		self.framePhysique(deltaTime)

		if self.armeActuel.enChargement():
			if self.armeActuel.finirChargement():
				self.changerArmeChargeurTexte()

# Création de la partie graphique de la page d'accueil
accueil = MWidget(0, 0, TAILLE[0], TAILLE[1], mapp)
titreAccueil = MText("Jeu", 200, 20, TAILLE[0] - 400, 150, accueil)
boutonJouerAccueil = MButton("Jouer", 50, TAILLE[1] - 100, 200, 70, accueil)

# Création de la partie graphique de la page de fin
fin = MWidget(0, 0, TAILLE[0], TAILLE[1], mapp)
titreFin = MText("Fin du jeu", 100, 20, TAILLE[0] - 200, 100, fin)
boutonRejouerFin = MButton("Rejouer", 50, TAILLE[1] - 100, 200, 70, fin)
boutonQuitterFin = MButton("Quitter", TAILLE[0] - 250, TAILLE[1] - 100, 200, 70, fin)
texteBalleDetruiteFin = MText("Balle(s) détruite(s) : 0", 20, 130, 200, 20, fin)
texteTirFin = MText("Tir(s) : 0", TAILLE[0] - 220, 130, 200, 20, fin)
texteTirReussieFin = MText("Tir(s) réussi(s) : 0%", 20, 160, 200, 20, fin)
texteTempsFin = MText("0.0 s", TAILLE[0] - 220, 160, 200, 20, fin)

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
	ecranDAccueil = True

	#Affichage de l'écran d'accueil
	while ecranDAccueil:
		# Actualiser les évènements pygame et MLib
		mapp.frameEvent()

		if boutonJouerAccueil.isGettingLeftClicked(): #Lancer le jeu
			ecranDAccueil = False
					
		# Actualisater l'affichage graphique MLib et afficher de l'image
		mapp.frameGraphics()
		pygame.display.update()

	accueil.setVisible(False)

	#  -----------------------------------------------------------------------------------------------------------------------------
	#                              Fin de la première boucle 
	#  -----------------------------------------------------------------------------------------------------------------------------

	#  -----------------------------------------------------------------------------------------------------------------------------
	#      Boucle exécutée tant que MLib ne reçoit pas d'event "pygame.QUIT" et que le jeu n'est pas fini
	#  -----------------------------------------------------------------------------------------------------------------------------

	enJeu = True

	# Chargement du moteur de jeu
	moteurDeJeu = Game(0, 0, mapp)
	moteurDeJeu.creerBalle(2)

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
