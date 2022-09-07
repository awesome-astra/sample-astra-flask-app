"""
These functions wrap CQL queries to store and retrieve specific
kind of items from database tables. These are for direct use by the API code.

This module, crucially, holds a process-wide (lazy) cache of CQL
prepared statements, which are used over and over to optimize the API
performance.
"""

from utils.models import Animal, Plant


prepared_cache = {}
def get_prepared_statement(session, stmt):
    """
    We hold a cache of prepared statements, one per CQL command.
    New CQL statements are prepared and kept in this cache for subsequent
    usage. The cache key is the statement itself (a choice which works because
    (1) no CQL is built programmatically with variable spaces, etc, and
    (2) parameters, or values, are never part of the statements to prepare).
    """
    if stmt not in prepared_cache:
        print(f'[get_prepared_statement] Preparing statement "{stmt}"')
        prepared_cache[stmt] = session.prepare(stmt)
    return prepared_cache[stmt]


def store_animal(session, animal):
    """
    This and the next functions wrap the execution of some CQL statement
    using the provided session, some parameters and the casting to
    Pydantic models. They take advantage of the prepared-statement cache.
    """
    store_cql = 'INSERT INTO animals (genus,species,image_url,size_cm,sightings,taxonomy) VALUES (?,?,?,?,?,?);'
    prepared_store = get_prepared_statement(session, store_cql)
    session.execute(
        prepared_store,
        (
            animal.genus,
            animal.species,
            animal.image_url,
            animal.size_cm,
            animal.sightings,
            animal.taxonomy,
        ),
    )


def retrieve_animal(session, genus, species):
    get_one_cql = 'SELECT * FROM animals WHERE genus=? AND species=?;'
    prepared_get_one = get_prepared_statement(session, get_one_cql)
    row = session.execute(prepared_get_one, (genus, species)).one()
    if row:
        return Animal(**row._asdict())
    else:
        return row


def retrieve_animals_by_genus(session, genus):
    get_many_cql = 'SELECT * FROM animals WHERE genus=?;'
    prepared_get_many = get_prepared_statement(session, get_many_cql)
    rows = session.execute(prepared_get_many, (genus,))
    return (
        Animal(**row._asdict())
        for row in rows
    )

def generator_retrieve_plant_by_genus(session, genus):
    """
    Contrary to all other functions here, this is a *generator*
    returning row after row. This choice is made to illustrate
    the StreamingResponse usage in the API and how it seamlessly
    integrates with the pagination over DB results, handled
    automatically by the Cassandra drivers.
    """
    get_many_cql = 'SELECT * FROM plants WHERE genus=?;'
    prepared_get_many = get_prepared_statement(session, get_many_cql)
    rows = session.execute(prepared_get_many, (genus,))
    for row in rows:
        yield Plant(**row._asdict())
