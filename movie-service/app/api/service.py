import os
import httpx


def is_cast_present(cast_id: int):
    url = os.environ.get('CAST_SERVICE_HOST_URL')
    r = httpx.get(f'{url}{cast_id}')
    return True if r.status_code == 200 else False