from utilities import log
from utilities.common_methods import getDebugInfo
from data_monitoring import MonitorIntrinsicValue


def main():

    try:
        # Get the equities to monitor
        # take them from the file
        monitor = MonitorIntrinsicValue()
        monitor.check_for_discount()

    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

# run the program
if __name__ == "__main__":
    main()
