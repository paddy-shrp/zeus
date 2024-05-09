# ZEUS Project

## Setup

The "startup.py" file triggers the setups of the zeus project.

## What the ZEUS Project is about

This project aims to streamline API management and enhance control from a Python-based environment. 
It focuses on rapid module development and seamless API integrations. An HTTP-API provides straightforward access for frontend applications, while a dedicated data logger captures information from all modules for future data analysis and predictive automation of workflows.

## Structure
![ZEUS](https://github.com/paddy-shrp/zeus/assets/50612943/c5c21c6d-62bb-465f-8726-a5b1cbbe6b55)

## Modules
### Extensions
- Google Calendar API
- Spotify API
- OpenWeatherMap API
- Philips Hue Devices
- More to come as soon as the baseline is completely safe

### File Structure

```
zeus
├── api/
├── data_logger/
├── ai/
├── zeus_core/
│   ├── modules/
│   │   ├── extensions/
│   │   │   ├── example_extension_0/
│   │   │   │   └── example_extension_0.py
│   │   │   └── example_extension_1.py
│   │   ├── managers/
│   │   │   ├── example_manager/
│   │   │   │   └── example_manager_0.py
│   │   │   └── example_manager_1.py
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
└── startup.py
```
