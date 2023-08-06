from pytmosph3r.log import Logger
from pytmosph3r.constants import G, RSOL, MSOL
import numpy as np
import astropy.units as u

class Star(Logger):
    """ Star (blackbody) properties.

    Args:
        temperature (float, optional): Stellar temperature (`K`)
        radius (float, optional): Stellar radius (by default in `solar radius`, see :py:attr:`r_units` for changing the units)
        mass (float, optional): Stellar mass (by default in `solar mass`, see :py:attr:`m_units` for changing the units)
        r_units (str, optional): Length unit for the radius ('m' for meters, 'Rsun' for solar radius, i.e., 695700000 m, ...). See https://docs.astropy.org/en/stable/units/index.html#module-astropy.units for more units.
        m_units (str, optional): Mass unit ('kg' for kilograms, 'Msun' for solar mass, i.e., :math:`1.9884099×10^{30} m`, ...). See https://docs.astropy.org/en/stable/units/index.html#module-astropy.units for more units.
    """

    def __init__(self, temperature=5000, radius=1.0, mass=1.0, r_units='Rsun', m_units='Msun'):

        Logger.__init__(self, self.__class__.__name__)
        self.temperature = temperature
        try:
            to_meters = u.Unit(r_units).to(u.m)
        except:
            to_meters = u.Unit(r_units, format="cds").to(u.m)
        self.radius = radius * to_meters
        """ Planet radius (in `m`)."""

        try:
            to_kg = u.Unit(m_units).to(u.kg)
        except:
            to_kg = u.Unit(m_units, format="cds").to(u.kg)
        self.mass = mass * to_kg
        """ Planet mass (in `kg`)."""
        self.r_units = 'm'
        self.m_units = 'kg'

    @property
    def mass_sol(self):
        """ Planet mass (in `solar mass`)."""
        try:
            return self.mass/MSOL
        except:
            return None

    @property
    def radius_sol(self):
        """ Planet radius (in `solar radii`)."""
        try:
            return self.radius/RSOL
        except:
            return None

    def inputs(self):
        return ['temperature', 'radius', 'mass', 'r_units', 'm_units']

class BlackbodyStar(Star):
    """Alias for the base star type"""
    pass