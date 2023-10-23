class VerticalCoordinateValidation:
    def __init__(self, namelist):
        self.namelist = namelist
        self.errors = []

    def validate_vertical_levels(self):
        try:
            num_metgrid_levels = self.namelist['geogrid']['num_metgrid_levels']

            if not isinstance(num_metgrid_levels, int) or num_metgrid_levels <= 0:
                self.errors.append("Number of vertical levels (num_metgrid_levels) must be a positive integer.")
        except KeyError as e:
            self.errors.append(f"Missing key in namelist: {e}")

    def validate_top_model_level(self):
        try:
            p_top_requested = self.namelist['geogrid']['p_top_requested']

            if not (isinstance(p_top_requested, int) or isinstance(p_top_requested, float)) or p_top_requested <= 0:
                self.errors.append("Top model level pressure (p_top_requested) must be a positive number.")
        except KeyError as e:
            self.errors.append(f"Missing key in namelist: {e}")

    def validate_coordinate_system(self):
        try:
            vcoord = self.namelist['geogrid']['vcoord']
            eta_levels = self.namelist['geogrid']['eta_levels']
            sigma_levels = self.namelist['geogrid']['sigma_levels']
            hybrid_levels = self.namelist['geogrid']['hybrid_levels']

            if vcoord.lower() == 'eta':
                if eta_levels is None or len(eta_levels) == 0:
                    self.errors.append("Eta levels must be specified when using the eta vertical coordinate system.")
                else:
                    for level in eta_levels:
                        if not (0 <= level <= 1):
                            self.errors.append("Eta levels should be within the range of 0 to 1.")
            elif vcoord.lower() == 'sigma':
                if sigma_levels is None or len(sigma_levels) == 0:
                    self.errors.append("Sigma levels must be specified when using the sigma vertical coordinate system.")
                else:
                    for level in sigma_levels:
                        if not (0 <= level <= 1):
                            self.errors.append("Sigma levels should be within the range of 0 to 1.")
            elif vcoord.lower() == 'hybrid':
                if hybrid_levels is None or len(hybrid_levels) == 0:
                    self.errors.append("Hybrid levels must be specified when using the hybrid vertical coordinate system.")
                else:
                    for level in hybrid_levels:
                        if not (0 <= level <= 1):
                            self.errors.append("Hybrid levels should be within the range of 0 to 1.")
            else:
                self.errors.append("Invalid vertical coordinate system specified. Options are 'eta', 'sigma', or 'hybrid'.")

        except KeyError as e:
            self.errors.append(f"Missing key in namelist: {e}")



    def run_validation(self):
        self.validate_vertical_levels()
        self.validate_top_model_level()
        self.validate_coordinate_system()
