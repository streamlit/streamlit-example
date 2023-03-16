class NestingOptionsValidation:
    def __init__(self, namelist):
        self.namelist = namelist
        self.errors = []

    def validate_nesting_options(self):
        try:
            feedback = self.namelist['domains']['feedback']
            time_step_ratio = self.namelist['domains']['time_step_ratio']
            parent_grid_ratio = self.namelist['domains']['parent_grid_ratio']

            # Validate feedback option
            if feedback not in [0, 1]:
                self.errors.append("Invalid feedback option. Options are 0 (one-way interaction) or 1 (two-way interaction).")

            # Validate consistency of time step ratio and parent grid ratio
            if len(time_step_ratio) != len(parent_grid_ratio) - 1:
                self.errors.append("Number of time step ratios must be one less than the number of parent grid ratios.")

            for i in range(len(time_step_ratio)):
                if time_step_ratio[i] != parent_grid_ratio[i+1]:
                    self.errors.append("Inconsistency between time step ratio and parent grid ratio for nested domains.")

        except KeyError as e:
            self.errors.append(f"Missing key in namelist: {e}")
