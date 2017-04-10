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
    Then on doit me proposer la suite de sections suivante : "Funiculaire Gare Basse (Paris) ==[ Funiculaire FUN - Navette ]==> Funiculaire Gare Haute (Paris) "

Scenario: Calcul d'iti métro + tram
    When je calcule un itinéraire avec les paramètres suivants :
        | from               | to              |datetime_represent | jour  | heure |
        | Le Kremlin Bicêtre | Porte de Thiais | Partir après      | Jeudi | 14h30 |
    Then on doit me proposer la suite de sections suivante : "Le Kremlin-Bicêtre (Le Kremlin-Bicêtre) ==[ Métro 7 - METRO ]==> Villejuif-Louis Aragon (Villejuif) / Villejuif - Louis Aragon (Villejuif) ==[ Tramway T7 - Tramway ]==> Porte de Thiais (Marche International) (Chevilly-Larue) "

Scenario: Nombre de lignes de RER
    When  je demande les lignes du réseau "network:RER"
    Then on doit m'indiquer un total d'au moins "5" éléments

Scenario: Nombre de lignes dans le réseau tram
    When  je demande les lignes du réseau "network:TRAM"
    Then  on doit m'indiquer un total de "9" éléments

Scenario: Parcours d'un Noctilien
    When  je demande les lignes du réseau "network:OIF:56"
    Then  la ligne de code "N144" doit avoir un parcours de nom "Gare de l'Est Noctilien - Corbeil Essonnes Noctilien"
    Then  la ligne de code "N144" doit avoir un parcours de nom "Corbeil Essonnes Noctilien - Gare de l'Est Noctilien"

Scenario: Recapitalisation des arrêts - Musée d'Orsay
    When  je cherche le lieu "musee orsay"
    Then  on doit me proposer le libellé "Musée d'Orsay (Paris)"
    But   on ne doit pas me proposer le libellé "MUSEE D'ORSAY (Paris)"

Scenario: Recapitalisation des arrêts - St >> Saint
    When  je cherche le lieu "gare de boissy"
    Then  on doit me proposer le libellé "Gare de Boissy Saint-Léger (Boissy-Saint-Léger)"
    But   on ne doit pas me proposer le libellé "GARE DE BOISSY ST LEGER (Boissy-Saint-Léger)"

Scenario: Recapitalisation des arrêts - Chiffres romains
    When  je cherche le lieu "louis XIV"
    Then  on doit me proposer le libellé "Place Louis XIV (Viroflay)"

Scenario: Recapitalisation des arrêts - exception sur RER
    When  je cherche le lieu "rer rosny"
    Then  on doit me proposer le libellé "Rosny Bois Perrier RER (Rosny-sous-Bois)"
    But   on ne doit pas me proposer le libellé "ROSNY SOUS BOIS RER (Rosny-sous-Bois)"

Scenario: Recapitalisation des arrêts - exception sur IUT
    When  je cherche le lieu "iut paris 13"
    Then  on doit me proposer le libellé "IUT Paris 13 (Bobigny)"
    But   on ne doit pas me proposer le libellé "IUT PARIS 13 (Bobigny)"

Scenario: Recapitalisation des arrêts - 1er
    When  je cherche le lieu "alexandre 1er"
    Then  on doit me proposer le libellé "Alexandre 1er (Neuilly-Plaisance)"
    But   on ne doit pas me proposer le libellé "ALEXANDRE 1ER (Neuilly-Plaisance)"

Scenario: Recapitalisation des arrêts - 2ième
    When  je cherche le lieu "mairie 2"
    Then  on doit me proposer le libellé "Mairie du 2ème (Paris)"
    But   on ne doit pas me proposer le libellé "MAIRIE DU 2E (Paris)"

Scenario: Recapitalisation des arrêts - exception sur 2E et CDG
    When  je cherche le lieu "terminal 2E"
    Then  on doit me proposer le libellé "Aéroport CDG Terminal 2E (Le Mesnil-Amelot)"

Scenario: Recapitalisation des arrêts - HDV >> Hôtel de Ville
    When  je cherche le lieu "Préfecture versailles"
    Then  on doit me proposer le libellé "Préfecture Hôtel de Ville (Versailles)"
    But   on ne doit pas me proposer le libellé "Préfecture HDV (Versailles)"

