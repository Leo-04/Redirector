# Redirector
A simple app that allows you to redirect the sound of audio devices

Run the progam with no input files to see your devices and their index numbers

The config file should be a JSON file in the format:

```json
[
    {
        "from": {
            "type": ...,
            "device": ...,
            "chunk": ...,
            "format": ...,
            "channels": ...,
            "rate": ...
        },
        "to": {
            "type": ...,
            "device": ...,
            "chunk": ...,
            "format": ...,
            "channels": ...,
            "rate": ...
        }
    },
    ...
]
```

Where:
- `type` specifies if the source is an input or output, it can be the values `"input"` or `"output"`
- `device` is the device index number
- `chunk` is the amount of data (in bytes) to redirect each loop
- `format` is the format of audio being redrected, can be one of `"F32"`, `"U8"`, `"I8"`, `"I16"`, `"I24"` and  `"I32"`
- `channels` is the number of audio channels
- `rate` is the sampling rate

See `example.redirect` for an example
