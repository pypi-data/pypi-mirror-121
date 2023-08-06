"""
Module responsible for setting up initialization of the hopla entry command.
"""

from hopla.hoplalib.hoplaversion import HoplaVersion

# set version so we can use attr: in setup.cfg
__version__ = HoplaVersion().semantic_version()

try:
    from hopla.kickstart import hopla, kickstart_hopla


    def setup_hopla_application():
        """The entry function for the hopla command"""
        kickstart_hopla()

except ModuleNotFoundError as ex:
    pass
    # This error catching is just here for the `python -m build` call that
    # fails to find click at build time when trying to find __version__.
