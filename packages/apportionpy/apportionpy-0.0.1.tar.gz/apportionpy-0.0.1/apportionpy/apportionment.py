from apportionpy.methods.adam import calculate_adam
from apportionpy.methods.hamilton import calculate_hamilton
from apportionpy.methods.jefferson import calculate_jefferson
from apportionpy.methods.webster import calculate_webster


class Apportion:
    def __init__(self, seats, populations, method):
        """
        Initialize variables.

        :param seats: Amount of seats to apportion.
        :type seats: int

        :param populations: The populations of each state respectively.
        :type populations: [float]

        :param method: The apportioning method to be used.
        :type method: str
        """

        self.seats = seats
        self.populations = populations
        self.method = method.lower()

        if method.upper() == "ADAM":
            self.initial_fair_shares, self.final_fair_shares, self.initial_quotas, self.final_quotas, \
            self.initial_divisor, self.modified_divisor = calculate_adam(self.seats, self.populations)
        elif method.upper() == "HAMILTON":
            self.initial_fair_shares, self.final_fair_shares, self.initial_quotas, self.final_quotas, \
            self.initial_divisor, self.modified_divisor = calculate_hamilton(self.seats, self.populations)
        elif method.upper() == "JEFFERSON":
            self.initial_fair_shares, self.final_fair_shares, self.initial_quotas, self.final_quotas, \
            self.initial_divisor, self.modified_divisor = calculate_jefferson(self.seats, self.populations)
        elif method.upper() == "WEBSTER":
            self.initial_fair_shares, self.final_fair_shares, self.initial_quotas, self.final_quotas, \
            self.initial_divisor, self.modified_divisor = calculate_webster(self.seats, self.populations)
        else:
            error_message = "\"" + method + "\" is not a valid method."
            raise Exception(error_message)