import datetime

class TimeControlValidation:
    def __init__(self, namelist):
        self.namelist = namelist
        self.errors = []
        
    def validate_input_times(self):
        try:
            start_date = self.namelist['time_control']['start_date']
            end_date = self.namelist['time_control']['end_date']

            start_date = [datetime.datetime.strptime(date, '%Y-%m-%d_%H:%M:%S') for date in start_date]
            end_date = [datetime.datetime.strptime(date, '%Y-%m-%d_%H:%M:%S') for date in end_date]

            for s, e in zip(start_date, end_date):
                if s >= e:
                    self.errors.append("Start date must be before end date.")
        except KeyError as e:
            self.errors.append(f"Missing key in namelist: {e}")
        except ValueError as e:
            self.errors.append(f"Incorrect date format in namelist: {e}. Use 'YYYY-MM-DD_HH:MM:SS' format.")

    def validate_time_step(self):
        try:
            time_step = self.namelist['time_control']['time_step']
            if time_step <= 0:
                self.errors.append("Time step must be a positive value.")
            # Add additional logic to check if the time step is appropriate for the chosen grid size and model stability.
        except KeyError as e:
            self.errors.append(f"Missing key in namelist: {e}")

    def validate_output_interval(self):
        try:
            history_interval = self.namelist['time_control']['history_interval']
            frames_per_outfile = self.namelist['time_control']['frames_per_outfile']
            end_date = self.namelist['time_control']['end_date']
            start_date = self.namelist['time_control']['start_date']

            end_date = [datetime.datetime.strptime(date, '%Y-%m-%d_%H:%M:%S') for date in end_date]
            start_date = [datetime.datetime.strptime(date, '%Y-%m-%d_%H:%M:%S') for date in start_date]

            for domain, (s, e, interval, frames) in enumerate(zip(start_date, end_date, history_interval, frames_per_outfile)):
                if not (0 < interval <= (e - s).total_seconds() / frames):
                    self.errors.append(f"Output interval for domain {domain+1} must be within the simulation period and greater than 0.")
        except KeyError as e:
            self.errors.append(f"Missing key in namelist: {e}")

    def run_validation(self):
        self.validate_input_times()
        self.validate_time_step()
        self.validate_output_interval()
