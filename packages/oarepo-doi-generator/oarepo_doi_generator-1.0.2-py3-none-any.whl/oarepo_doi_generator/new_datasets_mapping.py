from deepmerge import always_merger
from flask import current_app


def try_name(nlist,record, default=None):
    for name in nlist:
        try:
            return record[name]
        except:
            continue
    else:
        return default

def schema_mapping(record, pid_type, test_mode = False):

    prefix = current_app.config.get("DOI_DATACITE_PREFIX")
    url = record.canonical_url
    for_test_array = url.split('/')

    test_url_prefix = current_app.config.get("DOI_DATACITE_TEST_URL")
    test_url = test_url_prefix + for_test_array[-3] + '/' + for_test_array[-2] + '/' + for_test_array[-1]

    id_data = {}
    id = record['InvenioID']
    always_merger.merge(id_data, {"id": id})
    always_merger.merge(id_data, {"type": pid_type})


    attributes = {"event" :"publish", "prefix": prefix}

    #creators
    creators = try_name(nlist = ['creators'], record =record)
    if creators is None:
        always_merger.merge(attributes, {"creators": [{"name" : "Various authors"}]})
    else:
        creators_data = []
        for creator in creators:
            creator_data = {"name": creator['fullName']}
            creators_data.append(creator_data)
        always_merger.merge(attributes, {'creators': creators_data})

    #title
    titles = try_name(nlist=['titles'], record=record)
    if titles == None:
        always_merger.merge(attributes, {"titles": [{"_" : "Unknown"}]})
    else:
        for title in titles:
            if title['titleType'] == 'mainTitle':
                always_merger.merge(attributes, {"titles": title['title']})
                break

    #publication year
    if 'dateAvailable' in record: #should always be in record...
        date = record['dateAvailable']
        date_array = date.split('-')
        always_merger.merge(attributes, {"publicationYear": int(date_array[0])})

    #types
    datatype = try_name(nlist = ['resourceType' ], record =record)
    if datatype == None:
        new_type = "Dataset"  # defaul value
    else:
        new_type = datatype_mapping(datatype[0]['title']['en']) #tady to spadne, ci?

    always_merger.merge(attributes, {"types": {"resourceTypeGeneral": new_type}})

    #url
    if test_mode:
        always_merger.merge(attributes, {"url": test_url})
    else:
        always_merger.merge(attributes, {"url": record.canonical_url})

    #schemaVersion
    always_merger.merge(attributes, {"schemaVersion": "http://datacite.org/schema/kernel-4"})
    #publisher
    #todo publisher problem
    if current_app.config.get("DOI_DATACITE_PUBLISHER") == None:
        always_merger.merge(attributes, {"publisher": "CESNET"})
    else:
        always_merger.merge(attributes, {"publisher": current_app.config.get("DOI_DATACITE_PUBLISHER")}) #default: CESNET

    attributes = {"attributes" : attributes}


    always_merger.merge(id_data, attributes)
    data = {"data" : id_data}


    return data
def datatype_mapping(type):
    datatypes = ["Audiovisual", "Book", "BookChapter", "ComputationalNotebook",
                 "ConferencePaper", "ConferenceProceeding", "Dissertation",
                 "Journal", "JournalArticle", "OutputsManagementPlan",
                 "PeerReview", "Preprint", "Report", "Standard",
                 "Collection", "DataPaper", "Dataset", "Event",
                 "Image", "InteractiveResource", "Model", "PhysicalObject",
                 "Service", "Software", "Sound", "Text", "Workflow", "Other"
                 ]
    type_in_singular = type[:-1]
    for datatype in datatypes:
        if type.upper() == datatype.upper() or type_in_singular.upper() == datatype.upper():
            return(datatype)

    return "Dataset" #default value





