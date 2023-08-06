from .ip_api import IPInfoApi


def test_ip_info():
    api = IPInfoApi(fields=["query", "status", "country", "city"])
    info = api.get_ip_info("1.1.1.1")
    assert info.is_success()
