import enum
from pydantic import BaseModel

from src.app.models.institution import Institution


class InstitutionSortBy(str, enum.Enum):
    ID = "id"
    NAME = "name"
    EMAIL = "email"

class InstitutionCreateSch(BaseModel):
    name: str
    email: str
    address: str
    contact_number: str

    def fill_entity(self, entity: Institution):
        entity.name = self.name
        entity.email = self.email
        entity.address = self.address
        entity.contact_number = self.contact_number

class InstitutionUpdateSch(InstitutionCreateSch):
    id: int

class InstitutionSch(BaseModel):
    id: int
    name: str
    email: str
    address: str
    contact_number: str | None

    @staticmethod
    def from_entity(entity: Institution):
        return InstitutionSch(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            address=entity.address,
            contact_number=entity.contact_number
        )

class InstitutionDropDown(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_entity(entity: Institution) -> "InstitutionDropDown":
        return InstitutionDropDown(
            id=entity.id,
            name=entity.name
        )

