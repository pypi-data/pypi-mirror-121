import time
import requests
from . import settings, GQLException

URL = settings.dgraph_url
ACCESS_TOKEN = settings.dgraph_access_token


def execute(query_str: str, should_print: bool = False) -> dict:
    start = time.time()
    j = requests.post(
        URL,
        json={"query": query_str},
        headers={"X-Dgraph-AccessToken": ACCESS_TOKEN},
    ).json()
    print(
        f'took: {(time.time() - start) * 1000}, took internal: {int(j["extensions"]["tracing"]["duration"]) / (10 ** 6)}'
    )
    if should_print:
        print(f"{query_str=}, {j=}")
    if "data" not in j:
        raise GQLException(f"data not in j!, {j=}, {query_str=}")
    return j
