from behave import given, when, then
import requests
import json
import os, sys
import date_lib
import geo_lib

def call_navitia(environnement, coverage, service, api_key, parameters):
    call = requests.get(environnement + coverage + "/"  + service, headers={'Authorization': api_key}, params = parameters)
    return call

def check_nb_elem(expected_nb, explo_nav_result, is_nb_exact = True):
    """ compare le nombre de résultats retournés par une API d'exploration avec une référence"""
    try:
        nb_elem = int(explo_nav_result['pagination']['total_result'])
        if is_nb_exact :
            assert (nb_elem == int(expected_nb)), "Nb d'éléments attendus " +expected_nb+ " - Nb d'éléments obtenus " + str(nb_elem)
        else: #on s'attend à avoir au moins expected_nb d'élements
            assert (nb_elem >= int(expected_nb)), "Nb d'éléments attendus " +expected_nb+ " - Nb d'éléments obtenus " + str(nb_elem)
    except KeyError:
        assert (False), "Pas d'éléments"

@given(u'je teste le coverage "{test_coverage}"')
def step_impl(context, test_coverage):
    context.coverage = test_coverage
    params = json.load(open('steps/params.json'))
    test_env = context.config.userdata.get("environnement", "ko") #pour passer ce param : behave chemin/vers/mon_test.feature -D environnement=prod

    if test_env == "sim" or test_env == "simulation":
        context.base_url = params['environnements']['Simulation']['url'] + "coverage/"
        context.api_key = params['environnements']['Simulation']['key']
        context.env = "Simulation"
    elif test_env == "prod":
        context.base_url = params['environnements']['api.navitia.io']['url'] + "coverage/"
        context.api_key = params['environnements']['api.navitia.io']['key']
        context.env = "api.navitia.io"
    elif test_env == "preprod" or test_env == "ppd" or test_env == "pre":
        context.base_url = params['environnements']['PreProd']['url'] + "coverage/"
        context.api_key = params['environnements']['PreProd']['key']
        context.env = "PreProd"
    elif test_env == "int" or test_env == "internal":
        context.base_url = params['environnements']['Internal']['url'] + "coverage/"
        context.api_key = params['environnements']['Internal']['key']
        context.env = "Internal"
    elif test_env == "custo" or test_env == "customer":
        context.base_url = params['environnements']['Customer']['url'] + "coverage/"
        context.api_key = params['environnements']['Customer']['key']
        context.env = "Customer"
    else :
        assert False, "vous n'avez pas passé d'environnement de test valide : " + test_env

@given(u'je teste un coverage privé')
def step_impl(context):
    """
    Les fichiers features privés sont hébergés dans un autre répertoire et synchronisés (par ailleurs) avec le répertoire courant.
    Ce test vérifie que les fichiers features sont bien synchronisés.
    """
    destination = os.path.join(os.getcwd(), "private_features")

    #récupération de l'adresse du répo privé
    params = json.load(open('steps/params.json'))
    source = params['navitia-checker']['private_features_repo']

    nom_fichier_feature = ""
    for an_arg in sys.argv :
        if "private_features" in an_arg :
            path, filename = os.path.split(an_arg)
            nom_fichier_feature = filename

    if nom_fichier_feature == "":
        assert False, "je n'ai pas réussi à comparer le fichier contenu dans le répertoire navitia-checker avec celui contenu dans le répertoire source"

    #comparaison des deux fichiers
    import hashlib
    hash_source = hashlib.sha1(open(os.path.join(source, nom_fichier_feature), 'rb').read()).hexdigest()
    hash_dest = hashlib.sha1(open(os.path.join(destination, nom_fichier_feature), 'rb').read()).hexdigest()
    if hash_dest != hash_source :
        assert False, "le fichier contenu dans le répertoire est différent de celui contenu dans le répertoire source. Il faut les synchroniser avant de lancer les tests"

