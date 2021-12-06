"""This module contains common functionality between the server and client.
It may also contain methods that are deemed too out of scope for the server or client"""
import pip

def get_ascii_logo():
    logo_str = "__________       _________ .__            __   \n"
    logo_str = logo_str + "\______   \___.__\_   ___ \|  |__ _____ _/  |_ \n"
    logo_str = logo_str + " |     ___<   |  /    \  \/|  |  \\\\__  \\\\   __\\\n"
    logo_str = logo_str + " |    |    \___  \     \___|   Y  \/ __ \|  |  \n"
    logo_str = logo_str + " |____|    / ____|\______  |___|  (____  |__|  \n"
    logo_str = logo_str + "           \/            \/     \/     \/      \n"
    logo_str = logo_str + "                by Brad and Rhys                 "
    return logo_str


def try_import(package: str):
    """Check that dependency 'package' is installed and if not, install it"""
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])
