from astropy.constants import G, c, sigma_sb, L_bol0
from astropy.modeling.physical_models import BlackBody
from astropy.units import K, kg, m
from astroquery.simbad import Simbad
from numpy import log10, pi


class GroupMember:
    def __init__(self, name, position, **kwargs):
        """
        A class to hold information about an Observational Astrophysics group
        member.

        Parameters
        ----------
        name: str
            The group member's full name.
        position: str
            The group member's position, e.g., "Lecturer", "PhD student".

        Optional parameters
        -------------------
        phone: str
            The group member's phone number.
        office: str
            The group member's office number.
        favourite_object: int, str
            The group member's favourite astronomical object.
        T: float
            The group member's black body temperature. Defaults to 0 K.
        mass: float
            The group member's mass (kg).
        height: float
            The group member's height (m).
        """

        self.name = name
        self.position = position

        # set optional attributes
        self.phone = kwargs.get("phone", None)
        self.office = kwargs.get("office", None)
        self.favourite_object = kwargs.get("favourite_object", None)
        self.T = kwargs.get("T", 0)
        self.mass = kwargs.get("mass", None)
        self.height = kwargs.get("height", None)

    def __str__(self):
        return f"{self.name}: {self.position}"

    @property
    def email(self):
        """
        The group member's email address.
        """

        names = self.name.split()
        initial = names[0][0].lower()
        surname = names[1].strip().lower()

        em = f"{initial}.{surname}@lancaster.ac.uk"

        return em

    @property
    def phone(self):
        """
        The group member's phone number
        """

        return self._phone

    @phone.setter
    def phone(self, phonenum):
        if phonenum is None:
            self._phonenum = None
        else:
            try:
                int(phonenum.replace(" ", ""))
            except ValueError:
                raise ValueError("The phone number must consist entirely of numbers")

            self._phone = phonenum

    @property
    def favourite_object(self):
        """
        The SIMBAD query information for the group member's favourite object.
        """

        if self._favourite_object is None:
            return None

        try:
            result_table = Simbad.query_object(self._favourite_object)
        except Exception as e:
            raise ValueError(f"Object could not be found using SIMBAD: {e}")

        return result_table

    @favourite_object.setter
    def favourite_object(self, favob):
        if favob is None or isinstance(favob, str):
            self._favourite_object = favob
        else:
            raise TypeError("Favourite object must be a string")

    @property
    def T(self):
        """
        The group member's black-body temperature.
        """

        return self._T

    @T.setter
    def T(self, T):
        if not isinstance(T, (float, int)):
            raise TypeError("Temperature must be a positive number")

        if T < 0.0:
            raise TypeError("Temperature must be a positive number")

        self._T = T * K

        # get astropy Black Body object
        self._bb = BlackBody(self._T)

    @property
    def mass(self):
        """
        The group member's mass in kg.
        """

        return self._mass

    @mass.setter
    def mass(self, mass):
        if mass is None:
            self._mass = None
        elif not isinstance(mass, (float, int)):
            raise TypeError("Mass must be a number")
        else:
            if mass < 0.0:
                raise ValueError("Mass must be a positive number")

            self._mass = mass * kg

    @property
    def height(self):
        """
        The group member's height in m.
        """

        return self._height

    @height.setter
    def height(self, height):
        if height is None:
            self._height = None
        elif not isinstance(height, (float, int)):
            raise TypeError("Height must be a number")
        else:
            if height <= 0.0:
                raise ValueError("Height must be a positive number")

            self._height = height * kg

    @property
    def bolometric_flux(self):
        """
        The group member's bolometric flux based on their black body
        temperature.
        """

        return self._bb.bolometric_flux

    @property
    def bolometric_luminosity(self):
        """
        The group member's bolometric luminosity based on their black body
        temperature and assuming they are a cylinder with a diameter of 30 cm
        and a length given by their height.
        """

        if self.height is None:
            return None

        surfarea = pi * 0.15 ** 2 * self.height

        return sigma_sb * surfarea * self.T ** 4

    @property
    def absolute_magnitude(self):
        """
        The group members absolute bolometric magnitude assuming they are a
        black body.
        """

        if self.bolometric_luminosity is None:
            return None

        return -2.5 * log10(self.bolometric_luminosity.value / L_bol0.value)

    @property
    def schwarschild_radius(self):
        """
        The group member's Schwarschild radius based on their mass.
        """

        if self.mass is None:
            return None
        else:
            return 2 * self.mass * G / c ** 2