@when(u'j\'interroge le coverage')
def step_impl(context):
    nav_call =  call_navitia(context.base_url, context.coverage, "", context.api_key, {})
    context.http_code = nav_call.status_code
    print (nav_call.url)
    context.status = nav_call.json()['regions'][0]['status']

@then(u'je vois que tout va bien')
def step_impl(context):
    assert (context.http_code == 200)
    assert (context.status == "running")

@then(u'on doit m\'indiquer un total de "{expected_nb_elem}" éléments')
def step_impl(context, expected_nb_elem):
    print("L'URL d'appel est : " + context.url)
    check_nb_elem(expected_nb_elem, context.explo_result, is_nb_exact=True)

@then(u'on doit m\'indiquer un total d\'au moins "{expected_nb_elem}" éléments')
def step_impl(context,expected_nb_elem):
    print("L'URL d'appel est : " + context.url)
    check_nb_elem(expected_nb_elem, context.explo_result, is_nb_exact=False)

@when(u'je demande les réseaux')
def step_impl(context):
    nav_call =  call_navitia(context.base_url, context.coverage, "networks", context.api_key, {})
    context.explo_result = nav_call.json()
    context.url = nav_call.url

@when(u'je demande les calendriers')
def step_impl(context):
    nav_call =  call_navitia(context.base_url, context.coverage, "calendars", context.api_key, {})
    context.explo_result = nav_call.json()
    context.url = nav_call.url

@when(u'je cherche le lieu "{places_query}"')
def step_impl(context, places_query):
    nav_call =  call_navitia(context.base_url, context.coverage, "places", context.api_key, {'q': places_query})
    context.places_result = nav_call.json()
    context.url = nav_call.url

@then(u'on doit me proposer le libellé "{expected_text_result}"')
def step_impl(context, expected_text_result):
    results_text = [place['name'] for place in context.places_result['places']]
    print ("Résultats trouvés :")
    for a_result in results_text:
        print("--> " +  a_result)
    print (context.url)
    assert (expected_text_result in results_text)

@then(u'on doit me proposer le lieu suivant à "{distance}" mètres près : "{osm_link_with_marker}"')
def step_impl(context, distance, osm_link_with_marker):
    print (context.url)

    expected_coords = {}
    expected_coords['lat'] = osm_link_with_marker.partition("mlat=")[2].partition("&mlon")[0]
    expected_coords['lon'] = osm_link_with_marker.partition("mlon=")[2]

    results_coords = [place[place['embedded_type']]['coord'] for place in context.places_result['places']]
    print ("Résultats trouvés :")
    we_have_a_winner = False
    for a_result in results_coords:
        dist_to_expected = geo_lib.distance_wgs84(a_result, expected_coords)
        print("--> {} m - http://www.openstreetmap.org/?mlat={}&mlon={}".format(dist_to_expected, a_result['lat'], a_result['lon']))
        if dist_to_expected <= float(distance) :
            we_have_a_winner = True
    assert (we_have_a_winner), "Les propositions sont trop éloignées"

@then(u'on ne doit pas me proposer le libellé "{not_expected_text_result}"')
def step_impl(context, not_expected_text_result):
    results_text = [place['name'] for place in context.places_result['places']]
    assert (not_expected_text_result not in results_text)

@when(u'je demande les lignes du réseau "{network_id}"')
def step_impl(context, network_id):
    nav_call =  call_navitia(context.base_url, context.coverage, "networks/{}/lines".format(network_id), context.api_key, {})
    context.explo_result = nav_call.json()
    context.lines = nav_call.json()['lines']
    context.url = nav_call.url

@when(u'je demande les zones d\'arrêts du réseau "{network_id}"')
def step_impl(context, network_id):
    nav_call =  call_navitia(context.base_url, context.coverage, "networks/{}/stop_areas".format(network_id), context.api_key, {})
    context.explo_result = nav_call.json()
    context.url = nav_call.url

