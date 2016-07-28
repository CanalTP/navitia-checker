

# Installation
* cloner le repo
* installer les dépendances : pip3 install -r requirements.txt
* créer le fichier params.json à partir du fichier default_params.json.
  * Si vous utilisez [navitia-explorer](https://github.com/CanalTP/navitia-explorer), vous pouvez reprendre le même fichier ;)
  * Sinon, obtenez une clef d'authentification navitia.io et mettez là dans le fichier
* tester (à la racine du répertoire) :
```shell
behave -D environnement=prod public_features/fr_idf.feature
```

Si vous ne constatez aucune erreur sur les étapes Given, c'est bon !

# Configuration avancée :lock:
Pour effectuer des tests sur des données non publiques, vous pouvez placer vos fichiers features dans un répertoire private_features non suivi par git
* soit en l'ajoutant au .gitignore (et éventuellement en le synchronisant par ailleurs avec un autre répertoire suivi par git)
* soit en ajoutant un repertoire suivi par git en tant que submodule (`git submodule add -f chemin-de-mon-repo-git--de-tests-privés private_features
`)

Puis l'utilisation est la même :

```shell
behave -D environnement=mine private_features/my_very_own_private_data.feature
```
