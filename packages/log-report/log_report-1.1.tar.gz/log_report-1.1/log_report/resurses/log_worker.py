import argparse
import os
from datetime import datetime, timedelta


def args_parser(**args):
    """
    Parse args from command line
    :param args:
    :return: parsed args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="take path to dir with logs")
    parser.add_argument("--asc", help="sort by first to last ", action="store_false")
    parser.add_argument("--desc", help="sort by last to first", action="store_true")
    parser.add_argument("--driver", help="show statistic about driver")

    return parser.parse_args(**args)


class Log:
    """
    class object take one argument path to folder with logs
    class realize methods:
     -read logs from folder
     - check validate data
     - return lists with logs
    """
    def __init__(self, path):
        self.logs_path = path
        self.abbr_list = []
        self.start_list = []
        self.end_list = []

    def read_data(self):
        # open files in dir after write lines from files to lists
        try:
            with open(os.path.join(self.logs_path, 'start.log')) as f:
                self.start_list = [line.strip() for line in f.readlines()]
            with open(os.path.join(self.logs_path, 'end.log')) as f:
                self.end_list = [line.strip() for line in f.readlines()]
            with open(os.path.join(self.logs_path, 'abbreviations.txt')) as f:
                self.abbr_list = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            raise FileNotFoundError("directory not found or  incorrect names of files ")

    def validate(self):
        # if length abbreviations drivers not equal len start or end log
        if len(self.abbr_list) != len(self.end_list) and len(self.start_list):
            # print(f"exc 1, {len(self.abbr_list)} , {len(self.end_list)}, {len(self.start_list)}")
            print("data is not full")
            exit(0)
        # check first three chars for equal
        for abbr, abbr1, abbr2 in zip(self.abbr_list, self.start_list, self.end_list):
            if abbr[:3] != abbr1[:3] and abbr2[:3]:
                print("data is not correct ")
                # print(f" exc 2 ,  {abbr[:3]}, {abbr1[:3]}, {abbr2[:3]}")
                exit(0)

    def get_logs(self):
        self.start_list.sort()
        self.end_list.sort()
        self.abbr_list.sort()
        self.validate()
        return self.abbr_list, self.start_list, self.end_list


class Report:
    """
    class obj takes 3 arguments abbreviations, start_log_list, end_log_list
    """

    def __init__(self, abbr_list, start_list, end_list):
        self.diff_list = []
        self.abbreviations = abbr_list
        self.start_log_list = start_list
        self.end_log_list = end_list
        self.tuple_data = []

    def get_diff(self):
        # split string by _ takes last and end minus start , write it to diff_list
        for start_time, end_time in zip(self.start_log_list, self.end_log_list):
            start = start_time[3:]
            end = end_time[3:]
            _s = datetime.strptime(start, "%Y-%m-%d_%I:%M:%S.%f")
            _e = datetime.strptime(end, "%Y-%m-%d_%I:%M:%S.%f")
            diff = _e - _s
            self.diff_list.append(diff)

    def concatenate_sort_data(self, sort_by):
        # create tuple with abbreviations and diff_time sort by input arguments from cl
        # if desc: worst to best if blank or asc: default is asc so best to worst
        self.tuple_data = zip(self.abbreviations, self.diff_list)
        if sort_by.desc is True:
            self.tuple_data = sorted(self.tuple_data, key=lambda x: x[1], reverse=True)
        else:
            self.tuple_data = sorted(self.tuple_data, key=lambda x: x[1])

    def output(self):
        # create output takes data from tuple_data and takes variables from there
        for index, element in enumerate(self.tuple_data):
            _name = element[0].split("_")[1]
            _car = element[0].split("_")[-1]
            _time = str(element[1]).replace("000", "")
            if index + 1 < 10:
                print(f"{index + 1}. {_name.ljust(18)} | {_car.ljust(25)} |{_time}")
            else:
                print(f"{index + 1}. {_name.ljust(17)} | {_car.ljust(25)} |{_time}")

    def driver(self, name):
        for driver in self.abbreviations:
            if name in driver:
                _person = driver
                index = self.abbreviations.index(_person)
                _time_circle = self.diff_list[index]
                return _person, _time_circle
            else:
                print("name is incorrect")

    @staticmethod
    def output_solo(person, time):
        print(f"{person.split('_')[1]} | {person.split('_')[-1]} | {str(time).replace('000', '')}")


def parse_call(args_cm):
    logs = Log(path=args_cm.path)
    logs.read_data()
    abbr_lst, start_lst, end_lst = logs.get_logs()
    report = Report(abbr_list=abbr_lst, start_list=start_lst, end_list=end_lst)
    report.get_diff()
    report.concatenate_sort_data(sort_by=args_cm)
    if args_cm.path and not args_cm.driver:
        report.output()
    if args_cm.driver:
        person, time = report.driver(name=args_cm.driver)
        report.output_solo(person=person, time=time)