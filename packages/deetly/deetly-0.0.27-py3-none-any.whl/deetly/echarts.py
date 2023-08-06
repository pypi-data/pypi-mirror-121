import os
from typing import Dict
from typing import Optional
from typing import Union

import json


class Map:
    def __init__(
        self, map_name: str, geo_json: Dict, special_areas: Optional[Dict] = None
    ) -> None:
        self.map_name: str = map_name
        self.geo_json: Dict = geo_json
        self.special_areas: Optional[Dict] = special_areas

    def to_json(self):
        return {
            "mapName": self.map_name,
            "geoJson": self.geo_json,
            "specialAreas": self.special_areas,
        }


class JsCode:
    def __init__(self, js_code: str):
        js_placeholder = "--x_x--0_0--"
        self.js_code = f"{js_placeholder}{js_code}{js_placeholder}"


def echarts(
    options: Dict,
    theme: Union[str, Dict] = "",
    events: Dict[str, str] = None,
    height: str = "300px",
    width: str = "100%",
    renderer: str = "canvas",
    map: Map = None,
    key: str = None,
):
    """Display an ECharts instance
    Parameters
    ----------
    options: Dict
        Dictionary of echarts options. JS code should have been wrapped beforehand.
    theme: str | Dict
        Prebuilt theme, or object defining theme
    events: Dict
        Dictionary of mouse events to string JS functions. 
        Don't wrap values with JsCode placeholder.
    height: str
        Height of ECharts chart
    width: Image
        Width of ECharts chart
    renderer: {'canvas', 'svg'}
        Renderer for displaying chart
    map: Map
        Details of GeoJSON map to register into echarts
    key: str
        An optional string to use as the unique key for the widget. 
        Assign a key so the component is not remount every time the script is rerun.
    """
    if events is None:
        events = {}
    return json.dumps(
        {
            "options": options,
            "theme": theme,
            "onEvents": {k: JsCode(v).js_code for k, v in events.items()},
            "height": height,
            "width": width,
            "renderer": renderer,
            "map": map.to_json() if map is not None else None,
            "key": key,
            "default": None,
        }
    )


def pyecharts(
    chart: Dict,
    theme: Union[str, Dict] = "",
    events: Dict[str, str] = None,
    height: str = "300px",
    width: str = "100%",
    renderer: str = "canvas",
    map: Map = None,
    key: str = None,
):
    """Display a PyECharts instance
    Parameters
    ----------
    chart: Base
        PyEcharts instance. JS code should have been wrapped beforehand.
    theme: str | Dict
        Prebuilt theme, or object defining theme
    events: Dict
        Dictionary of mouse events to string JS functions. 
        Don't wrap values with JsCode placeholder.
    height: str
        Height of ECharts chart
    width: Image
        Width of ECharts chart
    renderer: {'canvas', 'svg'}
        Renderer for displaying chart
    map: Map
        Details of GeoJSON map to register into echarts
    key: str
        An optional string to use as the unique key for the widget. 
        Assign a key so the component is not remount every time the script is rerun.
    """
    options = json.dumps(chart.get_options(), default=default, ignore_nan=True)
    return echarts(
        options=json.loads(options),
        theme=theme,
        events=events,
        height=height,
        width=width,
        renderer=renderer,
        map=map,
        key=key,
    )
