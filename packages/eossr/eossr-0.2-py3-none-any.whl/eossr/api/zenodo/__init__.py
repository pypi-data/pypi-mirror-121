#!/usr/bin/env python

import sys
import json
import pprint
import requests
from os.path import abspath
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen
from ...metadata.codemeta2zenodo import parse_codemeta_and_write_zenodo_metadata_file
from . import http_status

__all__ = [
    'ZenodoAPI',
    'get_record',
    'get_zenodo_records',
    'http_status',
]



zenodo_api_url = "https://zenodo.org/api"
zenodo_sandobx_api_url = "https://sandbox.zenodo.org/api"


class ZenodoAPI:
    def __init__(self, access_token, sandbox=True, proj_root_dir='./'):
        """
        Manages the communication with the (sandbox.)zenodo REST API through the Python request library.
        This class is **EXCLUSIVELY** developed to be used within a CI/CD pipeline and to **EXCLUSIVELY PERFORM**
         the following tasks within the (sandbox.)zenodo api environment:

          - Fetches a user's published entries,
          - Creates a new deposit,
          - Fetches any published record,
          - Creates a new version of an existing deposit,
          - Uploads files to a specific Zenodo entry,
          - Erases a non-published entry / new version draft,
          - Erases (old version) files from an entry (when creating a new_version entry and uploading
            new_version files),
          - Uploads information to the entry (Zenodo compulsory deposit information),
          - Publishes an entry
          - Find all the published community entries
            * per title
            * per entry_id


        :param access_token: str
            Personal access token to (sandbox.)zenodo.org/api
        :param sandbox: bool
            Communicates with either zenodo or sandbox.zenodo api
        """

        if sandbox:
            self.api_url = zenodo_sandobx_api_url
        else:
            self.api_url = zenodo_api_url

        self.access_token = access_token
        self.parameters = {'access_token': self.access_token}

        self.proj_root_dir = Path(proj_root_dir)
        self.exist_codemeta_file = False
        self.path_codemeta_file = self.proj_root_dir
        self.exist_zenodo_metadata_file = False
        self.path_zenodo_metadata_file = self.proj_root_dir

    def fetch_user_entries(self):
        """
        Fetch the published entries of an user. Works to tests connection to Zenodo too.

        GET method to {api_url}/deposit/depositions

        :return: request.get method
        """
        url = f"{self.api_url}/deposit/depositions"

        return requests.get(url, params=self.parameters)

    def create_new_entry(self):
        """
        Create a new entry / deposition in (sandbox.)zenodo

        POST method to {api_url}/deposit/depositions

        :return: request.put method
        """
        url = f"{self.api_url}/deposit/depositions"
        headers = {"Content-Type": "application/json"}

        return requests.post(url, json={}, headers=headers, params=self.parameters)

    def fetch_entry(self, entry_id):
        """
        Fetches (recovers all the existing information, as well as links) of an existing Zenodo entry.

        GET method to {api_url}/deposit/depositions/{entry_id}

        :param entry_id: str
            entry_id of the entry to fetch

        :return: request.get method
        """
        # In case of entries created by oneself, or entries in the process of being created, the method to fetch
        # a record is request.get('api/deposit/deposition/{entry_id}') - see also the upload_file_entry method.

        # To fetch any other entry, already published, use:
        url = f"{self.api_url}/records/{entry_id}"
        return requests.get(url, params=self.parameters)

    def upload_file_entry(self, entry_id, name_file, path_file):
        """
        Upload a file to a Zenodo entry. If first retrieve the entry by a GET method to the
            {api_url}/deposit/depositions/{entry_id}.

        PUT method to {bucket_url}/{filename}. The full api url is recovered when the entry is firstly retrieved.

        :param entry_id: str
            deposition_id of the Zenodo entry
        :param name_file: str
            File name of the file when uploaded
        :param path_file: str
            Path to the file to be uploaded

        :return: request.put method
        """
        # 1 - Retrieve and recover information of a record that is in process of being published
        fetch = requests.get(f"{self.api_url}/deposit/depositions/{entry_id}",
                             params=self.parameters)

        # 2 - Upload the files
        bucket_url = fetch.json()['links']['bucket']  # full url is recovered from previous GET method
        url = f"{bucket_url}/{name_file}"

        with open(path_file, 'rb') as upload_file:
            upload = requests.put(url, data=upload_file, params=self.parameters)

        return upload

    def update_metadata_entry(self, entry_id, json_metadata):
        """
        Update an entry resource. Data should be the entry information that will be shown when a deposition is visited
        at the Zenodo site.

        PUT method to {api_url}/deposit/depositions/{entry_id}. `data` MUST be included as json.dump(data)

        :param entry_id: str
            deposition_id of the Zenodo entry
        :param json_metadata: object
            json object containing the metadata (compulsory fields) that are enclosed when a new entry is created.

        :return: request.put method
        """
        url = f"{self.api_url}/deposit/depositions/{entry_id}"
        headers = {"Content-Type": "application/json"}

        # The metadata field is already created, just need to be updated.
        # Thus the root 'metadata' key need to be kept, to indicate the field to be updated.
        data = {"metadata": json_metadata}

        return requests.put(url, data=json.dumps(data), headers=headers, params=self.parameters)

    def erase_entry(self, entry_id):
        """
        Erase an entry/new version of an entry that HAS NOT BEEN published yet.
        Any new upload/version will be first saved as 'draft' and not published until confirmation (i.e, requests.post)

        DELETE method to {api_url}/deposit/depositions/{entry_id}.

        :param entry_id: str
            deposition_id of the Zenodo entry to be erased

        :return: request.delete method
        """
        url = f"{self.api_url}/deposit/depositions/{entry_id}"
        return requests.delete(url, params=self.parameters)

    def erase_file_entry(self, entry_id, file_id):
        """
        Erase a file from an entry resource.
        This method is intended to be used for substitution of files (deletion) within an entry by their correspondent
         new versions.
        DELETE method to {api_url}/deposit/depositions/{entry_id}/files/{file_id}

        :param entry_id: str
            deposition_id of the Zenodo entry
        :param file_id: str
            Id of the files stored in Zenodo

        :return: requests.delete method
        """
        url = f"{self.api_url}/deposit/depositions/{entry_id}/files/{file_id}"
        return requests.delete(url, params=self.parameters)

    def publish_entry(self, entry_id):
        """
        Publishes an entry in (sandbox.)zenodo
        POST method to {api_url}/deposit/depositions/{entry_id}/actions/publish

        :param entry_id: str
            deposition_id of the Zenodo entry

        :return: requests.put method
        """
        url = f"{self.api_url}/deposit/depositions/{entry_id}/actions/publish"
        return requests.post(url, params=self.parameters)

    def new_version_entry(self, entry_id):
        """
        Creates a new version of AN EXISTING entry resource.
        POST method to {api_url}/deposit/depositions/{entry_id}/actions/newversion

        :param entry_id: str
            deposition_id of the Zenodo entry

        :return: requests.post method
        """
        url = f"{self.api_url}/deposit/depositions/{entry_id}/actions/newversion"
        parameters = {'access_token': self.access_token}

        return requests.post(url, params=parameters)

    def fetch_community_entries(self, community_name='escape2020', results_per_query=100):
        """
        Query the entries within a community.
        GET method, previous modification of the query arguments, to {api_url}/records


        :param community_name: str
            Community name. DEFAULT='escape2020'
        :param results_per_query: int
            Number of entries returned per call to the REST API. DEFAULT=100.

        :return: requests.get method
        """
        # https://developers.zenodo.org/#list36
        update_query_args = {'communities': str(community_name),
                             'size': int(results_per_query)
                             }
        self.parameters.update(update_query_args)

        # Full answer
        #   content = requests.post(url, params=self.parameters)
        # Answer items
        #   content.json().keys()
        # Stats
        #   content.json()['aggregations']
        # Total num of entries
        #   content.json()['hits']['total']
        # Zenodo metadata of each entry
        #   [item['metadata'] for item in content.json()['hits']['hits']]

        return requests.get(f"{self.api_url}/records", params=self.parameters)

    def fetch_community_entries_per_id(self, community_name='escape2020', results_per_query=100):
        """
        Query the `entries ids` of all the entries within a community

        :param community_name: str
            Community name. DEFAULT='escape2020'
        :param results_per_query: int
            Number of entries returned per call to the REST API. DEFAULT=100.

        :return: list
            List containing the `id`s of each community entry
        """
        return [entry['id'] for entry in
                self.fetch_community_entries(community_name, results_per_query).json()['hits']['hits']]

    def fetch_community_entries_per_title(self, community_name='escape2020', results_per_query=100):
        """
        Query the title of all the entries within a community

        :param community_name: str
            Community name. DEFAULT='escape2020'
        :param results_per_query: int
            Number of entries returned per call to the REST API. DEFAULT=100.

        :return: list
            List containing the title of each community entry
        """
        return [entry['metadata']['title'] for entry in
                self.fetch_community_entries(community_name, results_per_query).json()['hits']['hits']]

    def search_codemeta_file(self):
        """Check if a `codemeta.json` files exists in the ROOT directory of the project"""

        # root_dir = find_root_directory()
        root_dir = self.proj_root_dir
        print(f'\nProject root directory {abspath(root_dir)}')  # DEBUG

        codemeta_file = root_dir / 'codemeta.json'

        if codemeta_file.exists():
            print("\n * Found codemeta.json file within the project !")
            self.exist_codemeta_file = True
            self.path_codemeta_file = codemeta_file
        else:
            print("\n ! codemeta.json file NOT found in the root directory of the  project !")

    def search_zenodo_json_file(self):
        """Check if a `.zenodo.json` files exists in the ROOT directory of the project"""

        # root_dir = find_root_directory()
        root_dir = self.proj_root_dir

        zenodo_metadata_file = root_dir / '.zenodo.json'

        if zenodo_metadata_file.exists():
            print("\n * Found .zenodo.json file within the project !")
            self.exist_zenodo_metadata_file = True
            self.path_zenodo_metadata_file = zenodo_metadata_file
        else:
            print("\n ! .zenodo.json file NOT found in the root directory of the  project !")

    def conversion_codemeta2zenodo(self):
        """Perform the codemeta2zenodo conversion if a codemeta.json file is found"""

        if self.exist_codemeta_file:
            print("\n * Creating a .zenodo.json file from your codemeta.json file...")
            self.path_zenodo_metadata_file = self.path_codemeta_file.parent / '.zenodo.json'

            parse_codemeta_and_write_zenodo_metadata_file(self.path_codemeta_file,
                                                          self.path_zenodo_metadata_file)
        else:
            print("\n ! NO codemeta.json file found. \n"
                  "     Please add one to the ROOT directory of your project to ble able to perform the conversion.")

    def check_upload_to_zenodo(self):
        """
        `Tests` the different stages of the GitLab-Zenodo connection and that the status_code returned by every
        stage is the correct one.

        Checks:
         - The existence of a `.zenodo.json` file in the ROOT dir of the project
            - If not, it checks if it exists a `codemeta.json` file
               - If it exists it performs the codemeta2zenodo conversion
               - If not, it exits the program

         - The communication with Zenodo through its API to verify that:
            - You can fetch an user entries
            - You can create a new entry
            - The provided zenodo metadata can be digested, and not errors appear
            - Finally erases the test entry - because IT HAS NOT BEEN PUBLISHED !
        """
        # Search for the codemeta.json and the .zenodo.json files within the project
        self.search_codemeta_file()
        self.search_zenodo_json_file()

        if not self.exist_zenodo_metadata_file:

            if self.exist_codemeta_file:
                self.conversion_codemeta2zenodo()
            else:
                # No codemeta.json nor .zenodo.json
                sys.exit(-1)

        print("\n * Using the .zenodo.json file to simulate a new upload to Zenodo... \n")

        # 1 - Test connection
        print("1 --> Testing communication with Zenodo...")

        test_connection = self.fetch_user_entries()
        if test_connection.status_code == 200:
            print("  * Test connection status OK !")
        else:
            print("  ! ERROR while testing connection status\n", test_connection.json())

        # 2 - Test new entry
        print("2 --> Testing the creation of a dummy entry to (sandbox)Zenodo...")

        new_entry = self.create_new_entry()
        if new_entry.status_code == 201:
            print("  * Test new entry status OK !")
        else:
            print("  ! ERROR while testing the creation of new entry\n", new_entry.json())

        # 3 - Test upload metadata
        print("3 --> Testing the ingestion of the Zenodo metadata...")

        test_entry_id = new_entry.json()['id']
        with open(self.path_zenodo_metadata_file) as file:
            metadata_entry = json.load(file)
        update_metadata = self.update_metadata_entry(test_entry_id,
                                                     json_metadata=metadata_entry)

        if update_metadata.status_code == 200:
            print("  * Update metadata status OK !")
            pprint.pprint(metadata_entry)
        else:
            print("  ! ERROR while testing update of metadata\n",
                  update_metadata.json(), "\n", metadata_entry)
            print("  ! Erasing dummy test entry...\n")
            erase_error = self.erase_entry(test_entry_id)
            if erase_error.status_code != 204:
                print(f" !! ERROR erasing dummy test entry. Please erase it manually at\n "
                      f"{self.api_url[:-4]}/deposit")
            else:
                print("    - Done.\n")
            sys.exit(-1)

        # 4 - Test delete entry
        print("4 --> Testing the deletion of the dummy entry...")

        delete_test_entry = self.erase_entry(test_entry_id)
        if delete_test_entry.status_code == 204:
            print("  * Delete test entry status OK !")
        else:
            print("  ! ERROR while deleting test entry\n", delete_test_entry.json())

        print("\n\tYAY ! Successful testing of the connection to Zenodo ! \n\n"
              "You should not face any trouble when uploading a project to Zenodo - if you followed the "
              "`OSSR how to publish tutorial`:\n"
              "\t https://escape2020.pages.in2p3.fr/wp3/ossr-pages/page/contribute/publish_tutorial/#3-add-the-following-code-snippet \n"
              "In case you do, please contact us !\n")


    def get_user_records(self):
        request = self.fetch_user_entries()
        return [Record[hit] for hit in request.json()]


