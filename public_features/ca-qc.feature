Feature: Tests de non régression pour l'opendata au Québec

Background: définition de l'environnement utilisé pour les tests
    Given je teste le coverage "ca-qc"

Scenario: est-ce que mon paramétrage est ok et mon instance tourne ?
    When  j'interroge le coverage
    Then  je vois que tout va bien

Scenario: Profondeur de données
  When je demande les jeux de données
  Then on doit m'indiquer un total d'au moins "20" éléments
  Then je constate que chaque contributeur dispose d'un jeu de données valide au moins "20" jours

Scenario: Normalisation des modes physiques
  When  je demande les modes physiques
  Then  tous les modes retournés me sont connus

Scenario: Source des données carto
  When je demande des infos sur les données carto
  Then ma source de données pour les "adresses" est "osm"
  Then ma source de données pour les "POIs" est "osm"

Scenario: Nombre de réseaux
    When  je demande les réseaux
    Then  on doit m'indiquer un total de "19" éléments
