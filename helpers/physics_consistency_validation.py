class PhysicsConsistencyValidation:
    def __init__(self, namelist):
        self.namelist = namelist
        self.errors = []

    def validate_physics_consistency(self):
        try:
            microphysics_scheme = self.namelist['physics']['mp_physics']
            radiation_scheme = self.namelist['physics']['ra_lw_physics']
            pbl_scheme = self.namelist['physics']['bl_pbl_physics']
            sf_layer_scheme = self.namelist['physics']['sf_sfclay_physics']

            # Verify compatibility between microphysics and radiation schemes
            if microphysics_scheme in ['thompson', 'morrison']:
                if radiation_scheme not in [1, 4, 5]:
                    self.errors.append("The selected radiation scheme is not compatible with the chosen microphysics scheme.")

            # Verify compatibility between PBL and surface-layer schemes
            if pbl_scheme == 'ysu' and sf_layer_scheme != 'mm5':
                self.errors.append("The YSU PBL scheme is designed to work with the MM5 surface-layer scheme.")
            elif pbl_scheme == 'myj' and sf_layer_scheme != 'eta':
                self.errors.append("The MYJ PBL scheme is designed to work with the Eta surface-layer scheme.")
            # Add more compatibility checks if necessary

        except KeyError as e:
            self.errors.append(f"Missing key in namelist: {e}")