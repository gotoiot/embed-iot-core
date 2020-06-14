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

from flask import Flask, Response, abort, json, jsonify, request

from beacons.ibeacon_scanner import IBeaconsScanner

#########[ Settings & Data ]###################################################

APP_CONFIG = {
    "HOST"          : "0.0.0.0",
    "PORT"          : 5000,
    "PREFIX"        : "/api/v1/",
    "DEBUG"         : True,
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
    logging.info("Data readed from DB file: " + str(stored_data))
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

@app.route(APP_CONFIG["PREFIX"] + '/ibeacon_settings/', methods=['GET'])
def get_ibeacon_settings():
    response = get_ibeacon_scanner_settings()
    # return the response with the status code
    return create_json_response(response, 200)

@app.route(APP_CONFIG["PREFIX"] + '/ibeacon_settings/', methods=['PUT', 'POST'])
def set_ibeacon_settings():
    if not request.json:
        return create_json_response(
            {'error' : 'Impossible to parse request body'}, 
            422
            )
    # modify module data
    ibeacons_scanner.update_settings(request.json)
    # obtain the current module data in a local variable
    ibeacons_scanner_settings = get_ibeacon_scanner_settings()
    # update DB file with new current module data
    db_save_data_to_file(ibeacons_scanner_settings)
    # Send new current module data as response
    response = ibeacons_scanner_settings
    return create_json_response(response, 200)

@app.route(APP_CONFIG["PREFIX"] + '/ibeacon_scanner/', methods=['GET'])
def get_ibeacon_scanner_info():
    # create response for all devices
    response = ibeacons_scanner._to_dict()
    # return the response with the status code
    return create_json_response(response, 200)

#########[ Specific module code ]##############################################

def get_ibeacon_scanner_settings():
    return  {
        key: ibeacons_scanner._to_dict()[key] for key in \
            ["uuid_filter", "scan_tick", "run_flag"]
    }

#########[ Module main code ]##################################################

def init_app():
    global ibeacons_scanner
    
    print ("Welcome to iBeacons Reader - Powered by Agustin Bassi")

    # configure logging
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        datefmt='%H:%M:%S'
        )
    # obtain the module data saved previously in DB file
    db_data = db_get_stored_data()
    # beacons controller instance
    ibeacons_scanner = IBeaconsScanner()
    ibeacons_scanner.update_settings(db_data)
    

if __name__ == '__main__':
    init_app()
    app.run(
        host=APP_CONFIG.get("HOST"), 
        port=APP_CONFIG.get("PORT"),
        debug=APP_CONFIG.get("DEBUG"),
        )


#########[ TODO section ]######################################################

# TODO: Create a thread to manage pushing messages to CMS
# TODO: Evaluate the possibility to publish this code in some place, or contact
# beacons tools maintainer in order to discuss if it can be acceptable.

#########[ Enf of file ]#######################################################
