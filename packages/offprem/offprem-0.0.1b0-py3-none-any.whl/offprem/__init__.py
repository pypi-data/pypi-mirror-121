"""
Python package created to automate auditing tasks for resources that live in the cloud.
"""

__version__ = '0.0.1'

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler
from offprem.offprem import (VirtualPrivateCloud, Profile, ConfigureCredentials, ConfigureVPC, AWSPremise,
                             SecurityTokenService)

logging.getLogger(__name__).addHandler(NullHandler())
