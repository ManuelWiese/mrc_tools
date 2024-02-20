from mrc.mrc import Mrc
from wahoo_plan.wahoo_plan import WahooPlan, WahooInterval
import sys
import os

def get_wahoo_intervals(mrc):
    wahoo_intervals = []
    for index, data in enumerate(mrc.course_data[1:]):
        start_time = mrc.course_data[index][0] * 60
        end_time = data[0] * 60
        start_value = mrc.course_data[index][1]
        end_value = data[1]
        if abs(start_time - end_time) >= 0.1:
            interval = WahooInterval()
            interval.add_subinterval(duration=(end_time-start_time), percent_ftp_high=[start_value, end_value] )
            wahoo_intervals.append(interval)

    return wahoo_intervals

def mrc_to_wahoo_plan(mrc, name=None, description=None):
    builder = WahooPlan.Builder()

    if not name:
        name, _ = os.path.splitext(mrc.course_header.file_name)
    if not description:
        description = mrc.course_header.description

    builder.set_name(name).set_description(description)

    for interval in get_wahoo_intervals(mrc):
        builder.add_interval(interval)

    return builder.build()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 mrc_to_wahoo_plan.py FILE")
        quit()

    filename = sys.argv[1]

    mrc = Mrc.load_mrc_file(filename)

    if mrc.course_header.data_types[1] != "PERCENT" and mrc.course_header.data_types[1] != "FTP":
        print("mrc has no PERCENT or FTP data type")
        quit()

    with open(filename.strip("mrc") + "plan", "w") as f:
        f.write(str(mrc_to_wahoo_plan(mrc)))
