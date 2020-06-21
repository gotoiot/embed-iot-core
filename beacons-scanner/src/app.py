#!/usr/bin/python
###############################################################################
# Author: Agustin Bassi
# Date: June 2020
# Licence: GPLV3
# Brief: TODO comment here
###############################################################################

#########[ Imports ]########################################################### 

import os
import json
import time
import logging
import requests

from flask import Flask, Response, abort, json, jsonify, request

from beacons.ibeacon_scanner import IBeaconsScanner

#########[ Settings & Data ]###################################################

APP_CONFIG = {
    "HOST"          : "0.0.0.0",
    "PORT"          : 5000,
    "PREFIX"        : "/api/v1/",
    "DEBUG"         : False,
    "DB_FILE_PATH"  : "../db/db.json",
}
# Flask App object
app = Flask(__name__)
# iBeacon scanner object used in the module
ibeacons_scanner = None

#########[ Utils ]#############################################################

def create_json_response(response, status_code):
    logging.debug("Sending JSON response to client")
    return Response(
        mimetype="application/json",
        response=json.dumps(response),
        status=status_code
    )

def db_get_stored_data():
    # obtain the full db path
    full_db_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        APP_CONFIG["DB_FILE_PATH"]
    )
    # Read data from DB file
    stored_data = json.loads(open(full_db_file_path).read())
    # Log the action to console
    logging.info("Data readed from DB")
    logging.debug("The data from DB file is: " + str(stored_data))
    # returns the data read from DB file as dict
    return stored_data

def db_save_data_to_file(data_to_store):
    # obtain the full db path
    full_db_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        APP_CONFIG["DB_FILE_PATH"]
    )
    # Save current data into DB file
    with open(full_db_file_path, 'w') as db_file:
        # save app data in json pretty mode
        json.dump(
            data_to_store, 
            db_file, 
            ensure_ascii=False, 
            indent=4
            )
    # Log the action to console
    logging.info("Updated DB file with new app data")

#########[ Application Views (endpoints) ]#####################################

@app.route(APP_CONFIG["PREFIX"] + '/ibeacons_settings/', methods=['GET'])
def get_ibeacon_settings():
    # execute local call to filter the desired fields to show
    response = get_ibeacon_scanner_settings()
    # return the response with the status code
    return create_json_response(response, 200)

@app.route(APP_CONFIG["PREFIX"] + '/ibeacons_settings/', methods=['PUT', 'POST'])
def set_ibeacon_settings():
    if not request.json:
        return create_json_response(
            {'error' : 'Impossible to parse request body'}, 
            422
            )
    # modify module data
    ibeacons_scanner.update_settings(request.json)
    # execute local call to get the desired fields as settings
    ibeacons_scanner_settings = get_ibeacon_scanner_settings()
    # update DB file with new settings
    db_save_data_to_file(ibeacons_scanner_settings)
    # Send new current module data as response
    response = ibeacons_scanner_settings
    return create_json_response(response, 200)

@app.route(APP_CONFIG["PREFIX"] + '/ibeacons_info/', methods=['GET'])
def get_ibeacon_scanner_info():
    # create response for all devices
    response = ibeacons_scanner.to_dict()
    # return the response with the status code
    return create_json_response(response, 200)

@app.route(APP_CONFIG["PREFIX"] + '/interface_settings/', methods=['GET'])
def get_interface_settings():
    db_data = db_get_stored_data()
    # execute local call to filter the desired fields to show
    response = { 
        "callback_uri" : str(db_data["callback_uri"]) 
        }
    # return the response with the status code
    return create_json_response(response, 200)

@app.route(APP_CONFIG["PREFIX"] + '/interface_settings/', methods=['PUT', 'POST'])
def set_interface_settings():
    if not request.json:
        return create_json_response(
            {'error' : 'Impossible to parse request body'}, 
            422
            )
    # if data is correct update callback_uri
    if request.json["callback_uri"] is not None and isinstance(request.json["callback_uri"], str):
        db_data = db_get_stored_data()
        db_data["callback_uri"] = request.json["callback_uri"]
        db_save_data_to_file(db_data)
        # send response
        response = { "callback_uri" : db_data["callback_uri"]}
        return create_json_response(response, 200)

#########[ Specific module code ]##############################################

def get_ibeacon_scanner_settings():
    return  {
        key: ibeacons_scanner.to_dict()[key] for key in \
            ["uuid_filter", "scan_tick", "run_flag"]
    }

def advice_for_changes_callback(changes_data):
    # obtain the module data saved previously in DB file
    db_data = db_get_stored_data()
    if isinstance(db_data["callback_uri"], str):
        try:
            req = requests.post(db_data["callback_uri"], data=changes_data)
            logging.debug("Calling CMS callback: " + str(db_data["callback_uri"]))
            logging.debug("Response code is: " + str(req.status_code))
        except:
            logging.warn("An error has ocurred when POST to: " + str(db_data["callback_uri"]))
        

#########[ Module main code ]##################################################

def init_app():
    global ibeacons_scanner
    
    print ("Welcome to Beacons Reader - Powered by Agustin Bassi")

    # configure logging
    logging.basicConfig(
        format='[ %(levelname)5s ] - %(funcName)28s -> %(message)s',
        level=logging.DEBUG,
        datefmt='%H:%M:%S'
        )
    # obtain the module data saved previously in DB file
    db_data = db_get_stored_data()
    # beacons controller instance
    ibeacons_scanner = IBeaconsScanner()
    ibeacons_scanner.update_settings(db_data)
    ibeacons_scanner.set_changes_callback(advice_for_changes_callback)
    

if __name__ == '__main__':
    init_app()
    app.run(
        host=APP_CONFIG.get("HOST"), 
        port=APP_CONFIG.get("PORT"),
        debug=APP_CONFIG.get("DEBUG"),
        )


#########[ TODO section ]######################################################

# TODO: Evaluate the possibility to publish this code in some place, or contact
# beacons tools maintainer in order to discuss if it can be acceptable.
# TODO: evaluate to put flask config (APP_CONFIG) as a resource HTTP

#########[ Enf of file ]#######################################################
