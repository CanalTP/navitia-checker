Feature: Tests de non régression pour l'opendata en Île-de-rance

Background: définition de l'environnement de test
    Given je teste le coverage "fr-idf"

Scenario: Profondeur de données
    When je demande les jeux de données
    Then on doit m'indiquer un total d'au moins "1" éléments
    Then je constate que chaque contributeur dispose d'un jeu de données valide au moins "10" jours

Scenario: Normalisation des modes physiques
    When  je demande les modes physiques
    Then  tous les modes retournés me sont connus

Scenario: Source des données carto
  When je demande des infos sur les données carto
  Then ma source de données pour les "adresses" est "osm"
  Then ma source de données pour les "POIs" est "osm"

Scenario: Vérification des feed publishers
    When  je demande les réseaux
    Then  on doit m'indiquer un nombre de fournisseurs de données de "1"
    Then  les informations sur les fournisseurs de données sont exploitables

Scenario: Calcul d'iti en funiculaire
    When je calcule un itinéraire avec les paramètres suivants :
        | from                   | to                     |datetime_represent | jour  | heure |
        | Funiculaire Gare basse | Funiculaire Gare haute | Partir après      | Mardi | 10h30 |
    Then on doit me proposer la suite de sections suivante : "Funiculaire Gare basse (Paris) ==[ Funiculaire FUN - Navette ]==> Funiculaire Gare haute (Paris) "

Scenario: Calcul d'iti métro + tram
    When je calcule un itinéraire avec les paramètres suivants :
        | from               | to              |datetime_represent | jour  | heure |
        | Le Kremlin Bicêtre | Porte de Thiais | Partir après      | Jeudi | 14h30 |
    Then on doit me proposer la suite de sections suivante : "Le Kremlin-Bicêtre (Le Kremlin-Bicêtre) ==[ Métro 7 - METRO ]==> Villejuif-Louis Aragon (Villejuif) / VILLEJUIF - LOUIS ARAGON (Villejuif) ==[ Tramway T7 - Tramway ]==> PORTE DE THIAIS (MARCHE INTERNATIONAL) (Chevilly-Larue) "

Scenario: Nombre de lignes de RER
    When  je demande les lignes du réseau "network:RER"
    Then on doit m'indiquer un total d'au moins "5" éléments

Scenario: Nombre de lignes dans le réseau tram
    When  je demande les lignes du réseau "network:TRAM"
    Then  on doit m'indiquer un total de "9" éléments

# Scenario: Parcours d'un Noctilien
#     When  je demande les lignes du réseau "network:OIF:56"
#     Then  la ligne de code "N144" doit avoir un parcours de nom "GARE DE L'EST NOCTILIEN - CORBEIL ESSONNES NOCTILIEN"
#     Then  la ligne de code "N144" doit avoir un parcours de nom "CORBEIL ESSONNES NOCTILIEN - GARE DE L'EST NOCTILIEN"
