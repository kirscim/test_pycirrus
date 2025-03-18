import pycontrails

# Example function to apply CoCiP model

def apply_cocip():
    # Initialize CoCiP model
    cocip = pycontrails.Cocip()

    # Define some example input data
    # This should be replaced with actual flight data
    flight_data = {
        'latitude': [50.0, 51.0],
        'longitude': [-0.1, -0.2],
        'altitude': [35000, 36000],  # in feet
        'time': ['2025-03-18T10:00:00Z', '2025-03-18T11:00:00Z']
    }

    # Apply CoCiP model to the flight data
    contrail_results = cocip.run(flight_data)

    # Print the results
    print("Contrail Results:")
    for result in contrail_results:
        print(result)

if __name__ == "__main__":
    apply_cocip()
