## Face Detection

[!https://camo.githubusercontent.com/a28e0994e7bea13e304c15ca607ded89992307b1/68747470733a2f2f646f63732e6f70656e63762e6f72672f332e312e302f686161725f66656174757265732e6a7067]
(https://camo.githubusercontent.com/a28e0994e7bea13e304c15ca607ded89992307b1/68747470733a2f2f646f63732e6f70656e63762e6f72672f332e312e302f686161725f66656174757265732e6a7067)

<!-- FabLab 0472105481 -->
# Lien detection de visage 3D

Face classification using Tensorflow

https://www.polygon-design.io/blog/face-classification-using-tensorflow/



# Démo de Algo de Haar

https://github.com/joelbarmettlerUZH/FaceClassification_Tensorflow/raw/master/MD_Resources/haar_cascade_demo.gif


Here we will work with face detection. Initially, the algorithm needs a lot of positive images (images of faces) and negative images (images without faces) to train the classifier. Then we need to extract features from it. For this, Haar features shown in the below image are used. They are just like our convolutional kernel. Each feature is a single value obtained by subtracting sum of pixels under the white rectangle from sum of pixels under the black rectangle.


## OpenCV

# Traitement d'images
Elle propose la plupart des opérations classiques en traitement bas niveau des images 8:

- lecture, écriture et affichage d’une image ;
- calcul de l'histogramme des niveaux de gris ou d'histogrammes couleurs ;
- lissage, filtrage ;
- seuillage d'image (méthode d'Otsu, seuillage adaptatif)
- segmentation (composantes connexes, GrabCut) ;
- morphologie mathématique.

0472105481
# Traitement d'image

- lecture, écriture et affichage d’une vidéo (depuis un fichier ou une caméra)
- détection de droites, de segment et de cercles par Transformée de Hough
- détection de visages par la méthode de Viola et Jones
- cascade de classifieurs boostés
- détection de mouvement, historique du mouvement

# Telechargement de Visages

La prochaine étape serait de *télécharger des images montrant des visages masculins et féminins*. 
Nous utiliserons ces images pour former ultérieurement notre modèle v3 de création. Bien sûr, nous pourrions simplement effectuer manuellement une recherche dans Google Images, puis télécharger les premières images X qui semblent répondre à nos besoins. Mais pourquoi ferions-nous manuellement quelque chose que nous pourrions également coder en python? 

Écrivons un court script qui effectue *une recherche Bing Images*  et télécharger les premières images X pour nous.


from BingImages import BingImages

BingImages.download(BingImages("Male Face", count=30, person="portrait").get(), "./Males")
