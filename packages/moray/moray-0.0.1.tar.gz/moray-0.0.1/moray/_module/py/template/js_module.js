import {call_python} from '/moray/static/core'

{% for func_name in list_func_name %}
export let {{func_name}} = function() {
    return call_python('{{module}}', '{{func_name}}', arguments);
}
{% endfor %}