@when(u'je demande les réseaux de la zone d\'arrêt "{stop_area_id}"')
def step_impl(context, stop_area_id):
    nav_call =  call_navitia(context.base_url, context.coverage, "stop_areas/{}/networks".format(stop_area_id), context.api_key, {})
    context.explo_result = nav_call.json()
    context.url = nav_call.url

@then(u'la ligne de code "{expected_line_code}" doit remonter en position "{position}"')
def step_impl(context, expected_line_code, position):
    ma_ligne = context.lines[int(position)-1]
    assert (ma_ligne["code"] == expected_line_code), "Code de la ligne attendue : {} - Code de la ligne obtenu : {}".format(expected_line_code, ma_ligne['code'])

@then(u'la ligne de code "{line_code}" doit avoir un parcours de nom "{expected_route_name}"')
def step_impl(context, line_code, expected_route_name):
    assert (line_code in [a_line["code"] for a_line in context.lines] ), "impossible d'identifier cette ligne"
    ligne = [une_ligne for une_ligne in context.lines if une_ligne['code']== line_code][0]
    libelles_parcours = [route['name'] for route in ligne["routes"]]
    print('parcours attendu : ' + expected_route_name)
    print ('parcours trouvés :')
    for a_lib in libelles_parcours :
        print('--> ' + a_lib)
    assert (expected_route_name in libelles_parcours)

@then(u'la ligne de code "{line_code}" doit avoir un code de type "{expected_code_type}" ayant pour valeur "{expected_code_value}"')
def step_impl(context, line_code, expected_code_type, expected_code_value):
    assert (line_code in [a_line["code"] for a_line in context.lines] ), "impossible d'identifier cette ligne"
    ligne = [une_ligne for une_ligne in context.lines if une_ligne['code']== line_code][0]
    codes = [code_list for code_list in ligne["codes"]]
    expected_code = {"value":expected_code_value, "type":expected_code_type}
    print("code attendu : ")
    print (expected_code)
    print ('code trouvés :')
    print (codes)
    assert (expected_code in codes), "le code n'a pas été trouvé dans la liste des codes retournés"

@given(u'j\'ai le profil voyageur "{traveler_profile}"')
def step_impl(context, traveler_profile):
    context.profile = traveler_profile

@when(u'je calcule un itinéraire avec les paramètres suivants ')
def step_impl(context):
    from_text = [row['from'] for row in context.table][0]
    to_text = [row['to'] for row in context.table][0]

    places_from_call = call_navitia(context.base_url, context.coverage, "places", context.api_key, {'q' : from_text})
    from_places = places_from_call.json()['places'][0]['id']

    places_to_call = call_navitia(context.base_url, context.coverage, "places", context.api_key, {'q' : to_text})
    to_places = places_to_call.json()['places'][0]['id']

    datetime_represent = [row['datetime_represent'] for row in context.table][0] #TODO
    if datetime_represent == "Arriver avant":
        datetime_represent = "arrival"
    else :
        datetime_represent = "departure"
    jour = [row['jour'] for row in context.table][0]
    heure = [row['heure'] for row in context.table][0]

    datetime = date_lib.day_to_use(jour, heure)

    params = {'from' : from_places, "to" : to_places, "datetime_represents": datetime_represent, "datetime" : datetime}

    #gestion des éventuels profils
    if "profile" in context :
        params['traveler_type'] = context.profile

    journey_call = call_navitia(context.base_url, context.coverage, "journeys", context.api_key, params )
    context.journey_result = journey_call.json()
    context.journey_url = journey_call.url

    nav_explo_url = "navitia-explorer/journey.html?ws_name={}&coverage={}".format(context.env ,context.coverage)
    nav_explo_url += "&from_text={}&from={}".format(from_text, from_places)
    nav_explo_url += "&to_text={}&to={}".format(to_text, to_places)
    date = "{}/{}/{}".format(datetime[6:8], datetime[4:6],datetime[0:4] )
    nav_explo_url += "&date={}&time={}&datetime_represents={}".format(date, heure, datetime_represent)
    if "profile" in context :
        nav_explo_url += "&traveler_type={}".format(context.profile)
    context.nav_explo = nav_explo_url

