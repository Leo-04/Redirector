import os


def report_error(error: Exception, message: any):
    """
    Reports an error to the screen, then exits

    Args:
        error: Exception
            The error that has just occurred

        message: any
            The message to be displayed before the error
    """

    print(message, error, sep="\n\t")

    input("[Press enter to exit]")
    os._exit(-1)