class Record:

    def __init__(self, data: dict):
        for k in ['id', 'metadata']:
            if k not in data.keys():
                raise ValueError(f"key {k} not present in data")
        self.data = data

    def __str__(self):
        return f"Record #{self.id} : {self.title}"

    def __repr__(self):
        return f"Record({self.data})"

    @property
    def id(self):
        return self.data['id']

    @property
    def title(self):
        return self.data['metadata']['title']

    def print_info(self):
        metadata = self.data['metadata']
        descrp = metadata['description']
        print(f"=== Record #{self.id} ===")
        print(f"Title: {self.title} ===")
        print(f"DOI: {self.data['doi']}")
        print(f"URL: {self.data['links']['html']}")
        print(f"Description:\n{descrp}")
        print('\n')

    @classmethod
    def from_id(cls, record_id):
        record = get_record(record_id=record_id)
        return record

    def get_codemeta(self):
        if 'files' not in self.data:
            raise FileNotFoundError(f'The record {self.id} does not contain any file')
        for file in self.data['files']:
            if file['key'] == 'codemeta.json':
                url = file['links']['self']
                return json.loads(urlopen(url).read())
        raise FileNotFoundError(f"No `codemeta.json` file found in record {self.id}")

    @property
    def doi(self):
        if not 'conceptdoi' in self.data:
            raise KeyError(f"Record {self.id} does not have a conceptdoi")
        return self.data['conceptdoi']

    def get_mybinder_url(self):
        binder_zenodo_url = 'https://mybinder.org/v2/zenodo/'
        doi = self.doi
        return binder_zenodo_url + doi



