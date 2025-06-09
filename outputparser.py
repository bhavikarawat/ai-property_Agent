from typing import List, Dict, Any
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field


class Property(BaseModel):
    id: int=Field(description="Property ID")
    name: str=Field(description="Name of the property")
    address: str=Field(description="Complete address of property")
    rent_per_sq_feet: str=Field(description="Rent per square feet area")
    size_sqft: str=Field(description="Area Available")

    def to_dict(self) -> Dict[str, Any]:
        return {"Prop_id": self.id, "address": self.address,"rent":self.rent_per_sq_feet,"Area Available":self.size_sqft}


class FilteredProperties(BaseModel):
    properties: List[Property]

parser=PydanticOutputParser(pydantic_object=FilteredProperties)
