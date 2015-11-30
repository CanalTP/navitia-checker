from behave import given, when, then
import requests
import json
import date_lib

def call_navitia(environnement, coverage, service, api_key, parameters):
    call = requests.get(environnement + coverage + "/"  + service, headers={'Authorization': api_key}, params = parameters)
    return call

@given(u'je teste le coverage "{test_coverage}"')
def step_impl(context, test_coverage):
    context.coverage = test_coverage
    params = json.load(open('steps/params.json'))
    test_env = context.config.userdata.get("environnement", "ppd") #pour passer ce param : behave fr_idf.feature -D environnement=production

    if test_env == "sim" or test_env == "simulation":
        context.base_url = params['environnements']['Simulation']['url'] + "coverage/"
        context.api_key = params['environnements']['Simulation']['key']
    elif test_env == "prod":
        context.base_url = params['environnements']['api.navitia.io']['url'] + "coverage/"
        context.api_key = params['environnements']['api.navitia.io']['key']
    elif test_env == "preprod" or test_env == "ppd" or test_env == "pre":
        context.base_url = params['environnements']['PreProd']['url'] + "coverage/"
        context.api_key = params['environnements']['PreProd']['key']
    else :
        assert False, "vous n'avez pas passé d'environnement de test valide : " + test_env

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
    nb_elem = int(context.lines['pagination']['total_result'])
    assert (nb_elem == int(expected_nb_elem)), "Nb d'éléments attendus " +expected_nb_elem+ " - Nb d'éléments obtenus " + str(nb_elem)

@when(u'je demande les réseaux')
def step_impl(context):
    nav_call =  call_navitia(context.base_url, context.coverage, "networks", context.api_key, {})
    context.lines = nav_call.json()
    context.url = nav_call.url

@when(u'je cherche le lieu "{places_query}"')
def step_impl(context, places_query):
    nav_call =  call_navitia(context.base_url, context.coverage, "places", context.api_key, {'q': places_query})
    context.places_result = nav_call.json()
    context.url = nav_call.url

@then(u'on doit me proposer le libellé "{expected_text_result}"')
def step_impl(context, expected_text_result):
    results_text = [place['name'] for place in context.places_result['places']]
    assert (expected_text_result in results_text)

@then(u'on ne doit pas me proposer le libellé "{not_expected_text_result}"')
def step_impl(context, not_expected_text_result):
    results_text = [place['name'] for place in context.places_result['places']]
    assert (not_expected_text_result not in results_text)

@when(u'je demande les lignes du réseau "{network_id}"')
def step_impl(context, network_id):
    nav_call =  call_navitia(context.base_url, context.coverage, "networks/{}/lines".format(network_id), context.api_key, {})
    context.lines = nav_call.json()
    context.url = nav_call.url

@when(u'je demande les zones d\'arrêts du réseau "{network_id}"')
def step_impl(context, network_id):
    nav_call =  call_navitia(context.base_url, context.coverage, "networks/{}/stop_areas".format(network_id), context.api_key, {})
    context.lines = nav_call.json()
    context.url = nav_call.url

@then(u'la ligne de code "{expected_line_code}" doit remonter en position "{position}"')
def step_impl(context, expected_line_code, position):
    ma_ligne = context.lines["lines"][int(position)-1]
    assert (ma_ligne["code"] == expected_line_code), "Code de la ligne attendue : {} - Code de la ligne obtenu : {}".format(expected_line_code, ma_ligne['code'])

@then(u'la ligne de code "{line_code}" doit avoir un parcours de nom "{expected_route_name}"')
def step_impl(context, line_code, expected_route_name):
    ligne = [une_ligne for une_ligne in context.lines['lines'] if une_ligne['code']== line_code][0]
    libelles_parcours = [route['name'] for route in ligne["routes"]]
    print('parcours attendu : ' + expected_route_name)
    print ('parcours trouvés :')
    for a_lib in libelles_parcours :
        print('--> ' + a_lib)
    assert (expected_route_name in libelles_parcours)

