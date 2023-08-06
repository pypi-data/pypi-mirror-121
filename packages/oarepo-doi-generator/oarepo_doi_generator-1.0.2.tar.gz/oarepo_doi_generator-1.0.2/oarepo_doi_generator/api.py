import json

from flask import current_app
from invenio_db import db
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from jsonref import requests

from .new_datasets_mapping import schema_mapping

def doi_already_requested(record):
    doi_requested = False

    if "persistentIdentifiers" not in record:
        return doi_requested
    identifiers_array = record["persistentIdentifiers"]


    for id in identifiers_array:
        if "DOI" in id["scheme"] and "requested" in id["status"]:
            doi_requested = True
            break

    return doi_requested

def doi_request(record):

    #if doi was not already requested
    if not doi_already_requested(record):
        if "persistentIdentifiers" not in record:
            record['persistentIdentifiers'] = [{
                "identifier": "",
                "scheme": "DOI",
                "status": "requested"
            }]
        else:
            record['persistentIdentifiers'].append(
                {
                    "identifier": "",
                    "scheme": "DOI",
                    "status": "requested"
                }
            )

    record.commit()
    db.session.commit()
    return record

def doi_approved(record, pid_type, test_mode = False):

    if doi_already_requested(record):
        record['persistentIdentifiers'].remove(
            {
                "identifier": "",
                "scheme": "DOI",
                "status": "requested"
            }
        )
        data = schema_mapping(record, pid_type, test_mode=test_mode)
        doi = doi_registration(data=data, test_mode=test_mode)
        if doi != None:
            record['persistentIdentifiers'].append(
                {
                    "identifier": doi,
                    "scheme": "DOI",
                    "statuse": "registered"
                }
            )
            record.commit()

            PersistentIdentifier.create('DOI', doi, object_type='rec',
                                    object_uuid=record.id,
                                    status=PIDStatus.REGISTERED)

            db.session.commit()

    return record


def doi_registration(data, test_mode = False):
    username = current_app.config.get("DOI_DATACITE_USERNAME")
    password = current_app.config.get("DOI_DATACITE_PASSWORD")

    if test_mode:
        url = 'https://api.test.datacite.org/dois'
    else:
        url = 'https://api.datacite.org/dois'


    request = requests.post(url=url, json=data, headers = {'Content-type': 'application/vnd.api+json'}, auth=(username, password))
    doi = ''
    if request.status_code == 201:
        response = json.loads(request.text)
        doi = response['data']['id']
    else:
        print(request.status_code)

    return doi




