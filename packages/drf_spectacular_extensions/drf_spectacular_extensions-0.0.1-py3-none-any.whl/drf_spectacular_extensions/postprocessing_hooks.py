from typing import Optional
from urllib.parse import urlparse

from drf_spectacular.generators import SchemaGenerator
from rest_framework.request import Request


def add_servers(
    result: dict,
    generator: SchemaGenerator,
    request: Optional[Request],
    public: bool,
) -> dict:
    if request:
        parsed_uri = urlparse(request.get_raw_uri())
        result["servers"] = [{"url": f"{parsed_uri.scheme}://{request.get_host()}/"}]
    return result