def get_zenodo_records(search='', sandbox=False, **kwargs):
    """
    Search the ossr based on `search`.
    Function rewritten from pyzenodo3 (https://github.com/space-physics/pyzenodo3)

    :param search: string
    :param kwargs: Zenodo query arguments.
        For an exhaustive list, see the query arguments at https://developers.zenodo.org/#list36
        Common arguments are:
            - size: int
                Number of results to return
            - all_versions: int
                Show (1) or hide (0) all versions of records
            - type: string
                Records of the specified type (Publication, Poster, Presentation, Software, ...)
            - keywords: string
                Records with the specified keywords

    :return:
    list of `Record`
    """
    search = search.replace("/", " ")  # zenodo can't handle '/' in search query

    params = {
        'q': search,
        **kwargs
    }

    api_url = zenodo_sandobx_api_url if sandbox else zenodo_api_url
    url = api_url + "/records?" + urlencode(params)

    recs = [Record(hit) for hit in requests.get(url).json()["hits"]["hits"]]

    if not recs:
        raise LookupError(f"No records found for search {search}")

    return recs


def get_record(record_id, sandbox=False):
    """
    Get a record from its id

    :param record_id: int
    :return: Record
    """
    api_url = zenodo_sandobx_api_url if sandbox else zenodo_api_url
    url = f"{api_url}/records/{record_id}"
    json = requests.get(url).json()
    if 'status' in json.keys():
        raise ValueError(f"Error {json['status']} : {json['message']}")
    else:
        return Record(json)



