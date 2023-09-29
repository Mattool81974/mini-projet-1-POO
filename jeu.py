# Importation des bibliothèques (ma librairie graphique (version 2.0.1, qui importe math et pygame) et random)
from mlib import *
from random import *

# Pour comprendre comment fonctionne le code, je vous invite à aller voir la documentation de ma librairie graphique (voir documentation.html)

# Dimensions de la fenetre
largeur = 638
hauteur = 320
TAILLE = (largeur, hauteur)

# Chargement des images et de la police de caractères
fond = 'img/fond.jpg'
balle = 'img/balle.png'
font = 'font/elite.ttf'

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

# Création de la classe des balles
# La classe héritant de MImage, elle affiche la texte de la balle
class Balle(MImage):
	# Chargement des constantes de Balle
	BALLE_RAYON = 25
	MINIMUM_Z = 100
	MAXIMUM_Z = 200

	# Constructeur d'une balle (qui prend un attribut x et y, mais aussi z pour calculer sa taille en profondeur)
	def __init__(self, x, y, z, parent, widgetType="MImage"):
		self.setZ(z)

		super().__init__(balle, x, y, Balle.BALLE_RAYON * 2 * self.calculerRetrecissement(), Balle.BALLE_RAYON * 2 * self.calculerRetrecissement(), parent, widgetType)
		self.setBackgroundColor((0, 0, 0, 0))
		self.setImageSize((Balle.BALLE_RAYON * 2 * self.calculerRetrecissement(), Balle.BALLE_RAYON * 2 * self.calculerRetrecissement()))
		self.setImageReframing(4)

		self.dessinerForce = False
		self.force = 10
		self.forceAngle = 0

	# Calculer le retrecissement apparent de l'objet par l'utilisateur
	def calculerRetrecissement(self):
		return Balle.MINIMUM_Z/self.getZ()
	
	#Permettre le dessin d'une flèche indiquant l'angle de la force
	def setDessinerForce(self, dessinerForce):
		if self.dessinerForce != dessinerForce:
			self.dessinerForce = dessinerForce
			self.setShouldModify(True)
	
	# Retourne la valeur de la force de la balle
	def getForce(self):
		return self.force
	
	# Retourne la valeur de l'angle (en radian) de la force de la balle (pour comprendre comment fonctionne l'angle, voir angle.png)
	def getForceAngle(self):
		return self.forceAngle
	
	# Retourne l'attribut z
	def getZ(self):
		return self.z
	
	# Change la valeur de la force de la balle
	def setForce(self, force):
		self.force = force
	
	# Change la valeur de l'angle de la force de la balle
	def setForceAngle(self, forceAngle):
		self.forceAngle = normaliserAngle(forceAngle)
		if self.dessinerForce:
			self.setShouldModify(True)
	
	# Change la valeur de l'attribut z
	def setZ(self, z):
		self.z = z

	# Retourne par combien il faut multiplier la valeur de la force pour obtenir le vecteur vitesse
	def vecteurMultiplicateur(self):
		return (cos(self.getForceAngle()), sin(self.getForceAngle()))

	# Retourner le vecteur vitesse de la balle selon la force et son angle
	def vecteurVitesse(self):
		vecteurMultiplicateur = self.vecteurMultiplicateur()
		return (vecteurMultiplicateur[0] * self.getForce(), vecteurMultiplicateur[1] * self.getForce())
	
	# Dessine sur la surface de la balle
	def _renderBeforeHierarchy(self, surface):
		surface = super()._renderBeforeHierarchy(surface)

		# Si on doit dessiner une ligne sur le widget
		if self.dessinerForce:
			vecteurMultiplicateur = self.vecteurMultiplicateur()

			endPos = (round(self.getWidth() / 2) + (vecteurMultiplicateur[0] * round(self.getWidth() / 2)), round(self.getHeight() / 2) + (vecteurMultiplicateur[1] * round(self.getHeight() / 2)))
			draw.line(surface, (0, 0, 0), (round(self.getWidth() / 2), round(self.getHeight() / 2)), endPos, 2)

		return surface

# Création de la classe du moteur de jeu
# La classe héritant de MImage, elle affiche l'image de font
class Game(MImage):

	# Constructeur du moteur de jeu
	def __init__(self, x, y, parent, widgetType="MImage"):
		super().__init__(fond, x, y, TAILLE[0], TAILLE[1], parent, widgetType)

		self.balles = [] #Liste qui contient toutes les balles du jeu

		# Texte qui sera affiché au bas de la fenetre
		WHITE = pygame.Color(255, 255, 255)
		text = MText('Projet NSI', 490, 300, 100, 20, self)
		text.setBackgroundColor((0, 0, 0, 0))
		text.setFont(font)
		text.setFontSize(16)
		text.setTextColor(WHITE)
		text.setTextVerticalAlignment(1)

	# Créer nombre balle
	def creerBalle(self, nombre):
		zS = []
		for i in range(nombre): # Créer totues les valeurs de x
			z = random()*(Balle.MAXIMUM_Z - Balle.MINIMUM_Z)+Balle.MINIMUM_Z
			zS.append(z)

		zS.sort() # Trier les valeurs de x pour permettre de générer les plus grandes en dernières
		zS = zS[::-1]

		for i in range(nombre):
			# Coordonnees de la POSITION initiale de la nouvelle balle (générees aléatoirement)
			angle = pi * 2 * random()
			f = 450 * random() + 50
			x = random()*(largeur-Balle.BALLE_RAYON)
			y = random()*(hauteur-Balle.BALLE_RAYON)
			z = zS[i]

			balle = Balle(x, y, z, self)
			balle.setForce(f)
			balle.setForceAngle(angle)
			self.balles.append(balle)

	# Fonction appelée à chaque frames par mapp avec deltaTime le temps qu'a duré la dernière frame
	def _update(self, deltaTime):
		for i in self.balles:
			nouveauX = i.getX()
			nouveauY = i.getY()
			vecteurVitesse = i.vecteurVitesse()

			# On calcule les nouvelles positions de chaques balles
			nouveauX += vecteurVitesse[0] * deltaTime
			nouveauY += vecteurVitesse[1] * deltaTime

			# On prend en compte les rebonds avec le bord
			if nouveauX < 0:
				nouveauX = 0
				i.setForceAngle(angleMiroir(i.getForceAngle(), "y"))
			elif nouveauX > self.getWidth() - i.getImageSize()[0]:
				nouveauX = self.getWidth() - i.getImageSize()[0]
				i.setForceAngle(angleMiroir(i.getForceAngle(), "y"))

			if nouveauY < 0:
				nouveauY = 0
				i.setForceAngle(angleMiroir(i.getForceAngle(), "x"))
			elif nouveauY > self.getHeight() - i.getImageSize()[1]:
				nouveauY = self.getHeight() - i.getImageSize()[1]
				i.setForceAngle(angleMiroir(i.getForceAngle(), "x"))

			i.move(nouveauX, nouveauY)


# Chargement du moteur de jeu
moteurDeJeu = Game(0, 0, mapp)
moteurDeJeu.creerBalle(50)

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
