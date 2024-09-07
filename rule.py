import json
import pyaudio

from report_error import report_error
from source import Source


def load_rules(file: str) -> list[dict]:
    """
    Loads rules from a json file

    Args:
        file: str | PathLike
            The file path to a json file

    Returns:
        A list of rules

    """

    try:
        fp = open(file)
    except Exception as err:
        report_error(err, "Cannot open file")

    try:
        data = json.load(fp)
        fp.close()
    except Exception as err:
        report_error(err, "Could not decode file")

    if type(data) is not list:
        report_error(SyntaxError(), "Invalid rule format")

    for i, rule in enumerate(data):
        if type(rule) is not dict:
            report_error(SyntaxError(), f"Rule {i} is not a valid rule")

        if "from" not in rule:
            report_error(SyntaxError(), f"Rule {i} is missing a \"from\"")

        if "to" not in rule:
            report_error(SyntaxError(), f"Rule {i} is missing a \"to\"")

        if "type" not in rule["from"] or rule["from"]["type"] not in ["input", "output"]:
            report_error(SyntaxError(), f"Rule {i} \"from\" \"type\" is invalid")

        if "device" not in rule["from"] or type(rule["from"]["device"]) != int:
            report_error(SyntaxError(), f"Rule {i} \"from\" \"device\" is invalid")

        if "chunk" not in rule["from"] or type(rule["from"]["chunk"]) != int:
            report_error(SyntaxError(), f"Rule {i} \"from\" \"chunk\" is invalid")

        if "format" not in rule["from"] or rule["from"]["format"] not in ["F32", "U8", "I8", "I16", "I24", "I32"]:
            report_error(SyntaxError(), f"Rule {i} \"from\" \"format\" is invalid")

        if "channels" not in rule["from"] or type(rule["from"]["channels"]) != int:
            report_error(SyntaxError(), f"Rule {i} \"from\" \"channels\" is invalid")

        if "rate" not in rule["from"] or type(rule["from"]["rate"]) != int:
            report_error(SyntaxError(), f"Rule {i} \"from\" \"rate\" is invalid")

        if "type" not in rule["to"] or rule["to"]["type"] not in ["input", "output"]:
            report_error(SyntaxError(), f"Rule {i} \"to\" \"type\" is invalid")

        if "device" not in rule["to"] or type(rule["to"]["device"]) != int:
            report_error(SyntaxError(), f"Rule {i} \"to\" \"device\" is invalid")

        if "chunk" not in rule["to"] or type(rule["to"]["chunk"]) != int:
            report_error(SyntaxError(), f"Rule {i} \"to\" \"chunk\" is invalid")

        if "format" not in rule["to"] or rule["to"]["format"] not in ["F32", "U8", "I8", "I16", "I24", "I32"]:
            report_error(SyntaxError(), f"Rule {i} \"to\" \"format\" is invalid")

        if "channels" not in rule["to"] or type(rule["to"]["channels"]) != int:
            report_error(SyntaxError(), f"Rule {i} \"to\" \"channels\" is invalid")

        if "rate" not in rule["to"] or type(rule["to"]["rate"]) != int:
            report_error(SyntaxError(), f"Rule {i} \"to\" \"rate\" is invalid")

    return data


def create_source_from_rule(driver, type: str, device: int, chunk: int = 1024, format: str = pyaudio.paFloat32, channels: int = 2,
                            rate: int = 44200) -> Source:
    """Creates a source from rule's values"""

    type = Source.OUTPUT if type == "output" else Source.INPUT if type == "input" else Source.UNKNOWN

    format = {
        "F32": pyaudio.paFloat32,
        "U8": pyaudio.paUInt8,
        "I8": pyaudio.paInt8,
        "I16": pyaudio.paInt16,
        "I24": pyaudio.paInt24,
        "I32": pyaudio.paInt32
    }[format]

    return Source(
        driver,
        type,
        device,
        chunk,
        format,
        channels,
        rate
    )
