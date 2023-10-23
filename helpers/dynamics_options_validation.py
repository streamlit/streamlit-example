class DynamicsOptionsValidation:
    def __init__(self, namelist):
        self.namelist = namelist
        self.errors = []

    def validate_advection_schemes(self):
        try:
            h_advection_scheme = self.namelist['dynamics']['h_adv_order']
            v_advection_scheme = self.namelist['dynamics']['v_adv_order']

            # Validate horizontal advection scheme
            if h_advection_scheme not in [2, 3, 5]:
                self.errors.append("Invalid horizontal advection scheme. Options are 2 (2nd order), 3 (3rd order), or 5 (5th order).")

            # Validate vertical advection scheme
            if v_advection_scheme not in [2, 3]:
                self.errors.append("Invalid vertical advection scheme. Options are 2 (2nd order) or 3 (3rd order).")

        except KeyError as e:
            self.errors.append(f"Missing key in namelist: {e}")
