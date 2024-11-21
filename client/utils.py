from .models import Client


def hostname_from_request(request):
    """returns hosts name from request"""
    return request.get_host().split(":")[0].lower()


def root_company():
    return Client.objects.filter(schema_name="public").first()


def company_from_request(request):
    """returns company from current request"""
    if hasattr(request, "cache__company"):
        return request.cache__company

    hostname = hostname_from_request(request)
    # print(hostname)
    company = Client.objects.filter(domain_url=hostname).first()
    setattr(request, "cache__company", company)
    return company


def get_company_domain(request):
    company = company_from_request(request)
    if company:
        return company.domain_url
    else:
        return root_company().domain_url


def get_company_url(request):
    company = company_from_request(request)
    if company:
        if request.is_secure():
            return "https://" + company.domain_url
        return "http://" + company.domain_url
    else:
        return root_company().domain_url
