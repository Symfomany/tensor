## MFCC

Pour revenir aux spectrogrammes, vous obtiendrez à la fin un tableau numpy de forme (32,128) - imaginez-le comme (*temps, fréquence*) - qui indique *la force d’une fréquence donnée pour un horodatage donné*. 

À partir de là, vous pouvez fondamentalement traiter *les fichiers son comme des images* et devenir fou avec n'importe quel modèle basé sur *la convolution qui fonctionne bien sur des images normales*, telles que *vgg, resnet*, etc. 

De plus, vous voudriez tirer parti de la *nature séquentielle des données*. les *réseaux de neurones récurrents* seront donc utiles.

En reconnaissance vocale, *l’augmentation des données aide à généraliser les modèles et à les rendre robustes contre les variations de vitesse, de volume, de hauteur tonale ou de bruit de fond.*

 J'ai fait ma propre implémentation de l'augmentation pour bien comprendre et contrôler ce qui se passe (au lieu d'utiliser l'implémentation tensorflow). *Pydub* s'est avéré très utile pour cette partie; Par exemple, cela vous permet *d'augmenter le volume d'un fichier wave de 5 décibels* en écrivant simplement wav += 5où se wavtrouve un AudioSegmentobjet pydub .


Pour créer des échantillons pour l'étiquette «silence», j'ai extrait des parties d'une seconde *à partir des échantillons de bruit fournis avec le jeu de données.*

La MFCC (Mel Frequency Cepstral Coefficients) est une extraction de caractéristique du signal développée autour de la *FFT et de la DCT*, ceci sur une échelle de Mel. 


## On parle tous avec un filtre
Qu’est ce que la voix ?

La voix, pour faire simple, *c’est un flux d’air généré par les poumons qui fait vibrer les cordes vocales*. 
Cet air pulsé (ou non) est ensuite modulé par la cavité buccale et/ou nasale pour donner des sons intelligibles selon votre état.

Ce son est ensuite modulé par tout ce qui se présente *(dents, lèvres, langues, palais, cavité nasale, nourriture, etc) en fonction de ce que l’on souhaite dire.*

Maintenant découpons un signal sonore en plusieurs *petites tranches de 20 ms toutes les 10 ms (typiquement).* 
Sur chacune d’elles, on effectue une transformée de Fourier discrète permettant d’obtenir *la répartition énergétique des fréquences qui composent le signal.* 

Si on met bout à bout *ces spectres sur l’échelle du temps*, on obtient ce que l’on appelle un *spectrogramme.* 

En plus d’être agréable à regarder, il donne tout un tas d’informations. Il permet notamment de *deviner les mots prononcés à partir des formants et de la répartition du bruit.* Mais plus que ça, *il vous est unique.*

Gardons en tête qu’un système doit reconnaître un individu par sa voix *comme un humain le ferai.*
Car c’est bien notre oreille qui nous dit s’il s’agit de votre copine ou non lorsqu’il fait noir. Cet organe de perception ne sélectionne que ce qui l’intéresse. Par exemple, à intensité égale nous entendons mieux les aiguës (fréquences élevées) que les graves (fréquences basses), ou encore nous distinguons plus facilement deux fréquences proches dans les graves que dans les aiguës. Par conséquent pour savoir si deux voix sont identiques pour nos oreilles, et non celles de votre chat, nous devons tenir compte de nos propres spécificités.



Liens:
https://blog.groupe-sii.com/ral/



