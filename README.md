## inertia-django conector.

Based on inertia-laravel.

Check https://github.com/zodman/django-inertia-demo for example how to use



## Usage



### `render_inertia` function

The easiest way to render a Vue component with inertia-django is to use the `render_inertia` function. *
Note:* You have to have an `Index.vue` component in your project.


```python
from inertia import render_inertia

def index(request):
    # for function views just use the render_inertia function
    return render_inertia(request, 'Index', props={'title': 'My inertia-django page'}, template_name='index.html')
```


