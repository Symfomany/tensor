# ML


*Une caractéristique est une variable d'entrée*  la variable x dans une régression linéaire simple. 
Un projet de Machine Learning simple peut utiliser une seule caractéristique, tandis qu'un projet plus sophistiqué en utilisera plusieurs millions, spécifiés sous la forme :



Un exemple est une instance de donnée particulière, x. (x est mis en gras pour indiquer qu'il s'agit d'un vecteur.) Les exemples se répartissent dans deux catégories :

* Exemples étiquetés
* Exemples sans étiquette

Un exemple étiqueté comprend une ou plusieurs caractéristiques et l'étiquette. Par exemple :

labeled examples: {features, label}: (x, y)

On utilise des exemples étiquetés *pour entraîner le modèle*. 
Dans l'exemple du détecteur de spam, les exemples étiquetés désignent les e-mails que les utilisateurs ont explicitement marqués comme "spam" ou "non-spam".



Formulation : principaux termes du Machine Learning
Durée estimée : 8 minutes
Qu'est-ce que le *Machine Learning (supervisé)* ? Voici une description claire et concise :

Les systèmes de ML apprennent comment combiner *des entrées pour formuler des prédictions efficaces sur des données qui n'ont encore jamais été observées.*

Modèles
Un modèle définit *la relation entre les caractéristiques et l'étiquette*.* Par exemple, un modèle de détection de spam peut associer étroitement certaines caractéristiques à du "spam". Penchons-nous à présent sur deux phases de la durée de vie d'un modèle :

L'apprentissage consiste à créer ou à entraîner le modèle. En d'autres termes, vous présentez au modèle des exemples étiquetés, et vous lui permettez d'apprendre progressivement les relations entre les caractéristiques et l'étiquette.

L'inférence consiste à appliquer le modèle entraîné à des exemples sans étiquette. En d'autres termes, vous utilisez le modèle entraîné pour faire des prédictions efficaces (y'). Par exemple, pendant l'inférence, vous pouvez prédire medianHouseValue pour les nouveaux exemples sans étiquette.