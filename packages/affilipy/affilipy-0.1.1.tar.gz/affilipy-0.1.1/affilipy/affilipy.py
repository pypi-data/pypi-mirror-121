def replace(service_name, url, your_key):
    """
    """
    replaced_url = ''
    if service_name == "amazon":
        from .amazon import amazon
        replaced_url = amazon.replace(url, your_key)
    else:
        raise('implamented service')

    return replaced_url

