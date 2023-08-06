# 2021-08-30 Asomchik Aleksander
# FoxMindEd Python course
# Task 06
"""

This module constructs report about F1 race.
It forms table from data read from user specified location and prints it.
"""

from datetime import datetime, timedelta
import re
import argparse

TIME_FORMAT = '%Y-%m-%d_%I:%M:%S.%f'
START_FILE = "//start.log"
END_FILE = "//end.log"
ABBREV_FILE = "//abbreviations.txt"


def get_data_for_report(folder: str) -> tuple:
    """
    Read data needed for report from files on disc.
        Parameters:
            folder - path to data used by module (files: start.log, end.log, abbreviations.txt)
        Return:
            Tuple of three data lists
            (Start time for each racer, Finish time for each racer, Racers abbreviation explanations)
        Catch errors:
            FileNotFoundError,
            PermissionError in case of files reading errors
    """
    start_path = folder + START_FILE
    end_path = folder + END_FILE
    abbrev_path = folder + ABBREV_FILE
    try:
        with open(start_path, "r") as start_file_object, \
                open(end_path, "r") as end_file_object, \
                open(abbrev_path, "r") as abbrev_file_object:
            start_data = start_file_object.read().splitlines()
            end_data = end_file_object.read().splitlines()
            abbrev_data = abbrev_file_object.read().splitlines()
            return start_data, end_data, abbrev_data
    except FileNotFoundError:
        print("Files not found")
        raise
    except PermissionError:
        print("Permission error occurred")
        raise


def build_report(folder: str, sorting: str, driver: str) -> list:
    """
    Construct report and return list of results of race.
        Parameters:
            folder - path to data
            sorting - "asc"/"desc" order of showing result
            driver - name of driver statistics to show (if "" - shows all drivers statistics)

        Return:
            list of racer(s) results as array of arrays in format
            [Name: str, Team: str, Time: str]

        Catch errors:
            ValueError in case of not valid driver name in "driver" parameter
    """
    if sorting not in ("asc", "desc"):
        raise ValueError('Sorting should be "asc" or "desc"')

    start_data, end_data, abbrev_data = get_data_for_report(folder)

    start_dict = {line[:3]: datetime.strptime(line[3:], TIME_FORMAT)
                  for line in start_data if line != ""}

    end_dict = {line[:3]: datetime.strptime(line[3:], TIME_FORMAT)
                for line in end_data if line != ""}

    abr_dict = {
        line.split("_")[0]:
        [line.split("_")[1], line.split("_")[2]]
        for line in abbrev_data if line != ""
    }

    all_racers_keys = {*start_dict, *end_dict}

    def race_time(abr_key):
        if ((end_dict.get(abr_key) <= start_dict.get(abr_key))
                or (end_dict.get(abr_key) or start_dict.get(abr_key)) == 0):
            error_msg = f"For racer {abr_dict.get(abr_key)[0]} no valid time data."
            if driver in abr_dict[abr_key] or driver == "":
                print(error_msg)
            return timedelta(days=1).total_seconds()
        else:
            return (end_dict.get(abr_key) -
                    start_dict.get(abr_key)).total_seconds()

    time_dict = {key: (race_time(key)) for key in all_racers_keys}

    report = sorted([
        [time_dict.get(key),
         abr_dict.get(key)[0],
         abr_dict.get(key)[1]]
        for key in all_racers_keys])

    if driver and driver not in [line[1] for line in report]:
        raise ValueError("No such driver")

    report = (
        [str(timedelta(seconds=line[0])),
         str(num + 1) + ". " + line[1],
         line[2]]
        for num, line in enumerate(report)
    )

    report = [line for line in report if driver in line[1] or driver == ""]

    report.sort(reverse=(sorting == "desc"))
    if len(report) > 15 and sorting == "asc":
        report.insert(15, ["", "", ""])
    elif len(report) > 15 and sorting == "desc":
        report.insert(-15, ["", "", ""])

    report = [[line[1], line[2], line[0]] for line in report]

    return report


def print_report(report: list):
    """
    Construct and print visual table of given report
        Parameters:
            report - list of racer(s) results as array of arrays in format
            [Name: str, Team: str, Time: str]
    """
    if report == []:
        print("No report data to show")
        return

    report_table = (
        [elem.replace('1 day, 0:00:00', "no_valid_time") for elem in line]
        for line in report
    )

    report_table = [
        [line[0], line[1], re.sub(r"^[0:]*|000$", "", line[2])]
        for line in report_table
    ]

    column_width = [
        max([len(line[i]) for line in report_table])
        for i in range(3)
    ]

    report_table = (
        [line[i].ljust(column_width[i]) for i in range(3)]
        for line in report_table
    )

    report_table = (
        ["-" * (sum(column_width) + 6)] if re.match(r" ", line[0]) else line
        for line in report_table
    )

    report_table = (" | ".join(line) for line in report_table)

    report_table = "\n".join(report_table)

    print("\n" + report_table)


def cli_for_report():
    """
    Command line parser


    """

    parser = argparse.ArgumentParser(description="F1 Monaco 2018 race report")
    parser.add_argument(
        "--files",
        type=str,
        help="path to folder with race data")
    parser.add_argument(
        "--driver",
        type=str,
        help='Drivers name for his statistics (use "")')

    sorting = parser.add_mutually_exclusive_group()

    sorting.add_argument(
        "--desc",
        action="store_true",
        help='sorting desc')
    sorting.add_argument(
        "--asc",
        action="store_true",
        help='sorting asc')

    parser.set_defaults(driver="", files="data")

    return parser.parse_args()


if __name__ == "__main__":

    args = cli_for_report()
    print_report(
        build_report(
            folder=args.files,
            driver=args.driver,
            sorting="desc" if args.desc else "asc"))