@then(u'on doit me proposer un prolongement de service à "{expected_stop_point}"')
def step_impl(context,expected_stop_point):
    print (context.journey_url) #pour le débug
    print (context.nav_explo)

    journeys = []
    print ("suite de sections hors transports : ")
    for a_journey in context.journey_result['journeys']:
        journey_transfer_sections = ""
        for a_section in a_journey['sections']:
            if a_section['type'] == "transfer":
                if 'transfer_type' in a_section and a_section['transfer_type']=='stay_in':
                    journey_transfer_sections += "Prolongement de service à {}".format(a_section['from']['name'])
                else :
                    journey_transfer_sections += "Correspondance à {}".format(a_section['from']['name'])
        print(journey_transfer_sections)
        journeys.append(journey_transfer_sections)

    assert ("Prolongement de service à {}".format(expected_stop_point) in journeys), "Il n'y a pas de prolongement de service à l'arrêt attendu"

@then(u'on doit me proposer le mode alternatif suivant "{expected_pseudo_mode}"')
def step_impl(context, expected_pseudo_mode):
    print (context.journey_url) #pour le débug
    print (context.nav_explo)

    journeys = []
    print ("suite de sections hors transports : ")
    for a_journey in context.journey_result['journeys']:
        journey_nonpt_sections = ""
        for a_section in a_journey['sections']:
            if a_section['type'] != "public_transport" and a_section['type'] != "on_demand_transport":
                journey_nonpt_sections += a_section['type']
                if 'mode' in a_section:
                    journey_nonpt_sections += " ({}); ".format(a_section['mode'])
                else :
                    journey_nonpt_sections += "; "
        print(journey_nonpt_sections)
        journeys.append(journey_nonpt_sections)

    pseudo_modes = []
    for a_journey in journeys :
        if "street_network (bike)" in a_journey :
            if "bss_put_back" in a_journey :
                pseudo_modes.append("vls")
            else :
                pseudo_modes.append("vélo personnel")
        if "street_network (car)" in a_journey :
                pseudo_modes.append("voiture personnelle")

    implemented_pseudo_modes = ['vélo personnel', 'voiture personnelle', 'vls']
    assert (expected_pseudo_mode in implemented_pseudo_modes), "Les modes alternatifs possibles sont les suivants : {}".format(implemented_pseudo_modes)
    assert (expected_pseudo_mode in pseudo_modes), "Le mode alternatif n'a pas été trouvé dans les itinéraires retournés"

@then(u'on doit me proposer la suite de sections suivante : "{expected_sections}"')
def step_impl(context, expected_sections):
    print (context.journey_url) #pour le débug
    print (context.nav_explo)
    #extraction du détail des sections
    journeys = []
    for a_journey in context.journey_result['journeys']:
        journey_to_string = ""
        last_to = None
        for a_section in a_journey['sections']:
            if a_section['type'] == "public_transport" or a_section['type'] == "on_demand_transport":
                mode = a_section['display_informations']['commercial_mode']
                code = a_section['display_informations']['code']
                reseau = a_section['display_informations']['network']
                from_ = a_section['from']['name']
                to_ = a_section['to']['name']
                if last_to == None:
                    journey_to_string += "{} ==[ {} {} - {} ]==> {} ".format(from_, mode, code, reseau, to_)
                elif last_to == from_ :
                    journey_to_string += "==[ {} {} - {} ]==> {} ".format(mode, code,reseau, to_)
                else :
                    journey_to_string += "/ {} ==[ {} {} - {} ]==> {} ".format(from_, mode, code,reseau, to_)
                last_to = to_

        journeys.append(journey_to_string)

    #comparaison avec l'attendu
    print ("suite de sections attendue : \n" + expected_sections)
    print ("suites de sections trouvées : ")
    for a_journey in journeys :
        print (a_journey)
    assert (expected_sections in journeys), "La suite de sections attendue n'a pas été trouvée"