@given(u'je calcule un itinéraire avec les paramètres suivants ')
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

    journey_call = call_navitia(context.base_url, context.coverage, "journeys", context.api_key, {'from' : from_places, "to" : to_places, "datetime_represents": datetime_represent, "datetime" : datetime})
    context.journey_result = journey_call.json()
    context.journey_url = journey_call.url



@then(u'un des itinéraires proposés emprunte les sections suivantes ') #deprecated _ do not use ! à supprimer ?
def step_impl(context):
    print (context.journey_url) #pour le débug
    #extraction du détail des sections
    sections = []
    for a_journey in context.journey_result['journeys']:
        for a_section in a_journey['sections']:
            section_detail = {'type' : a_section['type']}
            if a_section['type'] == "public_transport":
                section_detail['mode'] = a_section['display_informations']['commercial_mode']
                section_detail['code'] = a_section['display_informations']['code']
                section_detail['from'] = a_section['from']['name']
                section_detail['to'] = a_section['to']['name']
            sections.append(section_detail)

    #comparaison avec l'attendu
    nb_sections_to_test = len([row['from'] for row in context.table])
    for row in context.table:
        expected_section = ({'from' : row['from'], 'to' : row['to'], 'mode' : row['mode'], 'code' : row['code'], 'type' : 'public_transport'})
        print ('section attendue :')
        print (expected_section)
        print ('sections trouvées :')
        print (sections)
        assert (expected_section in sections), "La section attendue n'a pas été trouvée"

@then(u'on doit me proposer la suite de sections suivante : "{expected_sections}"')
def step_impl(context, expected_sections):
    print (context.journey_url) #pour le débug
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

@given(u'je cherche des POIs à "{distance}" m du lieu "{places_query}"')
def step_impl(context, distance, places_query):
    location_call = call_navitia(context.base_url, context.coverage, "places", context.api_key, {'q' : places_query})
    location = location_call.json()['places'][0]['id']
    print ("le lieu autour duquel chercher est {}".format(location)) #debug

    around_call = call_navitia(context.base_url, context.coverage, "places/{}/places_nearby".format(location), context.api_key, {'distance' : distance, "count" : "25", "type[]":"poi"})
    context.around_result = around_call.json()
    context.around_url = around_call.url
    around_call.json()['places_nearby'] # a-t-on des infos exploitables dans le retour navitia ?

@then(u'on doit me proposer au moins un POI de type "{poi_type_name}"')
def step_impl(context, poi_type_name):
    poi_types = [ elem['poi']['poi_type']['name'] for elem in context.around_result['places_nearby'] ]
    print ("Des POIs des types suivants ont été trouvés à proximité : {}".format(set(poi_types)))
    assert (poi_type_name in poi_types), "Aucun POI de ce type n'a été trouvé à proximité"

@when(u'je demande les modes physiques')
def step_impl(context):
    nav_call =  call_navitia(context.base_url, context.coverage, "physical_modes", context.api_key, {'count':50})
    context.physical_modes = nav_call.json()
    context.url = nav_call.url

@then(u'tous les modes retournés me sont connus')
def step_impl(context):
    expected_physical_modes = ["physical_mode:Air", "physical_mode:Boat", "physical_mode:Bus", "physical_mode:BusRapidTransit", "physical_mode:Coach", "physical_mode:Ferry", "physical_mode:Funicular",
        "physical_mode:LocalTrain", "physical_mode:LongDistanceTrain", "physical_mode:Metro", "physical_mode:RapidTransit", "physical_mode:Shuttle",  "physical_mode:Taxi", "physical_mode:Train",
        "physical_mode:Tramway", "physical_mode:Bike", "physical_mode:BikeSharingService", "physical_mode:CheckOut", "physical_mode:CheckIn", "physical_mode:Car",
        "physical_mode:default_physical_mode", "physical_mode:Other" ]
    modes = [elem['id'] for elem in context.physical_modes['physical_modes']]
    pb_de_mode = False
    for a_mode in modes :
        if a_mode not in expected_physical_modes :
            print ("le mode {} ne fait pas partie de la liste des modes physiques normalisés".format(a_mode))
            pb_de_mode = True
    if pb_de_mode :
        print (context.url)
        assert False, "il y a au moins un mode physique non normalisé"