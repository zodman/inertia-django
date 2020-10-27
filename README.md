# inertia-django conector
![Python package](https://github.com/zodman/inertia-django/workflows/Python%20package/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/zodman/inertia-django/badge.svg?branch=master)](https://coveralls.io/github/zodman/inertia-django?branch=master)

Based on inertia-laravel.

Check https://github.com/zodman/django-inertia-demo for example how to use


## Usage

### `render_inertia` function

The easiest way to render a Vue component with inertia-django is to use the `render_inertia` function.   
*Note:* You must  have an `Index.vue` component in your project.

```python
from inertia import render_inertia

def index(request):
    # for function views just use the render_inertia function
    return render_inertia(request, 'Index', props={'title': 'My inertia-django page'}, template_name='index.html')
```

----

## Server-side setup

### Install dependencies

`pip install inertia-django django-js-routes`

### Root Template

```html=
{# templates/base.html #}
{% load js_routes_tags %}<!DOCTYPE html>
<html  class="h-full bg-gray-200">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0" />
    {% js_routes %}
    <script src="{{ STATIC_URL}}dist/app.js" defer></script>
    <link href="{{ STATIC_URL}}dist/app.css" rel="stylesheet" />
            
  </head>
  <body class="font-sans leading-none text-gray-700 antialiased">
    {{ page|json_script:"page" }}
    <div id="app">
    </div>
  </body>
</html>
```

### Creating responses

```python=
from inertia.views import render_inertia

def event_detail(request, id):
    event = Event.objects.get(pk=id)
    props = {
        'event': {
            'id':event.id,
            'title': event.title,
            'start_date': event.start_date,
            'description': event.description
        }
    }
    return render_inertia(request, "Event/Show", props)
```

We strong suggest to use [marshmallow](https://marshmallow.readthedocs.io/en/latest/) 
because it had serializer and validation and  fully compatible with django.


## Client-side setup
### Install dependencies
```
npm install @inertiajs/inertia @inertiajs/inertia-vue 
# extra deps
npm install parcel-bundler
```

### Initialize app

```javascript=
import { InertiaApp } from '@inertiajs/inertia-vue'
import Vue from 'vue'
Vue.use(InertiaApp);

const app = document.getElementById('app');
// we are getting the initialPage from a rendered json_script
const page = JSON.parse(document.getElementById("page").textContent);

import Index from "./Pages/Index";
import Contacts from "./Pages/Contacts";
import Organization from "./Pages/Organizations";
import ContactEdit from "./Pages/Contacts.Edit";

const pages = {
  'Login': Login,
  'Index': Index,
  'Contacts': Contacts,
  'Contacts.Edit': ContactEdit,
}

new Vue({
  render: h => h(InertiaApp, {
    props: {
      initialPage: page,
      resolveComponent: (name) => {
        console.log("resolveComponent ", name)
        return pages[name];
      },
    },
  }),
}).$mount(app)

```

TODO: add why not use resolveComponent dynamic.  


## Routing

### Generating URLs

For the part of the urls the same functionality as laravel or ziggy is 

*django-js-routes* https://pypi.org/project/django-js-routes/

# TODO: explain how inertia/middleware.py works

# more info https://inertiajs.com/

