# Emissions Calculator

This is a Python package designed to calculate the emissions for a fleet of trucks transporting various cars. The package includes an emissions calculator that works with different fuel types and supports multi-stop journeys.

## Purpose

The **Emissions Calculator** package calculates the Well-to-Wheel (WTW) emissions for automotyive transporting cars. The package considers factors like fuel type, journey distance, and the types of cars being transported. It is ideal for estimating transport-related emissions for logistics companies or environmental studies.

## Setup

### Prerequisites

Make sure you have Python installed. We recommend using a virtual environment to manage dependencies.

1. Clone the repository:

    ```bash
    git clone https://github.com/transporting-wheels/emissions-py.git
    cd emissions-calculator
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. To run tests, install `pytest`:

    ```bash
    pip install pytest
    ```

4. Run the tests:
    ```bash
    pytest tests
    ```

## Example

Here is an example usage of the emissions calculator:

```python
from emissions import Cars, EmissionsCalculator, Journey, Truck, Trucks

truck = Trucks.heavy_duty_truck_diesel(id="T001")

journey = Journey.point_to_point(
    start="Hub LSP",
    end="Unloading Point VW",
    cars=["vw-golf", "vw-passat-tdi", "vw-passat-gte"],
    distance=40,
)

cars = [
    Cars('vw-golf', 1.8, 10, 3),
    Cars('vw-passat-tdi', 1.98, 11, 2),
    Cars('vw-passat-gte', 2.16, 12, 2),
]

emissions = EmissionsCalculator().calculate_emissions(truck, journey, cars)
print(emissions)
```

This example calculates the emissions for a heavy-duty truck transporting three cars from a start point to an unloading point over a 40-kilometer journey.

## Contribution

We welcome contributions! If you'd like to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Submit a Pull Request.

Ensure all tests pass before submitting your pull request by running:

```bash
pytest
```
