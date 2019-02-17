## MFCC

Pour revenir aux spectrogrammes, vous obtiendrez à la fin un tableau numpy de forme (32,128) - imaginez-le comme (*temps, fréquence*) - qui indique *la force d’une fréquence donnée pour un horodatage donné*. 

À partir de là, vous pouvez fondamentalement traiter *les fichiers son comme des images* et devenir fou avec n'importe quel modèle basé sur *la convolution qui fonctionne bien sur des images normales*, telles que *vgg, resnet*, etc. 

De plus, vous voudriez tirer parti de la *nature séquentielle des données*. les *réseaux de neurones récurrents* seront donc utiles.


En reconnaissance vocale, *l’augmentation des données aide à généraliser les modèles et à les rendre robustes contre les variations de vitesse*, de volume, de hauteur tonale ou de bruit de fond.

 J'ai fait ma propre implémentation de l'augmentation pour bien comprendre et contrôler ce qui se passe (au lieu d'utiliser l'implémentation tensorflow). *Pydub* s'est avéré très utile pour cette partie; Par exemple, cela vous permet *d'augmenter le volume d'un fichier wave de 5 décibels* en écrivant simplement wav += 5où se wavtrouve un AudioSegmentobjet pydub .


Pour créer des échantillons pour l'étiquette «silence», j'ai extrait des parties d'une seconde *à partir des échantillons de bruit fournis avec le jeu de données.*


