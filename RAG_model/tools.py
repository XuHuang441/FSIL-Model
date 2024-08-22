import json

def get_labeled_data():
    labeled_data = []

    # read json
    with open('covenants.json', 'r') as file:
        data = json.load(file)

    for document in data:
        for result in document['annotations'][0]['result']:
            try:
                string = result['value']['text']
                label = result['value']['hypertextlabels'][0]
                labeled_data_dict = {label: string}
                labeled_data.append(labeled_data_dict)

            except KeyError:
                pass

    return labeled_data
