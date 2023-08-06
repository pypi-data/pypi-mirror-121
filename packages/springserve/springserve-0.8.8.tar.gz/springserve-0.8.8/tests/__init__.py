


import springserve as mock_spring

from mock import MagicMock

def format_url(endpoint, path_param=None, query_params=None):

    _url = endpoint

    if path_param:
        _url += "/{}".format(path_param)

    if query_params and isinstance(query_params, dict):
        params = "&".join(["{}={}".format(key, value) for key,value in
                           query_params.iteritems()])
        _url += "?{}".format(params)

    return _url



class _MockResponse(mock_spring._VDAPIResponse):
    pass

class _MockService(mock_spring._VDAPIService):

    __API__ = "mock_endpoint"
    __RESPONSE_OBJECT__ = _MockResponse


def reset_mock():
    mock_api = MagicMock()

    mock_spring.API = MagicMock(return_value=mock_api)
        
    #allows us to test get, put, post methods
    mock_spring.mock_service = _MockService()

reset_mock()
