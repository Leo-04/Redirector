import atexit
import pyaudio
import sys

from report_error import report_error
from rule import load_rules, create_source_from_rule


def main():
    # Create driver
    driver = pyaudio.PyAudio()
    atexit.register(driver.terminate)

    # Print all device info
    print("Device | InputChannels | OutputChannels | SampleRate | Name")
    for i in range(driver.get_device_count()):
        dev = driver.get_device_info_by_index(i)
        print(
            str(dev["index"]).ljust(6, " "),
            str(dev['maxInputChannels']).ljust(13, " "),
            str(dev['maxOutputChannels']).ljust(14, " "),
            str(dev['defaultSampleRate']).ljust(10, " "),
            dev['name'],
            sep=" | "
        )

    # Get input file
    if len(sys.argv) == 2:
        file = sys.argv[1]
    else:
        print("Input config file or drag and drop file onto this window then press enter:")
        file = input("")

    # Load rules
    rules = load_rules(file)

    # Create redirects
    redirects = []
    try:
        for rule in rules:
            redirects.append((
                create_source_from_rule(driver, **rule["from"]),
                create_source_from_rule(driver, **rule["to"])
            ))
    except Exception as err:
        for redirect in redirects:
            redirect[0].close()
            redirect[1].close()

        report_error(err, "Could not open audio source")

    # Main loop
    print("Press CTRL-C to stop")
    try:
        while True:
            for redirect in redirects:
                redirect[0].redirect(redirect[1])
    except KeyboardInterrupt:
        print("User stopped program")
    except Exception as err:
        for redirect in redirects:
            redirect[0].close()
            redirect[1].close()
        report_error(err, "Could not open audio source")

    # Close redirects
    for redirect in redirects:
        redirect[0].close()
        redirect[1].close()

    print("Exiting...")


if __name__ == "__main__":
    main()
