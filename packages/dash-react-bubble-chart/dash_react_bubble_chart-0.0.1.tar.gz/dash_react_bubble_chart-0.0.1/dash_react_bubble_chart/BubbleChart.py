# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class BubbleChart(Component):
    """A BubbleChart component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- id (string; optional)

- data (list of dicts; optional):
    The ID used to identify this component in Dash callbacks.

    `data` is a list of dicts with keys:

    - label (string; required)

    - value (number; required)

- height (number; default 800)

- labelFont (dict; default {    family: 'Arial',    size: 11,    color: '#fff',    weight: 'normal',})

    `labelFont` is a dict with keys:

    - color (string; optional)

    - family (string; optional)

    - size (number; optional)

    - weight (string; optional)

- overflow (boolean; optional)

- padding (number; default 0)

- selectedNode (string; optional)

- showLegend (boolean; optional)

- valueFont (dict; default {    family: 'Arial',    size: 16,    color: '#fff',    weight: 'bold',})

    `valueFont` is a dict with keys:

    - color (string; optional)

    - family (string; optional)

    - size (number; optional)

    - weight (string; optional)

- width (number; default 1000)"""
    @_explicitize_args
    def __init__(self, data=Component.UNDEFINED, id=Component.UNDEFINED, overflow=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, padding=Component.UNDEFINED, showLegend=Component.UNDEFINED, valueFont=Component.UNDEFINED, labelFont=Component.UNDEFINED, selectedNode=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'data', 'height', 'labelFont', 'overflow', 'padding', 'selectedNode', 'showLegend', 'valueFont', 'width']
        self._type = 'BubbleChart'
        self._namespace = 'dash_react_bubble_chart'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data', 'height', 'labelFont', 'overflow', 'padding', 'selectedNode', 'showLegend', 'valueFont', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(BubbleChart, self).__init__(**args)
