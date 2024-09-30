from dataclasses import dataclass

@dataclass
class Truck:
    id: str
    vehicle_type: str
    fuel_type: str
    wtt_factor: float # in grams
    ttw_factor: float # in grams
    gross_vehicle_weight: float  # in tonnes
    payload_capacity: float  # in tonnes
    info_source: str

    @property
    def empty_weight(self) -> float:
        return self.gross_vehicle_weight - self.payload_capacity
    
    @property
    def wtw_factor(self) -> float:
        return self.wtt_factor + self.ttw_factor

@dataclass(frozen=True)
class Trucks:

    @staticmethod
    def light_duty_van_diesel(id: str) -> Truck:
        return Truck(
            id=id,
            vehicle_type='Light-duty van (<3.5t)', 
            fuel_type='Diesel', 
            wtt_factor=50, 
            ttw_factor=180, 
            gross_vehicle_weight=3.5, 
            payload_capacity=2, 
            info_source='DEFRA (2023), EEA (2022)'
        )

    @staticmethod
    def medium_duty_truck_diesel(id: str) -> Truck:
        return Truck(
            id=id,
            vehicle_type='Medium-duty truck (7.5–16t)', 
            fuel_type='Diesel', 
            wtt_factor=25, 
            ttw_factor=85, 
            gross_vehicle_weight=16, 
            payload_capacity=8, 
            info_source='DEFRA (2023)'
        )

    @staticmethod
    def heavy_duty_truck_diesel(id: str) -> Truck:
        return Truck(
            id=id,
            vehicle_type='Heavy-duty truck (>16t)', 
            fuel_type='Diesel', 
            wtt_factor=15, 
            ttw_factor=75, 
            gross_vehicle_weight=18, 
            payload_capacity=10, 
            info_source='DEFRA (2023), EEA (2022)'
        )
    
    @staticmethod
    def heavy_duty_truck_lng(id: str) -> Truck:
        return Truck(
            id=id,
            vehicle_type='Heavy-duty truck (>16t)', 
            fuel_type='LNG', 
            wtt_factor=35, 
            ttw_factor=45, 
            gross_vehicle_weight=18, 
            payload_capacity=10, 
            info_source='EcoTransIT World'
        )
    
    @staticmethod
    def articulated_truck_diesel(id: str) -> Truck:
        return Truck(
            id=id,
            vehicle_type='Articulated truck (40t)', 
            fuel_type='Diesel', 
            wtt_factor=20, 
            ttw_factor=55, 
            gross_vehicle_weight=40, 
            payload_capacity=25, 
            info_source='DEFRA (2023), EcoTransIT World'
        )
    
    @staticmethod
    def electric_van(id: str) -> Truck:
        return Truck(
            id=id,
            vehicle_type='Light-duty van (<3.5t)', 
            fuel_type='Electric', 
            wtt_factor=80,  # Assuming high grid emissions
            ttw_factor=0, 
            gross_vehicle_weight=3.5, 
            payload_capacity=2, 
            info_source='DEFRA (2023), EEA (2022)'
        )
    
    @staticmethod
    def electric_heavy_truck(id: str) -> Truck:
        return Truck(
            id=id,
            vehicle_type='Heavy-duty truck (>16t)', 
            fuel_type='Electric', 
            wtt_factor=50,  # Assuming moderate grid mix
            ttw_factor=0, 
            gross_vehicle_weight=18, 
            payload_capacity=10, 
            info_source='DEFRA (2023), EEA (2022)'
        )