## Cloud Machine Learning

# General
Idée: Avoir de la puissance de calcul et du storage

https://cloud.google.com/ml-engine/docs/tensorflow/getting-started-training-prediction


Lien:
https://cloud.google.com/ml-engine/docs/tensorflow/getting-started-training-prediction?_ga=2.183740962.-542718344.1549350786

Console ML Cloud:
https://console.cloud.google.com/mlengine/jobs?hl=fr&project=console-28d14



# Etapes
Suivez les étapes ci-dessous pour configurer un compte GCP, activer l'API Cloud ML Engine, puis installer et activer le SDK Cloud.

! Ne pas oublier de set GOOGLE_APPLICATION_CREDENTIALS

Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the file path of the JSON file that contains your service account key. This variable only applies to your current shell session, so if you open a new session, set the variable again.


Voir Cloud Shell
Cloud Shell est disponible sous macOS, Linux et Windows (voir l'onglet CLOUD SHELL). Ce service vous permet d'essayer Cloud Machine Learning Engine rapidement. Toutefois, son utilisation n'est pas adaptée aux tâches de développement continu.


# Set the project

console - project id : console-28d14

gcloud config set project console-28d14

Puis verifier les modèle de créer:
gcloud ml-engine models list


MAJ des composants Gcloud
gcloud components update



Lien
https://cloud.google.com/ml-engine/docs/tensorflow/getting-started-training-prediction?_ga=2.183740962.-542718344.1549350786#run_a_simple_tensorflow_python_program


# Voir Tuto
https://cloud.google.com/ml-engine/docs/tensorflow/getting-started-training-prediction?_ga=2.183740962.-542718344.1549350786#run_a_simple_tensorflow_python_program


Tutoriel bien fait, didactique.

## Coûts
Cette procédure utilise des composants facturables de Google Cloud Platform, tels que :

* Cloud Machine Learning Engine pour les éléments suivants :
 - Entraînement
 - Prédiction

* Cloud Storage pour les éléments suivants :
 - Stockage des données d'entrée pour l'apprentissage
 - Préproduction du package d'application d'apprentissage
 - Écriture d'artefacts d'apprentissage
 - Stockage des fichiers de données d'entrée pour la prédiction par lots


Best of Tools

Installing collected packages: numpy, tensorboard, setuptools, tensorflow, future, pyyaml, scipy, Keras, numexpr, python-dateutil, pandas, scikitlearn

# Executer en local

Pour exécuter votre apprentissage en local, exécutez la commande suivante :

```
    gcloud ml-engine local train \
        --module-name trainer.task \
        --package-path trainer/ \
        --job-dir $MODEL_DIR \
        -- \
        --train-files $TRAIN_DATA \
        --eval-files $EVAL_DATA \
        --train-steps 1000 \
        --eval-steps 100
```
https://cloud.google.com/ml-engine/docs/tensorflow/getting-started-training-prediction?_ga=2.183740962.-542718344.1549350786#local-train-single


### Executer la visualisation avec TensorBoard

Pour afficher les résultats de l'évaluation, vous pouvez utiliser l'outil de visualisation appelé TensorBoard. Il vous permet de visualiser votre graphe TensorFlow, de tracer des métriques quantitatives sur l'exécution de votre graphe, ainsi que d'afficher des données supplémentaires comme des images qui transitent par le graphe. TensorBoard est fourni avec l'installation de TensorFlow.



tensorboard --logdir=$MODEL_DIR --port=8080

# Devellopping Tensorflow Apps

https://cloud.google.com/ml-engine/docs/tensorflow/trainer-considerations
