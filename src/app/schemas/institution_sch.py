from pydantic import BaseModel

from src.app.models.institution import Institution


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

class InstitutionSch(BaseModel):
    id: int
    name: str
    email: str
    address: str
    contact_number: str

    @staticmethod
    def from_entity(entity: Institution):
        return InstitutionSch(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            address=entity.address,
            contact_number=entity.contact_number
        )