Scenario: Recapitalisation des arrêts - gestion des articles
    When  je cherche le lieu "noisy le grand"
    Then  on doit me proposer le libellé "Gare de Noisy le Grand Mont d'Est (Noisy-le-Grand)"
    But   on ne doit pas me proposer le libellé "GARE DE NOISY LE GRAND MONT D'EST (Noisy-le-Grand)"

Scenario: Recapitalisation des arrêts - ajout d'apostrophe
    When  je cherche le lieu "chateau d'eau moissy"
    Then  on doit me proposer le libellé "Château d'Eau C.Bernard (Moissy-Cramayel)"
    But   on ne doit pas me proposer le libellé "CHATEAU D EAU C.BERNARD (Moissy-Cramayel)"

Scenario: Recapitalisation des arrêts - ajout d'accents
    When  je cherche le lieu "cité universitaire"
    Then  on doit me proposer le libellé "Cité Universitaire (Paris)"

Scenario: Recapitalisation des arrêts - ajout d'accents mais pas trop quand même
    When  je cherche le lieu "torcy"
    Then  on doit me proposer le libellé "Gare de Vaires Torcy (Vaires-sur-Marne)"

Scenario: Recapitalisation des arrêts - suppresion d'apostrophe
    When  je cherche le lieu "evreux"
    Then  on doit me proposer le libellé "Gare d'Évreux-Normandie (Évreux)"
    But   on ne doit pas me proposer le libellé "GARE DE EVREUX-NORMANDIE (Évreux)"

Scenario: Recapitalisation des arrêts - accents sur À
    When  je cherche le lieu "mare quenette"
    Then  on doit me proposer le libellé "Mare à Quenette (Vaux-le-Pénil)"
    But   on ne doit pas me proposer le libellé "Mare a Quenette (Vaux-le-Pénil)"

Scenario: Recapitalisation des arrêts - Rond point >> Rond-Point
    When  je cherche le lieu "rond point charles"
    Then  on doit me proposer le libellé "Rond-Point Saint-Charles (Paris)"
    But   on ne doit pas me proposer le libellé "ROND-POINT SAINT-CHARLES (Paris)"

Scenario: stop_points : ajout d'accents
    When  je consulte le point d'arrêt "stop_point:OIF:SP:59:4614403"
    Then  on doit me proposer le libellé "Libération - Condé (Saint-Maur-des-Fossés)"

Scenario: Modif de géoloc de point d'arrêt - Jules Vanzuppe
    When  je consulte le point d'arrêt "stop_point:OIF:SP:59:5709859"
    Then  on doit me proposer le libellé "Jules Vanzuppe (Paris) (Ivry-sur-Seine)"
    Then  on doit me proposer le lieu suivant à "10" mètres près : "https://www.openstreetmap.org/?mlat=48.8215038&mlon=2.3938315"

Scenario: Modif de géoloc de point d'arrêt - Friches - Jean Jaurès
    When  je consulte le point d'arrêt "stop_point:OIF:SP:70:11927"
    Then  on doit me proposer le libellé "Friches Jean Jaurès (Aulnay-sous-Bois)"
    Then  on doit me proposer le lieu suivant à "10" mètres près : "https://www.openstreetmap.org/?mlat=48.9220718&mlon=2.5047247"

Scenario: Modif de géoloc de point d'arrêt - Maison d'Arrêt
    When  je consulte le point d'arrêt "stop_point:OIF:SP:59:3730364"
    Then  on doit me proposer le libellé "Maison d'Arrêt (L'Haÿ-les-Roses) (Fresnes)"
    Then  on doit me proposer le lieu suivant à "10" mètres près : "https://www.openstreetmap.org/?mlat=48.7640436&mlon=2.3182474"

Scenario: Modif de géoloc de point d'arrêt - Les Sablons
    When  je consulte le point d'arrêt "stop_point:OIF:SP:46:11531"
    Then  on doit me proposer le libellé "Les Sablons (Viry-Châtillon)"
    Then  on doit me proposer le lieu suivant à "10" mètres près : "https://www.openstreetmap.org/?mlat=48.6688057&mlon=2.3636531"
