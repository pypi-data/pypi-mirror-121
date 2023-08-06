from astropy.constants import G, c
from astropy.modeling.physical_models import BlackBody
from astropy.units import K, kg
from astroquery.simbad import Simbad


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
        """

        self.name = name
        self.position = position

        # set optional attributes
        self.phone = kwargs.get("phone", None)
        self.office = kwargs.get("office", None)
        self.favourite_object = kwargs.get("favourite_object", None)
        self.T = kwargs.get("T", 0)
        self.mass = kwargs.get("mass", None)

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
    def bolometric_flux(self):
        """
        The group member's bolometric flux based on their black body
        temperature.
        """
        
        return self._bb.bolometric_flux

    @property
    def schwarschild_radius(self):
        """
        The group member's Schwarschild radius based on their mass.
        """
        
        if self.mass is None:
            return None
        else:
            return 2 * self.mass * G / c ** 2

