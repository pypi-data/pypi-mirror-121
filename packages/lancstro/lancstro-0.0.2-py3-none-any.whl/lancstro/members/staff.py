import json
import os
import pkg_resources

from ..base import GroupMember


class Staff(dict):
    """
    Class to hold staff members.
    """

    def add_member(self, member):
        """
        Add a member of staff to the group.
        """

        if not isinstance(member, GroupMember):
            raise TypeError("New member must be a 'GroupMember' type")

        self[member.name] = member

    @property
    def names(self):
        """
        A list of names of all staff members.
        """

        return list(self.keys())


# load staff office number data
offnumfile = pkg_resources.resource_filename(
    "lancstro",
    os.path.join("data", "office_numbers.txt")
)
with open(offnumfile, "r") as fp:
    officenumbers = json.load(fp)


#: Dictionary of staff members
staff = Staff()
staff.add_member(
    GroupMember(
        "Matthew Pitkin",
        "Lecturer",
        office=officenumbers["Matthew Pitkin"],
        favourite_object="m1",
        T=300,
        mass=72,
        height=1.83,
    )
)
