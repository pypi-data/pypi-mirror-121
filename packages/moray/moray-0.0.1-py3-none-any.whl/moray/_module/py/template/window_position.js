export default function() {
    {% if size is not none %}
    window.resizeTo({{ size.0 }}, {{ size.1 }});
    {% endif %}
    {% if position is not none %}
    window.moveTo({{ position.0 }}, {{ position.1 }});
    {% endif %}
}
