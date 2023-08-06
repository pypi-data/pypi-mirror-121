from .resurses.log_worker import parse_call, args_parser, Log, Report

if __name__ == "__main__":
    arguments = args_parser()
    parse_call(arguments)
