Feature: Tests de non régression pour l'opendata en Île-de-rance

Background: définition de l'environnement utilisé pour les tests
    Given je teste le coverage "fr-idf"

Scenario: est-ce que mon paramétrage est ok et mon instance tourne ?
    When  j'interroge le coverage
    Then  je vois que tout va bien

Scenario: Nombre de réseaux
    When  je demande les réseaux
    Then  on doit m'indiquer un total de "123" éléments

Scenario: Nombre de lignes du réseau SITUS
    When  je demande les lignes du réseau "network:OIF:112"
    Then  on doit m'indiquer un total de "12" éléments

Scenario: Nom des parcours du réseau Stigo
    When  je demande les lignes du réseau "network:OIF:752"
    Then  la ligne de code "201" doit avoir un parcours de nom "Clos la Vigne - Ozoir RER"
    Then  la ligne de code "201" doit avoir un parcours de nom "Ozoir RER - Clos la Vigne"
    Then  la ligne de code "202" doit avoir un parcours de nom "Ozoir RER - Ozoir RER"

Scenario: Normalisation des modes physiques
    When  je demande les modes physiques
    Then  tous les modes retournés me sont connus

Scenario: Calcul d'itinéraire (OPTILE inside)
    When je calcule un itinéraire avec les paramètres suivants :
        | from                                 | to                  |datetime_represent | jour  | heure |
        | rue Chirol Boissy Saint Léger        | Porte de Charenton  | Partir après      | Mardi | 09h00 |
    Then on doit me proposer la suite de sections suivante : "Boissy RER (Boissy-Saint-Léger) ==[ Bus 12 - Arlequin ]==> Métro Préfecture (Créteil) / Créteil-Préfecture (Hôtel de Ville) (Créteil) ==[ Metro 8 - METRO ]==> Porte de Charenton (Paris) "

Scenario: Volumétrie des POIs
    When  je demande les POIs de type "poi_type:amenity:townhall"
    Then on doit m'indiquer un total d'au moins "300" éléments

Scenario: Ligne en fourche - note indiquant un terminus secondaire
    When je consulte la fiche horaire du parcours "route:OIF:100110013:13" pour le prochain "Vendredi"
    Then on doit me renvoyer au moins la note suivante : "Asnieres Gennevilliers Les Courtilles"

Scenario: Calcul d'itinéraire avec vélo (par profil)
Given j'ai le profil voyageur "cyclist"
When je calcule un itinéraire avec les paramètres suivants :
  | from                 | to          |datetime_represent | jour      | heure |
  | Porte de vincennes   | Nation      | Partir après      | Dimanche  | 10h04 |
Then on doit me proposer le mode alternatif suivant "vélo personnel"

Scenario: Calcul d'itinéraire avec vls (par passage de paramètre en dur)
    Given je veux bien un itinéraire avec le mode alternatif suivant "vls"
    When je calcule un itinéraire avec les paramètres suivants :
      | from                 | to          |datetime_represent | jour      | heure |
      | Porte de vincennes   | Nation      | Partir après      | Dimanche  | 10h04 |
    Then on doit me proposer le mode alternatif suivant "vls"

Scenario: Calcul d'itinéraire accessible (ligne à 1 et 2 arrêts à 5)
    Given j'ai le profil voyageur "wheelchair"
    When je calcule un itinéraire avec les paramètres suivants :
      | from                    | to                            |datetime_represent | jour   | heure |
      | GARE D'AULNAY SOUS BOIS | GARE DE BONDY (Bondy)         | Partir après      | Lundi  | 10h00 |
    Then on doit me proposer la suite de sections suivante : "GARE D'AULNAY SOUS BOIS (Aulnay-sous-Bois) ==[ T4 - Tram ]==> GARE DE BONDY (Bondy) "

Scenario: Est-ce que la tour eiffel a bougé ?
    When  je cherche le lieu "Tour Eiffel Paris"
    Then  on doit me proposer le libellé "Paris Tour Eiffel (Paris)"
    Then  on doit me proposer le lieu suivant à "20" mètres près : "http://www.openstreetmap.org/?mlat=48.857966&mlon=2.2945015"

Scenario: Fusions des zones d'arrêts partagées entre plusieurs réseaux
    When je demande les réseaux de la zone d'arrêt "stop_area:OIF:SA:8739110"
    Then on doit m'indiquer un total d'au moins "3" éléments

Scenario: Profondeur de données
    When je demande les jeux de données
    Then je constate que chaque contributeur dispose d'un jeu de données valide au moins "10" jours

Scenario: Chemins piétons
  Given je souhaite un itinéraire sans transports en commun
  When je calcule un itinéraire avec les paramètres suivants :
    | from          | to                         |datetime_represent | jour      | heure |
    | Torcy gare    | Allée voltaire Lognes      | Partir après      | Dimanche  | 12h54 |
  Then on doit me proposer au moins une solution
  Then la meilleure solution doit durer moins de "10" minutes
