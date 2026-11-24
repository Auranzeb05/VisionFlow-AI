class TrafficDensity:
    def calculate(self, vehicle_count):

        if vehicle_count < 10:
            return "LOW"

        elif vehicle_count < 30:
            return "MEDIUM"

        else:
            return "HIGH"
