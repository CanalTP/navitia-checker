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
        | rue Louise Chenu Boissy Saint Léger  | Porte de Charenton  | Partir après      | Mardi | 08h30 |
    Then on doit me proposer la suite de sections suivante : "Boissy RER (Boissy-Saint-Léger) ==[ Bus 23 - Plateau de Brie ]==> Pointe du Lac (Créteil) ==[ Metro 8 - METRO ]==> Porte de Charenton (Paris) "

Scenario: Volumétrie des POIs
    When  je demande les POIs de type "poi_type:amenity:townhall"
    Then on doit m'indiquer un total d'au moins "900" éléments

Scenario: Ligne en fourche - note indiquant un terminus secondaire
    When je consulte la fiche horaire du parcours "route:OIF:100110013:13" pour le prochain "Vendredi"
    Then on doit me renvoyer au moins la note suivante : "Asnieres Gennevilliers Les Courtilles"

Scenario: Calcul d'itinéraire avec vélo
Given j'ai le profil voyageur "cyclist"
When je calcule un itinéraire avec les paramètres suivants :
  | from                 | to          |datetime_represent | jour      | heure |
  | Porte de vincennes   | Nation      | Partir après      | Dimanche  | 10h04 |
Then on doit me proposer le mode alternatif suivant "vélo personnel"
