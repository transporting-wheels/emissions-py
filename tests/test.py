from emissions_py import Cars, EmissionsCalculator, Journey, Truck, Trucks, Stop

def test_point_to_point_heavy_diesel():
    truck = Trucks.heavy_duty_truck_diesel(id="T001")

    journey = Journey.point_to_point(
        start = "Hub LSP", 
        end = "Unloading Point VW",
        cars=["vw-golf", "vw-passat-tdi", "vw-passat-gte"],
        distance=40,
    )

    cars = [
        Cars('vw-golf', 1.8, 10, 3),
        Cars('vw-passat-tdi', 1.98, 11, 2),
        Cars('vw-passat-gte', 2.16, 12, 2),
    ]

    emissions = EmissionsCalculator().calculate_emissions(truck, journey, cars)

    assert round(emissions['total_emissions_wtw']) == 49

def test_multi_stop_car_carrier_bio_fuel():
    truck = Truck(
        id="T001",
        vehicle_type="Car Carrier",
        fuel_type="Diesel, B100 (100 % Bio-Diesel-share)",
        wtt_factor=100,
        ttw_factor=0,
        gross_vehicle_weight=40, 
        payload_capacity=26, 
        info_source='DEFRA (2023), EEA (2022)',
    )

    journey = Journey.multi_stop(
        [
            Stop('Hub LSP', set(['vw', 'ford', 'audi']), set()),
            Stop('Unloading Point VW', set(), set(['vw'])),
            Stop('Unloading Point Ford', set(), set(['ford'])),
            Stop('Unloading Point Audi', set(), set(['audi'])),
        ],
        [50, 15, 30],
        return_trip=False
    )

    cars = [
        Cars('vw', 1.8, 10, 2),
        Cars('ford', 6.3, 35, 1),
        Cars('audi', 2.34, 13, 2),
    ]

    emissions = EmissionsCalculator().calculate_emissions(truck, journey, cars)

    assert round(emissions['total_emissions_wtw']) == 103