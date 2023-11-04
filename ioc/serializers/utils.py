from constants.ioc import LIST_IOC


def material_ioc_validate(data):
    """Method that validates if the ioc material has all the required fields"""
    missing = [element for element in LIST_IOC if element not in data]
    return missing
