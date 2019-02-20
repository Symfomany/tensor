(https://d2h0cx97tjks2p.cloudfront.net/blogs/wp-content/uploads/sites/2/2018/05/TensorFlow-Audio-Recognition-01.jpg)
[https://d2h0cx97tjks2p.cloudfront.net/blogs/wp-content/uploads/sites/2/2018/05/TensorFlow-Audio-Recognition-01.jpg]


+---+   +----------------+   +---+   +---+   +---+
|Mic|-->|Audio Processing|-->|KWS|-->|STT|-->|NLU|
+---+   +----------------+   +---+   +---+   +-+-+
                                               |
                                               |
+-------+   +---+   +----------------------+   |
|Speaker|<--|TTS|<--|Knowledge/Skill/Action|<--+
+-------+   +---+   +----------------------+


### Sound

Le *BIT DEPTH* et le *SAMPLE RATE*

Ces paramètres déterminent en partie *la qualité audio *des sons que vous allez produire, que ce soit pour créer des instrus, des boucles, des morceaux entiers, ou encore des lives.

### Le sample rate

En français : la fréquence (ou le taux) d’échantillonnage.
Un son « naturel » comme une voix, le bruit d’une porte qui claque ou encore celui du moteur d’une voiture est un signal continu, c’est une onde.

Mais quand on numérise ces sons « naturels », on les convertit en « 0 » et en « 1 », ce qui donne un signal binaire (contrairement à un signal continu).

C’est-à-dire que pour une durée donnée (par exemple : 1 seconde), on va « traduire » *(échantillonner) X fois* le son « naturel » en valeur numérique, et *cela à intervalles réguliers.*

Plus on a d’échantillons (ou « samples » en anglais) à la seconde,*plus la fréquence d’échantillonnage est grande*, et donc plus la traduction *en numérique est précise et fidèle.*

=> Un taux d’échantillonnage de *41.000 Hertz* (soit 41.000 Hz ou encore 41 Khz) ça veut dire qu’on a 41.000 échantillons par secondes 😉

– En dessous de 44.100 Hz : oubliez, c’est de la *qualité insuffisante pour faire du son* (et même pour juste écouter des MP3) !

– *44.100 Hz = très bonne qualité (CD)*, suffisant car deux fois la plage de fréquences audibles par *l’humain (20 Hz à 20.000 Hz maximum).*

– *48.000 Hz = excellente qualité*, plus que nécessaire dans la plupart des cas.

 

– Au dessus de 48.000 Hz = à fuir car ce sont des niveaux de qualité tellement élevés qu’ils n’ont pas d’utilité (sauf cas très particuliers), mais qui, en revanche, consomment beaucoup de ressources processeur (donc ralentissent votre ordi :-/ ).

 ### Le bit depth

On appelle ça la « résolution » en français : il s’agit de la *qualité de l’échantillonnage.*

Les échantillons traduits en valeurs numériques chaque seconde peuvent avoir différents niveaux de qualité :


– *16 bit = très bonne qualité (CD)*, suffisant dans la grande majorité des cas.
– *24 bit = excellente qualité*, plus que nécessaire dans la plupart des cas.
– 32 bit = à fuir car inutile (sauf cas particuliers).

### Recommandation of record Wave File

* Capture audio with a sampling rate of 16,000 Hz or higher. (avoid for example, in telephony the native rate is commonly 8000 Hz, which is the rate that should be sent to the service.)
* Use a lossless codec to record and transmit audio. FLAC or LINEAR16 is recommended. (avoid Using mp3, mp4, m4a, mu-law, a-law or other lossy codecs)
* The recognizer *is designed to ignore background voices and noise without additional noise-canceling*. 
However, for optimal results, position *the microphone as close to the user as possible, particularly when background noise is present.*

# Sampling rate
If possible, set the sampling rate of the audio source to 16000 Hz. 
For example, a rate of 8000 Hz means that a new frame is played or captured 8000 times per second.

# Frame size
Streaming recognition recognizes live audio as it is captured from a microphone or other audio source. 
 8000 Hz mono sound with 8 bit (1 byte) 

 See https://larsimmisch.github.io/pyalsaaudio/terminology.html

### Retourner par le read file of wav

* audiodata (numpy.ndarray or type(out)) – A two-dimensional NumPy array is returned,* where the channels are stored along the first dimension, i.e. as columns*. If the sound file has only one channel, a one-dimensional array is returned. Use always_2d=True to return a two-dimensional array anyway.
If out was specified, it is returned. If out has more frames than available in the file (or if frames is smaller than the length of out) and no fill_value is given, then only a part of out is overwritten and a view containing all valid frames is returned.

* samplerate (int) – The sample rate of the audio file.


## Conseils

Les avis des pros divergent sur la « bonne » configuration à adopter, mais ce qui revient souvent c’est que le format CD (*44.1 Khz en 16 bit*) est déjà *d’une très bonne qualité*, suffisante dans la grande majorité des cas.

Une autre chose qui revient souvent c’est *qu’un bit depth de 32 bit c’est inutile*, tout comme une *fréquence d’échantillonnage supérieure à 48 Khz* (et ça bouffe de la ressource processeur !).

Je parle bien sûr dans *le contexte de créer de la musique* (sound design / compo / mixage / mastering) pour un support comme le CD ou le vinyle…

C’est différent si vous comptez *faire des DVD avec du Dolby Surround…*

Vous pouvez donc mettre à jour votre logiciel de studio virtuel avec ces valeurs (*24 bit / 48 Khz*), et dormir sur vos deux oreilles 😀

### Le format WAV

Un fichier audio *non compressé est enregistré par défaut au format WAV.* 
Il s'agit d'un type de fichier mis au point par Microsoft. Un son d'une minute peut occuper entre 644Ko (kilo-octets) et 27Mo (mégaoctets). La taille de ce fichier dépend de *la fréquence d'échantillonnage, du type de son (mono ou stéréo) et du nombre de bits utilisés pour l'échantillonnage (8 ou 16 bits).*

Le taux d'echantillonage peut varier entre *11kHz, 22kHZ et 44kHz, avec un échantillonnage sur 8 ou 16 bit.*
Le volume d'un fichier wave stéréo pour 1 minute échantillonné à 44kHz en 16 bit est de :

```
    60 (secondes) * 16000 (taux d'échantillonage) * 1 (stéréo) * 2 (16 bits = 2 octets, 8bits = 1 octet) = 10.56Mo.
```

Un morceau de musique comprimé en MP3 à 128kbps et à 44kHz a une taille de 3Mo environ (pour 3 à 4 minutes), soit environ 1Mo par minute.


Pour un fichier compressé par divers procédés et dans divers formats (MP3, OGG, ...), on donne habituellement une valeur en kbps qui est en rapport avec le taux de compression (et donc le taux de perte).


Si on fait le calcul, on trouve qu'un WAV 44Khz / 16bits / Stéréo est à 1375Kbps. Donc, un MP3 compressé à 128Kbps a un taux de compression de 11 pour 1.


### Training Finished

After a few hours of training (depending on your machine's speed), the script should have completed all 18,000 steps. 
It will print out a final confusion matrix, along with an accuracy score, all run on the testing set. 
With the default settings, you should see an accuracy of between 85% and 90%.

Because audio recognition is particularly useful on mobile devices, next we'll export it to a compact format that's easy to work with on those platforms. To do that, run this command line:


Frozen model (.pb)
```
    python tensorflow/examples/speech_commands/freeze.py \
    --start_checkpoint=/tmp/speech_commands_train/conv.ckpt-18000 \
    --output_file=/tmp/my_frozen_graph.pb
```
Once the frozen model has been created, you can test it with the label_wav.py script, like this: (.pb)

python tensorflow/examples/speech_commands/label_wav.py \
--graph=/tmp/my_frozen_graph.pb \
--labels=/tmp/speech_commands_train/conv_labels.txt \
--wav=/tmp/speech_dataset/left/a5d485dc_nohash_0.wav



### MFCC

Les MFCC constituent une autre transformation sur les spectrogrammes et visent à mieux saisir les caractéristiques de la parole humaine (par rapport à la musique, par exemple). 
Il existe également des transformations delta et delta-delta au-dessus de MFCC, que vous pouvez probablement considérer comme des dérivées première et seconde. Voici à quoi ressemble la MFCC du même échantillon

Les MFCC sont la représentation standard des fonctionnalités dans les systèmes de reconnaissance vocale populaires tels que Kaldi. Je les ai essayés, mais comme je n’ai pas eu beaucoup de différence de précision et que je pensais que les spectrogrammes préservaient plus de données, je n’ai pas utilisé MFCC à la fin.

En reconnaissance vocale, *l’augmentation des données aide à généraliser les modèles et à les rendre robustes contre les variations de vitesse*, de volume, de hauteur tonale ou de bruit de fond. 

J'ai fait ma propre implémentation de l'augmentation pour bien comprendre et contrôler ce qui se passe (au lieu d'utiliser l'implémentation tensorflow). Pydub s'est avéré très utile pour cette partie; Par exemple, cela vous permet d'augmenter le volume d'un fichier wave de *5 décibels* en écrivant simplement wav += 5où se wavtrouve un AudioSegmentobjet pydub .




