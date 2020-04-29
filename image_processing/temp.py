#%matplotlib inline
import matplotlib.pyplot as plt
import math
import numpy as np
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.image as mpimg

class Couleur:
    def __init__(self, R, G, B):
        self.R = float(R)
        self.G = float(G)
        self.B = float(B)
    
    @staticmethod
    def creerCouleur(listeRGB):
        return [listeRGB[0],listeRGB[1],listeRGB[2]]
        
    def getR(self):
        return self.R
    
    def getG(self):
        return self.G
    
    def getB(self):
        return self.B
        
    def brighter(self, pourcentage):
        R = self.getR() + (self.getR())*pourcentage
        G = self.getG() + (self.getG())*pourcentage
        B = self.getB() + (self.getB())*pourcentage
        return [R,G,B]
    
    def darker(self, pourcentage):
        R = (self.getR())*pourcentage
        G = (self.getG())*pourcentage
        B = (self.getB())*pourcentage
        return [R,G,B]
    
    def toString(self):
        return 'rgb('+str(self.getR())+','+str(self.getG())+','+str(self.getB())+')'
        
    
    def equals(self,color):
        return self.getR() == color.getR() and self.getG() == color.getG() and self.getB() == color.getB()
    
    def luminance(self):
        return 0.299*self.getR() + 0.587*self.getG() + 0.114*self.getB()
        
    
    def grayScale(self):
        l = int(self.luminance())
        return Couleur(l,l,l)
    
    def compatible(self,couleur):
        if((abs(self.luminance() - couleur.luminance())) <= 128):
            return True
        else:
            return False
        

    def add(self,color):
        R = (self.getR() + color.getR())/2
        G = (self.getG() + color.getG())/2
        B = (self.getB() + color.getB())/2
        return Couleur(R,G,B).toString()

    def showColor(self):
        fig, ax = plt.subplots()
        # create a grid to plot the color
        grid = np.mgrid[0.2:0.8:3j, 0.2:0.8:3j].reshape(2, -1).T
        # add a circle
        circle = mpatches.Circle(grid[0], 0.05, ec="none",color=(self.R/255,self.G/255,self.B/255))
        ax.add_patch(circle)
        #ax.add_line(line)

        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()

        plt.show()

a = Couleur(0,10,156)
a.showColor()















class Picture:
    def __init__(self,nomFichier = None,H = None, W = None):
        if nomFichier == None:
                
            self.H = H
            self.W = W
            self.img = np.zeros((H,W,3))
        else:
                
            self.img = mpimg.imread(nomFichier)
            self.H = self.img.shape[1]
            self.W = self.img.shape[0]
        
    
    def getH(self):
        return self.H
    
    def getW(self):
        return self.H
    
    def getImg(self):
        return self.img
    
    def getCouleur(self,row, col):
        R = self.getImg()[row,col,0]*255
        G = self.getImg()[row,col,1]*255
        B = self.getImg()[row,col,2]*255
        return [R,G,B]
         
    
    def setCouleur(self,row, col,couleur):
        self.getImg()[row,col,0] = couleur[0]/255
        self.getImg()[row,col,1] = couleur[1]/255
        self.getImg()[row,col,2] = couleur[2]/255
        
        
    def affiche(self):
        plt.imshow(self.img)
    
    def save(self, nomFichier):
        
        plt.imsave(nomFichier, self.img, format = 'png')


image_src = 'bird.png'
image = Picture(image_src)
image.affiche()
image.save('oiseau.png')










