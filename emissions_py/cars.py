from dataclasses import dataclass
from typing import List, Dict

@dataclass(frozen=True)
class Cars:
    id: str
    adjusted_mass: float
    total_ceu_road: int
    count: int

    @classmethod
    def builder(cls, id: str, car_attributes: List[Dict[str, float]]) -> 'Cars':
        total_ceu_road = 0
        
        for car in car_attributes:
            # Base values
            base_mass = 1400
            base_height = 1500
            base_length = 4000
            
            # Calculate excess values
            extra_mass = max(0, car['mass'] - base_mass)
            extra_height = max(0, car['height'] - base_height)
            extra_length = max(0, car['length'] - base_length)
            
            # Calculate CEU-Road
            ceu_road = 10
            ceu_road += extra_mass / 250
            ceu_road += (extra_length / 500) * (extra_height / 300)
            
            # Round to nearest whole number and add to total
            total_ceu_road += round(ceu_road)
        
        # Calculate adjusted mass
        adjusted_mass = total_ceu_road * 0.18
        
        return cls(id=id, adjusted_mass=adjusted_mass, total_ceu_road=total_ceu_road, count=len(car_attributes))