@then(u'on ne doit pas me proposer de solution')
def step_impl(context):
    print (context.nav_explo)
    print (context.journey_url) #pour le débug
    #extraction du détail des sections
    journeys = []
    try:
        nb_elem = len(context.journey_result['journeys'])
    except KeyError:
        nb_elem = 0
    assert (nb_elem == 0), "Il y a {} résultats d'itinéraire".format(str(nb_elem))

@when(u'je cherche des POIs à "{distance}" m du lieu "{places_query}"')
def step_impl(context, distance, places_query):
    location_call = call_navitia(context.base_url, context.coverage, "places", context.api_key, {'q' : places_query})
    location = location_call.json()['places'][0]['id']
    print ("le lieu autour duquel chercher est {}".format(location)) #debug

    around_call = call_navitia(context.base_url, context.coverage, "places/{}/places_nearby".format(location), context.api_key, {'distance' : distance, "count" : "25", "type[]":"poi"})
    context.around_result = around_call.json()
    context.around_url = around_call.url
    context.nav_explo = "navitia-explorer/places_nearby.html?ws_name={}&coverage={}&point_name={}&point_id={}&distance={}".format(context.env ,context.coverage, places_query, location, distance)
    around_call.json()['places_nearby'] # a-t-on des infos exploitables dans le retour navitia ?

@then(u'on doit me proposer au moins un POI de type "{poi_type_name}"')
def step_impl(context, poi_type_name):
    print(context.nav_explo)
    poi_types = [ elem['poi']['poi_type']['name'] for elem in context.around_result['places_nearby'] ]
    print ("Des POIs des types suivants ont été trouvés à proximité : {}".format(set(poi_types)))
    assert (poi_type_name in poi_types), "Aucun POI de ce type n'a été trouvé à proximité"

@when(u'je demande les modes physiques')
def step_impl(context):
    nav_call =  call_navitia(context.base_url, context.coverage, "physical_modes", context.api_key, {'count':50})
    context.explo_result = nav_call.json()
    context.url = nav_call.url
    context.nav_explo = "navitia-explorer/ptref.html?ws_name={}&coverage={}&uri=%2Fphysical_modes%2F".format(context.env ,context.coverage)

@then(u'tous les modes retournés me sont connus')
def step_impl(context):
    print(context.nav_explo)
    expected_physical_modes = ["physical_mode:Air", "physical_mode:Boat", "physical_mode:Bus", "physical_mode:BusRapidTransit", "physical_mode:Coach", "physical_mode:Ferry", "physical_mode:Funicular",
        "physical_mode:LocalTrain", "physical_mode:LongDistanceTrain", "physical_mode:Metro", "physical_mode:RapidTransit", "physical_mode:Shuttle",  "physical_mode:Taxi", "physical_mode:Train",
        "physical_mode:Tramway", "physical_mode:Bike", "physical_mode:BikeSharingService", "physical_mode:CheckOut", "physical_mode:CheckIn", "physical_mode:Car",
        "physical_mode:default_physical_mode", "physical_mode:Other" ]
    modes = [elem['id'] for elem in context.explo_result['physical_modes']]
    pb_de_mode = False
    for a_mode in modes :
        if a_mode not in expected_physical_modes :
            print ("le mode {} ne fait pas partie de la liste des modes physiques normalisés".format(a_mode))
            pb_de_mode = True
    if pb_de_mode :
        print (context.url)
        assert False, "il y a au moins un mode physique non normalisé"

