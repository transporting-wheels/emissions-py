from typing import List
from .journey import Journey
from .truck import Truck
from .cars import Cars

class EmissionsCalculator:
    def calculate_emissions(self, truck: Truck, journey: Journey, cars: List[Cars]):
        legs = []
        cars_on_board = set()
        print(cars_on_board)

        # Function to calculate leg emissions
        def calculate_leg(distance, current_cars_on_board):
            leg_mass = sum(car.adjusted_mass * car.count for car in cars if car.id in current_cars_on_board)
            leg_ceu = sum(car.total_ceu_road for car in cars if car.id in current_cars_on_board)

            transport_activity = leg_mass * distance / 1000 # Convert to kg

            total_emissions_wtt = truck.wtt_factor * transport_activity
            total_emissions_ttw = truck.ttw_factor * transport_activity
            total_emissions_wtw = truck.wtw_factor * transport_activity

            car_assignment = {}
            for car in cars:
                assignment = car.total_ceu_road / leg_ceu
                car_assignment[car.id] = {
                    'assignment': assignment,
                    'wtt_emissions': assignment * total_emissions_wtt,
                    'ttw_emissions': assignment * total_emissions_ttw,
                    'wtw_emissions': assignment * total_emissions_wtw,
                    'wtt_emissions_per_car': (assignment / car.count) * total_emissions_wtt,
                    'ttw_emissions_per_car': (assignment / car.count) * total_emissions_ttw,
                    'wtw_emissions_per_car': (assignment / car.count) * total_emissions_wtw,
                } if car.id in cars_on_board else {
                    'assignment': 0,
                    'wtt_emissions': 0,
                    'ttw_emissions': 0,
                    'wtw_emissions': 0,
                    'wtt_emissions_per_car': 0,
                    'ttw_emissions_per_car': 0,
                    'wtw_emissions_per_car': 0,
                }

            return {
                'cars': list(cars_on_board),
                'distance': distance,
                'leg_mass': leg_mass,
                'utilization_rate': leg_mass / truck.payload_capacity,
                'transport_activity': transport_activity,
                'total_emissions_wtt': total_emissions_wtt,
                'total_emissions_ttw': total_emissions_ttw,
                'total_emissions_wtw': total_emissions_wtw,
                'assignment': car_assignment,
            }

        # Forward journey
        for i in range(len(journey.stops) - 1):
            cars_on_board = cars_on_board.union(journey.stops[i].load_cars)
            cars_on_board = cars_on_board.difference(journey.stops[i].unload_cars)
            legs.append(calculate_leg(journey.distances[i], cars_on_board))

        # Return journey if specified
        if journey.return_trip:
            cars_on_board.clear()  # Empty the truck for the return trip
            legs.append(calculate_leg(journey.distances[-1], cars_on_board))

        total_emissions_wtt = sum(leg['total_emissions_wtt'] for leg in legs)
        total_emissions_ttw = sum(leg['total_emissions_ttw'] for leg in legs)
        total_emissions_wtw = sum(leg['total_emissions_wtw'] for leg in legs)

        emissions_per_car = {car.id : {
            'wtt_emissions': sum(leg['assignment'][car.id]['wtt_emissions'] for leg in legs),
            'ttw_emissions': sum(leg['assignment'][car.id]['ttw_emissions'] for leg in legs),
            'wtw_emissions': sum(leg['assignment'][car.id]['wtw_emissions'] for leg in legs),
        } for car in cars}

        return {
            'total_emissions_wtt': total_emissions_wtt,
            'total_emissions_ttw': total_emissions_ttw,
            'total_emissions_wtw': total_emissions_wtw,
            'emissions_per_leg': legs,
            'emissions_per_car': emissions_per_car
        }