class ImageProcessing:
    
    def __init__(self,image):
        self.image = image
    '''
    Helper function
    '''
    def __calGray__(listePixel):
        A = math.floor(0.299*listePixel[0] + 0.587*listePixel[1] + 0.114*listePixel[2])
        return np.ndarray([A,A,A])
        
    '''
     Transformer en grayscale et visualiser l'image et sa transformée
     Appliquer les fonctions map, reduce ou filter pour reduire la complexite
    '''
    def transformGrayscaleMap(self):
        grayPicture = Picture(None,self.image.W,self.image.H)
        grayPicture.image = map(self.__calGray__,self.image[:,:])
        return grayPicture
        
    '''
     Transformer en grayscale et visualiser l'image et sa transformée
     Une classe gloutonne avec des boucles for
    '''
    def transformGrayscaleGlouton(self):
        image1_pixels = self.image.img
        nb_colonnes = len(image1_pixels[0,:,0])
        nb_lignes = len(image1_pixels[:,0,0])
        
        print("Résolution de l'image : " + str(nb_colonnes) + " x " + str(nb_lignes))
        
        for a in range(nb_lignes):
            for b in range(nb_colonnes):
                Y = image1_pixels[a][b][0]*0.299 + image1_pixels[a][b][1]*0.587 + image1_pixels[a][b][2]*0.114
                image1_pixels[a][b][0],image1_pixels[a][b][1],image1_pixels[a][b][2] = Y,Y,Y
        
        plt.imshow(image1_pixels)
                    
                 
        
    '''
     Creer une image en inversant les proportions de l'image source. Afficher les deux images
    '''
    def transformScale(self):
        image = self.image
        new_H = image.W
        new_W = image.H
        
        plt.figure(figsize=(30,20))
        
        plt.subplot(221)
        plt.imshow(image.img)
        plt.title("1280x838")
        
        plt.subplot(222)
        plt.imshow(image.img, extent=[0,new_W,0,new_H])
        plt.title("838x1280")
        plt.savefig("scaled.png", bbox_inches="tight", transparent="True")
        
        
    '''
    Separer les couleurs d'une image et visualiser les trois couleurs
    '''
    def separerCouleur(self):
        image = self.image.img
        
        red_only = image[:,:,0]
        green_only = image[:,:,1]
        blue_only = image[:,:,2]
        
        image1 = np.array([red_only, green_only*0, blue_only*0])
        image1 = np.swapaxes(image1, 0, 1)
        image1 = np.swapaxes(image1, 1, 2)
        
        image2 = np.array([red_only*0, green_only, blue_only*0])
        image2 = np.swapaxes(image2, 0, 1)
        image2 = np.swapaxes(image2, 1, 2)
        
        image3 = np.array([red_only*0, green_only*0, blue_only])
        image3 = np.swapaxes(image3, 0, 1)
        image3 = np.swapaxes(image3, 1, 2)
        
        plt.figure(figsize=(25,10))
        
        plt.subplot(241)
        plt.imshow(image)
        plt.title('Original')
        
        plt.subplot(242)
        plt.imshow(image1)
        plt.title('Red')
        
        plt.subplot(243)
        plt.imshow(image2)
        plt.title('Green')
        
        plt.subplot(244)
        plt.imshow(image3)
        plt.title('Blue')
        
        plt.imsave("red_channel.png", image1, format = 'png')
        plt.imsave("green_channel.png", image2, format = 'png')
        plt.imsave("blue_channel.png", image3, format = 'png')
        
        
    '''
    Filtre de glace: Affecter à chaque pixel p la couleur d'un pixel voisin choisi alétoirement
    (Les coordonnées du pixel et de p doivent différer d'au plus 5).
    Afficher les deux images 
    '''
    def filtreGlass(self):
        image = self.image
        i = image.img
        sH = image.H - 5
        sW = image.W - 5
        subset = i[5:(sH),5:(sW)]
        
        start = time.time()
        
        for y in range(5,sH):
            for x in range(5,sW):
                ss = subset[(y-5):(y+5),(x-5):(x+5)]
                i[y][x] = Voisin_centre(ss).get_color()
        
        plt.imshow(i)
        
        end = time.time()
        
        print("Durée de l'opération : " + str(end-start) + "s")
        
        plt.imsave("filter_glass.png", i, format = 'png')
        
        
        
    
class Voisin_centre:
    def __init__(self, subset):
        self.subset = subset
        
    def get_color(self):
        return random.choice(random.choice(self.subset))
    

image1 = Picture('bird.png')
#ImageProcessing(image1).transformGrayscaleGlouton()
#ImageProcessing(image1).transformScale()
#ImageProcessing(image1).separerCouleur()
#ImageProcessing(image1).filtreGlass()