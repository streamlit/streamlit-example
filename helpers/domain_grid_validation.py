class DomainGridValidation:
    def __init__(self, namelist):
        self.errors = []
        self.namelist = namelist

    def validate_grid_size(self):
        try:
            e_we = self.namelist['domains']['e_we']
            e_sn = self.namelist['domains']['e_sn']
            parent_grid_ratio = self.namelist['domains']['parent_grid_ratio']

            if all(x > 0 for x in e_we) and all(x > 0 for x in e_sn):
                for i in range(1, len(e_we)):
                    if e_we[i] <= parent_grid_ratio[i-1] * e_we[i-1] or e_sn[i] <= parent_grid_ratio[i-1] * e_sn[i-1]:
                        self.errors.append({"Child domain grid size must be larger than parent grid ratio times parent domain grid size."})
                        # raise ValueError("Child domain grid size must be larger than parent grid ratio times parent domain grid size.")
            else:
                self.errors.append({f"Grid sizes ({e_we} and {e_sn}) must be positive integers."})
                # raise ValueError("Grid sizes (e_we and e_sn) must be positive integers.")

        except KeyError as e:
            self.errors.append(f"Missing key in namelist: {e}")

    def validate_domain_bounds(self):
        try:
            ref_lat = self.namelist['geogrid']['ref_lat']
            ref_lon = self.namelist['geogrid']['ref_lon']

            if not (-90 <= ref_lat <= 90) or not (-180 <= ref_lon <= 180):
                self.errors.append("Reference latitude and longitude must be within valid Earth bounds.")
        except KeyError as e:
            self.errors.append(f"Missing key in namelist: {e}")

    def validate_domain_coverage(self):
        try:
            dx = self.namelist['geogrid']['dx']
            dy = self.namelist['geogrid']['dy']
            e_we = self.namelist['domains']['e_we']
            e_sn = self.namelist['domains']['e_sn']
            ref_lat = self.namelist['geogrid']['ref_lat']
            ref_lon = self.namelist['geogrid']['ref_lon']

            area_of_interest = {
                'min_lat': -90, 'max_lat': 90,
                'min_lon': -180, 'max_lon': 180
            }
            # You can replace the above area_of_interest with the specific bounds of the region you want to check coverage for.

            # Calculate the domain boundaries for each domain
            domains = []
            for i in range(len(e_we)):
                width = dx[i] * (e_we[i] - 1)
                height = dy[i] * (e_sn[i] - 1)

                min_lat = ref_lat - height / 2.0
                max_lat = ref_lat + height / 2.0
                min_lon = ref_lon - width / 2.0
                max_lon = ref_lon + width / 2.0

                domains.append({'min_lat': min_lat, 'max_lat': max_lat, 'min_lon': min_lon, 'max_lon': max_lon})

                # Check if the domain covers the area of interest
                if not (area_of_interest['min_lat'] >= min_lat and area_of_interest['max_lat'] <= max_lat and
                        area_of_interest['min_lon'] >= min_lon and area_of_interest['max_lon'] <= max_lon):
                    raise ValueError(f"Domain {i+1} does not cover the area of interest.")

                # Check if the nested domain is within the parent domain
                if i > 0:
                    parent_domain = domains[i-1]
                    if not (parent_domain['min_lat'] <= min_lat and parent_domain['max_lat'] >= max_lat and
                            parent_domain['min_lon'] <= min_lon and parent_domain['max_lon'] >= max_lon):
                        raise ValueError(f"Nested domain {i+1} is not within its parent domain.")

        except KeyError as e:
            raise KeyError(f"Missing key in namelist: {e}")

    def run_validation(self):
        self.validate_grid_size()
        self.validate_domain_bounds()
        self.validate_domain_coverage()
