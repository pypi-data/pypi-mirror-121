# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashAutocomplete(Component):
    """A DashAutocomplete component.
AutosuggestComponent
A simplified select that enables user to use server-side filtering for options.

Keyword arguments:

- id (optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- className (optional):
    className of the dropdown element.

- clearable (default True):
    Whether or not the dropdown is \"clearable\", that is, whether or
    not a small \"x\" appears on the right of the dropdown that
    removes the selected value.

- disabled (default False):
    If True, this dropdown is disabled and the selection cannot be
    changed.

- loading_state (optional):
    Object that holds the loading state object coming from
    dash-renderer.

- multi (default False):
    If True, the user can select multiple values.

- optionHeight (default 35):
    height of each option. Can be increased when label lengths would
    wrap around.

- options (optional):
    An array of options {label: [string|number], value:
    [string|number]}, an optional disabled field can be used for each
    option.

- persisted_props (default ['value']):
    Properties whose user interactions will persist after refreshing
    the component or the page. Since only `value` is allowed this prop
    can normally be ignored.

- persistence (optional):
    Used to allow user interactions in this component to be persisted
    when the component - or the page - is refreshed. If `persisted` is
    truthy and hasn't changed from its previous value, a `value` that
    the user has changed while using the app will keep that change, as
    long as the new `value` also matches what was given originally.
    Used in conjunction with `persistence_type`.

- persistence_type (default 'local'):
    Where persisted user changes will be stored: memory: only kept in
    memory, reset on page refresh. local: window.localStorage, data is
    kept after the browser quit. session: window.sessionStorage, data
    is cleared once the browser quit.

- placeholder (optional):
    The grey, default text shown when no option is selected.

- search_value (optional):
    The value typed in the DropDown for searching.

- searchable (default True):
    Whether to enable the searching feature or not.

- setProps (optional):
    Dash-assigned callback that gets fired when the input changes.

- style (optional):
    Defines CSS styles which will override styles previously set.

- value (optional):
    The value of the input. If `multi` is False (the default) then
    value is just a string that corresponds to the values provided in
    the `options` property. If `multi` is True, then multiple values
    can be selected at once, and `value` is an array of items with
    values corresponding to those in the `options` prop."""
    @_explicitize_args
    def __init__(self, options=Component.UNDEFINED, value=Component.UNDEFINED, id=Component.UNDEFINED, optionHeight=Component.UNDEFINED, className=Component.UNDEFINED, clearable=Component.UNDEFINED, disabled=Component.UNDEFINED, multi=Component.UNDEFINED, placeholder=Component.UNDEFINED, searchable=Component.UNDEFINED, search_value=Component.UNDEFINED, style=Component.UNDEFINED, loading_state=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'clearable', 'disabled', 'loading_state', 'multi', 'optionHeight', 'options', 'persisted_props', 'persistence', 'persistence_type', 'placeholder', 'search_value', 'searchable', 'setProps', 'style', 'value']
        self._type = 'DashAutocomplete'
        self._namespace = 'dash_autocomplete'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'clearable', 'disabled', 'loading_state', 'multi', 'optionHeight', 'options', 'persisted_props', 'persistence', 'persistence_type', 'placeholder', 'search_value', 'searchable', 'setProps', 'style', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashAutocomplete, self).__init__(**args)
