from dataclasses import dataclass
from typing import Dict

@dataclass
class SimpleCard:
    name : str
    supertype : list[str]
    subtype : list[str]

    def __eq__(self, other):
        return isinstance(other, SimpleCard) and self.name == other.name

    def __hash__(self):
        return hash((self.name))

    @staticmethod
    def from_dict(data: Dict) -> 'SimpleCard':
        # Safely split the typeline
        type_parts = data.get("type_line", "").split("—")
        supertype = type_parts[0].strip().split() if len(type_parts) > 0 else []
        subtype = type_parts[1].strip().split() if len(type_parts) > 1 else []

        return SimpleCard(
            name=data.get("name", "Unknown"),
            supertype=supertype,
            subtype=subtype
        )
    
    @staticmethod
    def from_simple(data: Dict) -> 'SimpleCard':
        return SimpleCard(
            name=data.get("name"),
            supertype=data.get("supertype"),
            subtype=data.get("subtype")
        )
    
@dataclass
class TypeData:
    type_name : str
    count : int
    card_names : list[str]

    def __str__(self):
        return f"Creature Type: {self.type_name}\nCount: {self.count}\nCards: {self.card_names}"