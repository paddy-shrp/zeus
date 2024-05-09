import requests

class RequestsWrapper:
    def __init__(self, base_url):
        """
        Initializes the wrapper with a base URL.
        
        :param base_url: The base URL for all API requests.
        """
        self.base_url = base_url

    def request(self, path, method="GET", headers=None, params=None, data=None, json=None):
        """
        General method to send HTTP requests.
        
        :param method: HTTP method ('GET', 'POST', 'PUT', etc.)
        :param path: The URL path to append to the base URL.
        :param params: Dictionary of URL parameters for GET requests.
        :param data: Dictionary, bytes, or file-like object to send in the body of POST/PUT requests.
        :param json: JSON object to send in the body of POST/PUT requests.
        :return: Response object or None if an error occurred.
        """
        if path.startswith("/"):
            path = path[1:]

        url = f"{self.base_url}{path}"
        try:
            response = requests.request(method, url, headers=headers, params=params, data=data, json=json)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None