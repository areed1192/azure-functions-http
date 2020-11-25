import json
import requests
import datetime
import logging
import xml.etree.ElementTree as ET

import azure.functions as func

from typing import List
from typing import Dict

from azure.storage.blob import ContainerClient
from azure.keyvault.secrets import SecretClient

from azure.identity import ClientSecretCredential
from azure.identity import DefaultAzureCredential


def parse_rss_feed(content: str) -> List[Dict]:
    """Parses the Content from the Azure Article feed.

    ### Parameters
    ----------
    content : str
        The HTTP response content returned from
        the request.

    ### Returns
    -------
    list[dict]
        A list of article dictionaries that have been
        parsed.
    """    

    # Initialize a list to store articles.
    articles = []

    # Parse it.
    root = ET.fromstring(content)

    # Grab all the articles by finding the "item" tag.
    articles_collection = root.findall("./channel/item" )

    # Loop through the articles.
    for article in articles_collection:
        
        # Prep a dictionary.
        article_dict = {}

        # Loop through each element in the "item" element.
        for elem in article.iter():

            # Set the tag as the key and the text as the value.
            article_dict[elem.tag] = elem.text.strip()
        
        # Add to the master list.
        articles.append(article_dict)
    
    return articles


def main(mytimer: func.TimerRequest) -> None:

    urls_to_pull = [
        'https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?board=AzureDataFactory&size=1000',
        'https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?board=AzureDataShare&size=1000',
        'https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?board=AzureStorage&size=1000',
        'https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?board=AzureDataExplorer&size=1000',
        'https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?board=AzureDataFactoryBlog&size=1000',
        'https://techcommunity.microsoft.com/plugins/custom/microsoft/o365/custom-blog-rss?board=AzureToolsBlog&size=1000'
    ]

    # Initialize the Credentials.
    default_credential = DefaultAzureCredential()

    # Create a Secret Client, so we can grab our Connection String.
    secret_client = SecretClient(
        vault_url='https://sigma-key-vault.vault.azure.net/',
        credential=default_credential
    )

    # Grab the Blob Connection String, from our Azure Key Vault.
    blob_conn_string = secret_client.get_secret(
        name='blob-storage-connection-string'
    )

    # Connect to the Container.
    container_client = ContainerClient.from_connection_string(
        conn_str=blob_conn_string.value,
        container_name='microsoft-azure-articles'
    )

    articles = []

    # Loop through each URL.
    for url in urls_to_pull:
        
        # Grab the Response.
        response = requests.get(url=url)

        # If it was okay.
        if response.ok:

            # Then Parse the articles and combine them.
            articles_parsed = parse_rss_feed(content=response.content)

            # Some feeds are empty.
            if articles_parsed:
                articles = articles + articles_parsed

    # Create a dynamic filename.
    filename = "Microsoft RSS Feeds/articles_{ts}.json".format(
        ts=datetime.datetime.now().timestamp()
    )

    # Create a new Blob.
    container_client.upload_blob(
        name=filename,
        data=json.dumps(obj=articles, indent=4),
        blob_type="BlockBlob"
    )

    logging.info('File loaded to Azure Successfully...')

    # Grab the UTC Timestamp.
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc
    ).isoformat()

    # Send message if Past Due.
    if mytimer.past_due:
        logging.info('The timer is past due!')

    # Otherwise let the user know it ran.
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
