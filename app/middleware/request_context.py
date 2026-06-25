from contextvars import ContextVar

_source_ip: ContextVar[str] = ContextVar("source_ip", default="")
_endpoint: ContextVar[str] = ContextVar("endpoint", default="")
_destination_ip: ContextVar[str] = ContextVar("destination_ip", default="")


def set_request_context(source_ip: str, endpoint: str, destination_ip: str = ""):
    _source_ip.set(source_ip)
    _endpoint.set(endpoint)
    _destination_ip.set(destination_ip)


def get_request_context() -> dict:
    return {
        "source_ip": _source_ip.get(),
        "endpoint": _endpoint.get(),
        "destination_ip": _destination_ip.get(),
    }
