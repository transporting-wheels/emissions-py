from typing import NamedTuple, List, Set
from collections import defaultdict

class Stop(NamedTuple):
    location: str
    load_cars: Set[str] = set()
    unload_cars: Set[str] = set()

class Journey:
    def __init__(self, stops: List[Stop], distances: List[float], return_trip: bool):
        if len(stops) < 2:
            raise ValueError("A journey must have at least 2 stops")
        if return_trip and len(distances) != len(stops):
            raise ValueError("For a return trip, number of distances must equal number of stops")
        if not return_trip and len(distances) != len(stops) - 1:
            raise ValueError("For a one-way trip, number of distances must be equal to number of stops minus 1")
        
        self._stops = tuple(stops)
        self._distances = tuple(distances)
        self._return_trip = return_trip
    
    def __post_init__(self):
        self.validate_journey()

    @property
    def stops(self) -> tuple:
        return self._stops

    @property
    def distances(self) -> tuple:
        return self._distances

    @property
    def return_trip(self) -> bool:
        return self._return_trip

    def validate_journey(self):
        loaded_cars = set()
        unloaded_cars = set()
        car_locations = defaultdict(list)

        for i, stop in enumerate(self._stops):
            if stop.load_cars.intersection(stop.unload_cars):
                raise ValueError(f"Cars cannot be loaded and unloaded at the same stop: {stop.location}")

            loaded_cars.update(stop.load_cars)
            unloaded_cars.update(stop.unload_cars)

            for car in stop.load_cars:
                car_locations[car].append(i)
            for car in stop.unload_cars:
                car_locations[car].append(i)

        if loaded_cars != unloaded_cars:
            raise ValueError("All loaded cars must be unloaded")

        for car, locations in car_locations.items():
            if len(locations) != 2:
                raise ValueError(f"Car {car} must be loaded once and unloaded once")
            if locations[0] >= locations[1]:
                raise ValueError(f"Car {car} must be loaded before it is unloaded")

    def total_distance(self) -> float:
        return sum(self._distances)

    def empty_trip_factor(self) -> float:
        total_distance = self.total_distance()
        empty_distance = 0
        cars_on_board = set()

        for i, (stop, distance) in enumerate(zip(self._stops, self._distances)):
            if not cars_on_board and not stop.load_cars:
                empty_distance += distance
            cars_on_board.update(stop.load_cars)
            cars_on_board.difference_update(stop.unload_cars)

        # Check if the return trip (last leg) is empty
        if self._return_trip and not cars_on_board:
            empty_distance += self._distances[-1]

        return empty_distance / total_distance

    def __repr__(self):
        return f"Journey(stops={self._stops}, distances={self._distances}, return_trip={self._return_trip})"
    
    @classmethod
    def point_to_point(cls, start: str, end: str, cars: Set[str], distance: float, return_trip: bool = False):
        """
        Create a point-to-point journey.
        
        :param start: Starting location
        :param end: Ending location
        :param cars: Set of cars to be transported
        :param distance: Distance between start and end
        :return: Journey instance
        """

        return cls(
            [
                Stop(start, load_cars=cars),
                Stop(end, unload_cars=cars)
            ],
            [distance, distance] if return_trip else [distance],
            return_trip=return_trip
        )

    @classmethod
    def multi_stop(cls, stops: List[Stop], distances: List[float], return_trip: bool = False):
        """
        Create a multi-stop journey.
        
        :param stops: List of Stop instances
        :param distances: List of distances between consecutive stops
        :return: Journey instance
        """
        return cls(stops, distances, return_trip=return_trip)

    @classmethod
    def ftl(cls, start: str, end: str, cargo: str, distance: float, return_trip: bool = False):
        """
        Create a Full Truck Load (FTL) journey.
        
        :param start: Starting location
        :param end: Ending location
        :param cargo: Description of the full load cargo
        :param distance: Distance between start and end
        :return: Journey instance
        """
        return cls([
            Stop(start, load_cars={cargo}),
            Stop(end, unload_cars={cargo})
        ], [distance], return_trip=return_trip)

    @classmethod
    def ltl(cls, stops: List[Stop], distances: List[float], return_trip: bool = False):
        """
        Create a Less Than Truck Load (LTL) journey.
        
        :param stops: List of Stop instances representing multiple pickups and drop-offs
        :param distances: List of distances between consecutive stops
        :return: Journey instance
        """
        return cls(stops, distances, return_trip=return_trip)