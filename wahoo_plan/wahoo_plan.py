import textwrap

class WahooSubinterval:
    def __init__(
        self,
        duration=None,
        percent_ftp_high=None,
        percent_ftp_low=None,
        cadence_low=None,
        cadence_high=None,
        name=None
        
    ):      
        self.duration = int(duration)
        self.name = name
        self.values = {}

        if percent_ftp_low is not None:
            self.values.update({"PERCENT_FTP_LO": percent_ftp_low})

        if percent_ftp_high is not None:
            self.values.update({"PERCENT_FTP_HI": percent_ftp_high})
        
        if cadence_low is not None:
            self.values.update({"CAD_LO": cadence_low})

        if cadence_high is not None:
            self.values.update({"CAD_HI": cadence_high})

    def __str__(self):
        output = "=SUBINTERVAL=\n"
        
        if self.name is not None:
            output += "NAME={}\n".format(self.name)

        for key, value in self.values.items():
            if isinstance(value, list):
                if len(value) == 2 and value[0] != value[1]:
                    ramp_rate = (value[1] - value[0]) / self.duration
                    output += "{}={}@{:.6f}\n".format(key, value[0], ramp_rate)
                else:
                    output += "{}={}\n".format(key, value[0])
            else:
                output += "{}={}\n".format(key, value)

        output += "MESG_DURATION_SEC>={}?EXIT\n".format(self.duration)
        return output
        
class WahooInterval:
    def __init__(self, name=None):
        self.name = name
        self.duration = 0
        self.subintervals = []
        
    def add_subinterval(self, **kwargs):
        subinterval = WahooSubinterval(**kwargs)
        self.duration += subinterval.duration
        self.subintervals.append(subinterval)

    def __str__(self):
        output = "=INTERVAL=\n"

        if self.name is not None:
            output += "NAME={}\n".format(self.name)

        if len(self.subintervals) == 1:
            output += str(self.subintervals[0]).replace("=SUBINTERVAL=\n", "")
        else:
            output += "MESG_DURATION_SEC>=0?EXIT\n"
            for subinterval in self.subintervals:
                output += "\n{}".format(subinterval)

        return output

class WahooPlan:
    class Builder:
        def __init__(self):
            self.wahoo_plan = WahooPlan()

        def set_name(self, name):
            self.wahoo_plan.name = name
            return self

        def set_description(self, description):
            self.wahoo_plan.description = description
            return self

        def set_ftp_test_factor(self, ftp_test_factor):
            self.wahoo_plan.ftp_test_factor = ftp_test_factor
            return self

        def add_interval(self, interval):
            self.wahoo_plan.intervals.append(interval)
            self.wahoo_plan.duration += interval.duration
            return self

        def build(self):
            return self.wahoo_plan

    def __init__(self):
        self.name = None
        self.duration = 0

        # LOCATION_TYPE and WORKOUT_TYPE, see:
        # https://gist.github.com/Intyre/2c0a8e337671ed6f523950ef08e3ca3f?permalink_comment_id=4688536#gistcomment-4688536
        self.location_type = 0
        self.workout_type = 0
        self.description = None
        self.ftp_test_factor = None

        self.intervals = []

    def __str__(self):
        output="=HEADER=\n"
        if self.name is not None:
            output += "NAME={}\n".format(self.name)

        output += "DURATION={}\n".format(self.duration)
        output += "LOCATION_TYPE={}\n".format(self.location_type)
        output += "WORKOUT_TYPE={}\n".format(self.workout_type)

        if self.description is not None:
            for line in textwrap.wrap(self.description, 96):
                output += "DESCRIPTION={} \n".format(line)

        output += "\n=STREAM=\n"

        for interval in self.intervals:
            output += "{}\n".format(interval)

        return output

if __name__ == "__main__":
    builder = WahooPlan.Builder().set_name("Test-Training").set_description("This is a test.")
    
    interval = WahooInterval(name="test")
    interval.add_subinterval(duration=60, percent_ftp_high=10)
    interval.add_subinterval(duration=60, percent_ftp_high=[10, 100])
    builder.add_interval(interval)

    interval = WahooInterval()
    interval.add_subinterval(name="subinterval", duration=120, percent_ftp_high=[100, 50])

    builder.add_interval(interval)

    print(builder.build())
