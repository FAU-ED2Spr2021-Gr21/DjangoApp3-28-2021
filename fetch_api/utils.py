from .models import Entity
from .models import KeyPhrase
from .models import Other
from .models import Story
from .models import KeyPhrase
from .models import Entity
from .models import Person
from .models import Quantity
from .models import Other

from .constants import COMPARISON, NAMES


MODEL_ENTITIES = {
    'Entity': Entity,
    'KeyPhrase': KeyPhrase,
    'Other': Other,
    'Person': Person,
    'Quantity': Quantity,
    'Story': Story
}

def filter_nodes(node_type, name, notes, value, text, type):
    node_set = node_type.nodes

    if node_type.__name__ == 'Story':
        node_set.filter(notes__icontains=notes)
        node_set.filter(name__icontains=name)
        node_set.filter(value__icontains=value)

    if node_type.__name__ == 'KeyPhrase':
        node_set.filter(text__icontains=text)

    if node_type.__name__ == 'Entity' :
        node_set.filter(type__icontains=type)
        node_set.filter(text__icontains=text)

    return node_set

#count the length of nodes returned with filter  
def count_nodes(count_info):
    count = {}
    node_type             = count_info['node_type'] #only accepts Story, KeyPhrase, and Entity 
    name                  = count_info['name'] #Story exclusive 
    notes                 = count_info['notes'] #Story exclusive | everything is redacted
    value                 = count_info['value'] # story exclusive
    text                  = count_info['text'] #works for Keyphrase and Entity
    type                  = count_info['type'] #entity exclusive | drop down with choices of Person, Quantity, and Other
    node_set                = filter_nodes(MODEL_ENTITIES[node_type], name, notes, value, text, type)
    count = len(node_set)
    return count

def fetch_nodes(fetch_info):
    
    node_type             = fetch_info['node_type']
    name                  = fetch_info['name']
    notes                 = fetch_info['notes']
    value                 = fetch_info['value']
    text                  = fetch_info['text']
    type                  = fetch_info['type']

    limit           = fetch_info['limit']
    start           = ((fetch_info['page'] - 1) * limit)
    end             = start + limit

    node_set        = filter_nodes(MODEL_ENTITIES[node_type], name, notes, value, text, type)
    fetched_nodes   = node_set[start:end]

    #return fetched_nodes[0] # for shell test
    return [node.serialize for node in fetched_nodes]

#can be used for Entity Labels
def fetch_node_details(node_info):
    node_type       = node_info['node_type']
    nodeID         = node_info['nodeID']
    node            = MODEL_ENTITIES[node_type].nodes.get(nodeID=nodeID)
    node_details    = node

    # Make sure to return an empty array if not connections
    node_details['node_connections'] = []
    if (hasattr(node, 'serialize_connections')):
        node_details['node_connections'] = node.serialize_connections
        
    return node_details

#from constants.py
def fetch_names():
    return NAMES

def fetch_comparisons():
    return COMPARISON