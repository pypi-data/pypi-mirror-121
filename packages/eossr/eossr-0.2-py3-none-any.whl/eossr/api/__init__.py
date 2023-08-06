import requests
from . import zenodo
from .zenodo import Record, get_zenodo_records, zenodo_api_url

__all__ = [
    'zenodo',
    'get_ossr_records'
]

escape_community = 'escape2020'


def get_ossr_records(search='', sandbox=False, **kwargs):
    """
    Retrieve all OSSR entries.
    Potentially long when the number of records in the OSSR increases.

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

    # make sure we find all OSSR records without limit on the number
    r = requests.get(zenodo_api_url+'/records', params={'communities': escape_community})
    number_of_ossr_entries = r.json()['aggregations']['access_right']['buckets'][0]['doc_count']
    kwargs['size'] = number_of_ossr_entries

    # if another community is specified, a logical OR is apply be zenodo API,
    # thus potentially finding entries that are not part of escape2020
    # ruling out that possibility at the moment
    kwargs['communities'] = escape_community

    return get_zenodo_records(search, sandbox=sandbox, **kwargs)

