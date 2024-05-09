# ZEUS Project

## Setup

The "startup.py" file triggers the setups of the current extensions.

## What ZEUS is about

This project is designed to make api control more unified and lean on better control over it from a Python perspective.
It will advance towards a maintainable API where all websites easily can refer to. It should also support data logging of api data, thus making it usable for a data analysis or workflow automation predictions.

Currently configured for:
- Google Calendar API
- Spotify API
- OpenWeatherMap API
- Philips Hue Devices

## Structure

![ZEUS](https://github.com/paddy-shrp/zeus/assets/50612943/c490be65-2d69-47c1-9be4-0a013f3e45c0)

### File Structure

```
zeus
├─ __init__.py
├─ api
├─ extensions
│  ├─ __init__.py
│  ├─ example_extension_0.py
│  └─ example_extension_1
│     └─ example_extension_1.py
├─ managers
│  ├─ __init__.py
│  ├─ example_manager_0.py
│  └─ example_manager_1
│     └─ example_manager_1.py
├─ utils
│  └─ __init__.py
└─ data_logger
```
