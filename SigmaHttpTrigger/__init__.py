import time
import json
import pyodbc
import textwrap
import datetime
import logging
import azure.functions as func

from configparser import ConfigParser

def default(o):
    """Converts our Dates and Datetime Objects to Strings."""
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP Database trigger function processed a request.')

    # Initialize the Parser.
    config_parser = ConfigParser()

    # Load the Database Credentials.
    config_parser.read('SigmaHttpTrigger/config.ini')
    database_username = config_parser.get('sec-database', 'database_username')
    database_password = config_parser.get('sec-database', 'database_password')

    logging.info('Loaded Database Credentials.')

    # Grab the table name.
    table_name = req.params.get('table_name', 'DT_Idx_XBRL')

    # Grba the Drivers.
    logging.info(pyodbc.drivers())

    # Define the Driver.
    driver = '{ODBC Driver 17 for SQL Server}'

    # Create the connection String.
    connection_string = textwrap.dedent('''
        Driver={driver};
        Server={your_server_name_here},1433;
        Database=sec-filings;
        Uid={username};
        Pwd={password};
        Encrypt=yes;
        TrustServerCertificate=no;
        Connection Timeout=30;
    '''.format(
        driver=driver,
        username=database_username,
        password=database_password
    )).replace("'", "")

    # Create a new connection.
    try:
        cnxn: pyodbc.Connection = pyodbc.connect(connection_string)
    except pyodbc.OperationalError:
        time.sleep(2)
        cnxn: pyodbc.Connection = pyodbc.connect(connection_string)

    logging.info(msg='Database Connection Successful.')

    # Create the Cursor Object.
    cursor_object: pyodbc.Cursor = cnxn.cursor()

    # Define the Query.
    upsert_query = textwrap.dedent("""
    SELECT TOP 100 * FROM [dbo].[{table_name}]
    """.format(table_name=table_name))

    # Execute the Query.
    cursor_object.execute(upsert_query)

    # Grab the Records.
    records = list(cursor_object.fetchall())

    # Clean them up so we can dump them to JSON.
    records = [tuple(record) for record in records]

    logging.info(msg='Query Successful.')

    if records:

        # Return the Response.
        return func.HttpResponse(
            body=json.dumps(obj=records, indent=4, default=default),
            status_code=200
        )