@when(u'je consulte la fiche horaire du parcours "{route_id}" pour le prochain "{weekday}"')
def step_impl(context, route_id, weekday):
    datetime = date_lib.day_to_use(weekday, "04h00")
    nav_call =  call_navitia(context.base_url, context.coverage, "routes/{}/route_schedules".format(route_id), context.api_key, {'from_datetime':datetime})
    context.explo_result = nav_call.json()
    context.url = nav_call.url

@then(u'on doit m\'indiquer que les horaires de l\'arrêt "{stop_point_id}" sont parfois estimés')
def step_impl(context, stop_point_id):
    print("L'URL d'appel est : " + context.url)
    if "route_schedules" in context.explo_result :
        found_stop_point = False
        for a_row in context.explo_result['route_schedules'][0]['table']['rows'] :
            arret_id = a_row['stop_point']['id']
            print(arret_id)
            if arret_id == stop_point_id :
                found_stop_point = True
                additional_informations = [elem['additional_informations'] for elem in a_row['date_times'] ]
                found_estimated = False
                for elem in additional_informations :
                    if 'date_time_estimated' in elem :
                        found_estimated = True
                        print ("c'est ok, j'ai trouvé un horaire de cet arrêt qui est estimé")
                        break
                    if found_estimated == False :
                        assert False, "aucun horaire de cet arrêt n'est estimé"
                break
        if found_stop_point == False :
            assert False, "l'arrêt indiqué n'est pas présent dans cette grille horaire de parcours"
    else :
        assert False, "pas d'horaires !"

@then(u'on doit me renvoyer au moins la note suivante : "{expected_note}"')
def step_impl(context, expected_note):
    print (context.url)
    if 'route_schedules' or 'stop_schedules' in context.explo_result :
        notes = [elem['value'] for elem in context.explo_result['notes']]
    else :
        assert False, "ce test ne permet de vérifier que les notes sur les fiches horaires"
    print ('voici la liste des notes retournées :')
    print (notes)

    assert (expected_note in notes), "la note attendue n'a pas été trouvée dans la liste des notes retournées"

@when(u'je demande les POIs de type "{poi_type}"')
def step_impl(context, poi_type):
    nav_call =  call_navitia(context.base_url, context.coverage, "poi_types/{}/pois".format(poi_type), context.api_key, {})
    context.explo_result = nav_call.json()
    context.url = nav_call.url

@when(u'je consulte la fiche horaire de l\'arrêt "{stop_point_id}" pour la ligne "{line_id}" et le calendrier "{calendar_id}"')
def step_impl(context, stop_point_id, line_id, calendar_id):
    params = {"calendar" : calendar_id, "show_code": True}
    nav_call =  call_navitia(context.base_url, context.coverage, "lines/{}/stop_points/{}/stop_schedules".format(line_id, stop_point_id), context.api_key, params)
    context.explo_result = nav_call.json()
    context.url = nav_call.url

@when(u'je consulte la fiche horaire de l\'arrêt "{stop_point_id}" pour la ligne "{line_id}"')
def step_impl(context, stop_point_id, line_id):
        nav_call =  call_navitia(context.base_url, context.coverage, "lines/{}/stop_points/{}/stop_schedules".format(line_id, stop_point_id), context.api_key, {})
        context.explo_result = nav_call.json()
        context.url = nav_call.url

@then(u'on doit me renvoyer des horaires temps réel')
def step_impl(context):
    print (context.url)
    if 'stop_schedules' in context.explo_result :
        data_freshness_list = set(elem['data_freshness'] for elem in context.explo_result['stop_schedules'][0]["date_times"])
    elif "departures" in context.explo_result :
        data_freshness_list = set(elem['stop_date_time']['data_freshness'] for elem in context.explo_result['departures'])
    else :
        assert False, "ce test ne permet de vérifier la présence de temps réel que sur les fiches horaires/prochains passages à l'arrêt"
    print ('voici la liste des fraicheurs de données retournées :')
    print (data_freshness_list)
    assert ("realtime" in data_freshness_list), "il n'y pas aucun horaire temps réel retourné"
