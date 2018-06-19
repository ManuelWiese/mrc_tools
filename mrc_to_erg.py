from mrc.mrc import Mrc
import sys
import copy

def mrc_to_erg(mrc, ftp):
    erg = copy.deepcopy(mrc)

    erg.course_header.data_types[1] = "WATTS"
    erg.course_header.ftp = int(ftp)

    data = erg.course_data[:]
    for index, value in enumerate(erg.course_data):
        data[index][1] = int(round(value[1] * erg.course_header.ftp / 100))
    erg.course_data = data

    return erg


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 mrc_to_erg.py FILE FTP")
        quit()

    filename = sys.argv[1]
    ftp = sys.argv[2]

    mrc = Mrc.load_mrc_file(filename)

    if mrc.course_header.data_types[1] != "PERCENT" and mrc.course_header.data_types[1] != "FTP":
        print("mrc has no PERCENT or FTP data type")
        quit()

    erg = mrc_to_erg(mrc, ftp)

    erg.save(filename.strip("mrc")+"erg")
