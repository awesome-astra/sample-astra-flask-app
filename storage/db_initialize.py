"""
Don't mind this code too much, it's there just to create/populate the tables
and make this sample app work on some data.
"""

from db_connect import get_session
from cassandra.query import BatchStatement

INIT_CQL_A = '''
CREATE TABLE IF NOT EXISTS animals (
  genus           TEXT,
  species         TEXT,
  image_url       TEXT,
  size_cm         FLOAT,
  sightings       INT,
  taxonomy        LIST<TEXT>,
  PRIMARY KEY ((genus), species)
);
'''

INIT_CQL_P = '''
CREATE TABLE IF NOT EXISTS plants (
  genus           TEXT,
  species         TEXT,
  sightings       INT,
  PRIMARY KEY ((genus), species)
);
'''

POPULATE_CQL_0 = '''
INSERT INTO animals (
  genus,
  species,
  image_url,
  size_cm,
  sightings,
  taxonomy
) VALUES (
  'Vanessa',
  'cardui',
  'https://imgur.com/WrPsKkD',
  5.5,
  12,
  ['Arthropoda', 'Insecta', 'Lepidoptera', 'Nymphalidae']
);
'''

POPULATE_CQL_1 = '''
INSERT INTO animals (
  genus,
  species,
  image_url,
  size_cm,
  sightings,
  taxonomy
) VALUES (
  'Vanessa',
  'atalanta',
  'https://imgur.com/2fSEnt1',
  4.8,
  43,
  ['Arthropoda', 'Insecta', 'Lepidoptera', 'Nymphalidae']
);
'''

POPULATE_CQL_2 = '''
INSERT INTO animals (
  genus,
  species,
  image_url,
  size_cm,
  sightings,
  taxonomy
) VALUES (
  'Saitis',
  'barbipes',
  'https://imgur.com/coVy27e',
  0.6,
  4,
  ['Arthropoda', 'Arachnida', 'Aranea', 'Salticidae']
);
'''

PLANTAIN_SPECIES = [
    'afra',
    'africana',
    'aitchisonii',
    'alpina',
    'amplexicaulis',
    'arborescens',
    'arenaria',
    'argentea',
    'aristata',
    'asiatica',
    'aucklandica',
    'bigelovii',
    'canescens',
    'coreana',
    'cordata',
    'coronopus',
    'cornuti',
    'cretica',
    'cynops',
    'debilis',
    'elongata',
    'erecta',
    'eriopoda',
    'erosa',
    'fernandezia',
    'fischeri',
    'gentianoides',
    'glabrifolia',
    'grayana',
    'hawaiensis',
    'hedleyi',
    'helleri',
    'heterophylla',
    'hillebrandii',
    'himalaica',
    'holosteum',
    'hookeriana',
    'incisa',
    'indica',
    'krajinai',
    'lagopus',
    'lanceolata',
    'lanigera',
    'leiopetala',
    'longissima',
    'macrocarpa',
    'major',
    'maritima',
    'maxima',
    'media',
    'melanochrous',
    'moorei',
    'musicola',
    'nivalis',
    'nubicola',
    'obconica',
    'ovata',
    'pachyphylla',
    'palmata',
    'patagonica',
    'polysperma',
    'princeps',
    'purshii',
    'pusilla',
    'psyllium',
    'raoulii',
    'rapensis',
    'remota',
    'reniformis',
    'rhodosperma',
    'rigida',
    'robusta',
    'rugelii',
    'rupicola',
    'schneideri',
    'sempervirens',
    'sparsiflora',
    'spathulata',
    'subnuda',
    'tanalensis',
    'taqueti',
    'tenuiflora',
    'triandra',
    'triantha',
    'tweedyi',
    'virginica',
    'winteri',
    'wrightiana',
]


MINIMAL_INSERT_CQL = 'INSERT INTO plants (genus, species, sightings) VALUES (?, ?, ?);'


def init_db():
    session = get_session()
    print('[init_db] Running init scripts')
    session.execute(INIT_CQL_A)
    session.execute(POPULATE_CQL_0)
    session.execute(POPULATE_CQL_1)
    session.execute(POPULATE_CQL_2)

    session.execute(INIT_CQL_P)
    minimal_insert = session.prepare(MINIMAL_INSERT_CQL)
    batch = BatchStatement()
    for idx, species in enumerate(PLANTAIN_SPECIES):
        # we just scramble the numbers for fun
        batch.add(minimal_insert, ('Plantago', species, 1 + (idx) % 5 + (idx + 5) % 3))
    session.execute(batch)

    print('[init_db] Init script finished')


if __name__ == '__main__':
    init_db()
