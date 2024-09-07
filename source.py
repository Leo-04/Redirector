import pyaudio


class Source:
    """
    A source of audio that can be redirected into another source
    """

    OUTPUT = 1
    INPUT = 0
    UNKNOWN = -1

    stream: pyaudio.Stream
    chunk: int

    def __init__(self, driver: pyaudio.PyAudio, type_: int, device: int, chunk: int = 1024, format_: int = pyaudio.paFloat32, channels: int = 2,
                 rate: int = 44200):
        """
        Args:
            driver: PyAudio
                The pyaudio driver to create the stream from

            type_: int
                A constant defining the type of stream to create, and input stream or an output

            device: PyAudio
                The pyaudio driver to create the stream from

            chunk: int
                The amount of data to redirect each time

            format_: int
                A constant defining the format of the audio

            channels: int
                The number of channels the audio has

            rate: int
                The frequency of the audio
        """

        self.stream = driver.open(
            format=format_,
            channels=channels,
            rate=rate,
            frames_per_buffer=chunk,
            **{"output": True, "output_device_index": device} if type_ == Source.OUTPUT else {"input": True, "input_device_index": device}
        )

        self.chunk = chunk

    def redirect(self, source: "Source"):
        """
        Redirects the audio of this source to another source

        Args:
            source: Source
                The other source to redirect to
        """

        source.stream.write(self.stream.read(self.chunk, exception_on_overflow=False), self.chunk, exception_on_underflow=False)

    def close(self):
        """Closes the stream"""

        self.stream.stop_stream()
        self.stream.close()
