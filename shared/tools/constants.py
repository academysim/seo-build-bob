# -*- coding: utf-8 -*-
"""Shared constants for the academy-seo-build toolchain.

Centralises values that appear in more than one script so that a single change
propagates everywhere.  Import with:

    import sys, os
    sys.path.insert(0, os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', '..'
    )))
    from shared.tools.constants import GA4_TAG, HOSTS, ADDRESS, PHONE, EMAIL

Scripts under shared/tools/ can use ROOT directly after computing it from HERE.
"""

# Google Analytics 4 measurement ID, shared across all five properties.
GA4_TAG = 'G-SQL40ZS59K'

# Production base URLs for the five managed properties.
HOSTS = {
    'lounge': 'https://lounge.academysim.com',
    'events': 'https://events.academysim.com',
    'builds': 'https://builds.academysim.com',
    'driver': 'https://driver.academysim.com',
    'health': 'https://health.academysim.com',
}

# NAP (Name / Address / Phone) contact details.
# Granular parts are exposed so each add_hub_links.py can assemble the
# exact byte sequence its template already uses without reformatting.
STREET       = '1421 Massaro Blvd'
CITY         = 'Tampa'
STATE        = 'FL'
ZIP_CODE     = '33619'
# Two pre-assembled address strings used by different properties:
#   "Tampa FL 33619"  — no comma before FL, used by lounge footer
#   "Tampa, FL 33619" — comma before FL, used by events/health/builds footers
CITY_STATE_ZIP       = '%s, %s %s' % (CITY, STATE, ZIP_CODE)   # Tampa, FL 33619
CITY_STATE_ZIP_LOUNGE = '%s %s %s' % (CITY, STATE, ZIP_CODE)   # Tampa FL 33619
# Full one-liner addresses
ADDRESS        = '%s, %s' % (STREET, CITY_STATE_ZIP)        # 1421 Massaro Blvd, Tampa, FL 33619
ADDRESS_LOUNGE = '%s, %s' % (STREET, CITY_STATE_ZIP_LOUNGE) # 1421 Massaro Blvd, Tampa FL 33619

PHONE      = '(813) 355-9071'
PHONE_E164 = '+18133559071'
EMAIL      = 'info@academysim.com'
