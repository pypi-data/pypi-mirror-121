# moray
>**<span>README</span>.md is a translation of README_jp.md.<br />So, there may be a mistranslation.**

- Package for creating HTML GUI using Python modules and JavaScript.
- Managing Python functions in modules.

***
## Contents
- [Install](#install)
- [Directory Structure](#directory-structure)
- [Usage](#usage)
  - [Starting the app](#starting-the-app)
  - [App options](#app-options)
  - [Call Python from JavaScript](#call-python-from-javascript)
  - [Call JavaScript from Python](#call-javascript-from-python)
  - [Abnormal exit handler](#abnormal-exit-handler)
  - [Logging](#logging)
- [Packages using](#packages-using)

***
## Install
- Execute the following command.
  ```
  pip install moray
  ```

***
## Directory Structure
- The moray application consists of a front-end with .html, .js, .css, etc., and a back-end with Python scripts.
- **/moray.js and /moray/ cannot be used, because moray use them.**
  ```
  python_script.py     <-- Python script
  web/                 <-- static web directory
    index.html
    css/
      style.css
    img/
      logo.png
  ```

***
## Usage
### Starting the app
- Suppose you put all the frontend files in `web` directory, including your start page `index.html`, then the app is started like this.
  ``` python
  import moray
  
  moray.run('web')
  ```
    - This will open a browser to `http://localhost:<automatically picked port>/index.html`.

### App options
- Additional options can be passed to `moray.run()` as keyword arguments.
  - start_page
    - str type (Default: '')
    - Your start page.
      - If `''`, index.html will be opened.
  - host
    - str type (Default: 'localhost')
    - Hostname to use for the Bottle server.
      - `'localhost'` or IP address is allowed.
  - port
    - int type (Default: 0)
    - Port to use for the Bottle server.
      - `0` or a value between `1025` and `65535` is allowed.
  - browser
    - str type (Default: 'chrome')
    - Browser to use.
      - Only `'chrome'` can be used.
  - cmdline_args
    - list of str type (Default: [])
    - Command line arguments to start the browser.
  - position
    - tuple of 2 int type (Default: None)
    - The (left, top) of the main window in pixels.
      - If not specified, `None`.
  - size
    - tuple of 2 int type (Default: None)
    - The (width, height) of the main window in pixels.
      - If not specified, `None`.

- Example
  ``` python
  import moray
  
  moray.run(
      'web',
      start_page = 'index.html',
      host = 'localhost',
      port = 8000,
      browser = 'chrome',
      cmdline_args = ['--disable-http-cache', '--incognito'],
      position = (400, 200),
      size = (800, 600)
  )
  ```

### Call Python from JavaScript
- **New thread is created for each Python call.**
- py_module.py
  ``` python
  import moray
  
  # Expose by decorator so that it can be called from JavaScript.
  @moray.expose
  def py_func(arg):
      return 'result'
  ```
- js_module.js
  ``` javascript
  // Import exposed Python function.
  // import {<function name>} from '/moray/py/<module name>.js'
  import {py_func} from '/moray/py/py_module.js'
  
  // Call Python function.
  py_func('arg')
  
  // To get the return value,
  // use "then" and "catch" of Promise object.
  py_func('arg').then(
      // Execution result is returned.
      v => ・・・
  ).catch(
      // Exception message is returned.
      v => ・・・
  )
  ```

### Call JavaScript from Python
- **If a Python function is called within a JavaScript function, it will be in a different thread than the calling Python function.**
- js_module.js
  ``` javascript
  import moray from '/moray.js'
  import {py_func} from '/moray/py/py_module.js'
  
  // Expose so that it can be called from Python.
  const js_func(arg) = function() {
      return 'result'
  }
  moray.expose(js_func)
  
  // Call Python function.
  py_func()
  ```
- py_module.py
  ``` python
  import moray
  
  @moray.expose
  def py_func():
      
      # Call JavaScript function.
      moray.js.js_func('arg')
      
      try:
          # To get the return value,
          # use "moray.js.<function name>(<arguments>)()".
          result = moray.js.js_func('arg')()
      except Exception as e:
          # When an exception is raised in JavaScript.
          print(e)
  ```

### Abnormal exit handler
- `"moray.onclose"` is handler that moray end.
- js_module.js
  ``` javascript
  import moray from '/moray.js'
  
  // Define a function in "moray.onclose".
  // "evt" is null.
  moray.onclose = function(evt) {
      alert('moray closed');
  }
  ```

### Logging
- `moray` uses `logging` module to logging.
- So you can set up a logger for `"moray"` to logging.
- Example
  ``` python
  import logging
  
  format = '[%(asctime)s][%(levelname)s] %(message)s (at %(name)s:%(lineno)s)'
  formatter = logging.Formatter(format)
  
  handler = logging.StreamHandler()
  handler.setLevel(logging.DEBUG)
  handler.setFormatter(formatter)
  
  logger = logging.getLogger('moray')
  logger.addHandler(handler)
  logger.setLevel(logging.INFO)
  ```

***
## Packages using
- [bottle-websocket](https://pypi.org/project/bottle-websocket/)
  - [MIT License](https://github.com/zeekay/bottle-websocket/blob/master/LICENSE)
- [requests](https://pypi.org/project/requests/)
  - [Apache License 2.0](https://github.com/psf/requests/blob/main/LICENSE)
- [Jinja2](https://pypi.org/project/Jinja2/)
  - [BSD License (BSD-3-Clause)](https://github.com/pallets/jinja/blob/main/LICENSE.rst)
