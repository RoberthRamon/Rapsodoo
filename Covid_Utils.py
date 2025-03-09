from datetime import datetime

def convert_valid_date(date_string ):
    """
    Checks if a string is a valid date by trying multiple formats and convert in correct date JSON

    :param date_string: The string to verify and for convert in date JSON
    :return: date JSON or None
    """
    ##################################
    # TODO: The time is important
    ##################################

    #formats: List of formats to test
    formats=["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y","%d/%m/%Y"]
    for fmt in formats:
        try:
            date=datetime.strptime(date_string, fmt).strftime("%Y-%m-%dT%H:%M:%S")
            return date
        except ValueError:
            continue
    return None

