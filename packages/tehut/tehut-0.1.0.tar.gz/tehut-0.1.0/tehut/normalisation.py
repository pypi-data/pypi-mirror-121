import time
from typing import Union
import warnings
import requests
from more_itertools import distribute

CAB_URL = 'https://www.deutschestextarchiv.de/public/cab/query?clean=1&qname=q&a=default&fmt=raw&file=C%3A%5Cfakepath%5Ctest.txt'
CAB_HEADERS = headers = {'Content-Type': 'text/plain'}


def cab(text: str, delay: Union[float, None] = None) -> Union[str, None]:

    """
    Queries the CAB-Webservice provided by Deutsches Textarchiv for orthographic normalisation.
    If you use this function repeatedly (e.g. in a loop), please use with delay parameter to avoid overloading the server.
    If a texts exceeds the size of one megabyte, it is split into smaller parts
    and then sent to the service iteratively.
    """

    if delay is not None:
        time.sleep(delay)

    n_megabytes = len(text.encode('utf-8')) // 1000000

    if n_megabytes >= 1:
        parts = list(distribute(n=n_megabytes+1, iterable=text.split(' ')))
        parts = [' '.join(part) for part in parts]
    else:
        parts = [text]

    normed_parts = []
    for part in parts:
        r = requests.post(url=CAB_URL, headers=CAB_HEADERS,
                          data=part.encode('UTF-8'))

        if r.status_code != 200:
            warnings.warn(
                f'Request returned with error code {r.status_code}\nError Message\n{r.body}')
            return None

        normed_parts.append(r.text.strip())

    return ' '.join(normed_parts)


if __name__ == '__main__':
    print(cab("Du seyst ein Theil fon mir!"))
    print(cab("Du seyst ein Theil fon mir!", delay=3.0))
