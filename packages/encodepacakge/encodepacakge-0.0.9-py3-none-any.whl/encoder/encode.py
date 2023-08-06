"""
module to encode url with sepcial charc during api call
"""
import logging
class Encode():
    """
    class contains encode functions
    """
    def __init__(self):
        self.logger = logging.getLogger()
    def encoded(self, data):
        """
        encode function to convert reserved char as per wiki [Reserved_characters in wiki]
        (https://en.wikipedia.org/wiki/Percent-encoding#Reserved_characters)
        usage
        enc = Encode()
        print(a.encoded("Data\""))
        """
        encodedata = {
            "!": "%21",
            "\"": "%22",
            "#": "%23",
            "$": "%24",
            "%": "%25",
            "&": "%26",
            "'": "%27",
            "(": "%28",
            ")": "%29",
            "*": "%2A",
            "+": "%2B",
            ",": "%2C",
            "-": "%2D",
            ".": "%2E",
            "/": "%2F"}
        output = "".join([encodedata.get(d, d) for d in data])
        self.logger.info('Encoded %s into %s', data, output)
        return output

    def encodewithtemplate(self, template, data):
        """
        Provide a template on what to convert in the given string
        encodedata = {"!": "%21", "\"": "%22",  "#": "%23", "$": "%24",
        "%": "%25", "&": "%26", "'": "%27",
        "(": "%28", ")": "%29", "*": "%2A", "+": "%2B",
        ",": "%2C", "-": "%2D", ".": "%2E",  "/": "%2F"}
        print(a.encodewithtemplate(encodedata, "data#"))
        """
        output = "".join([template.get(d, d) for d in data])
        self.logger.info('Encoded %s into %s', data, output)
        return output
