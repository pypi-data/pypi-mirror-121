"""
呼び出される関数を管理
呼び出し用ESモジュール(JavaScript)の生成
"""

from bottle import HTTPResponse
from functools import wraps
from jinja2 import PackageLoader, Environment

from moray import _config

_expose_module = {}

_loader = PackageLoader(package_name='moray._module.py', package_path='template')
_env = Environment(loader=_loader)
_template_js_module = _env.get_template(name='js_module.js')
_template_window_position = _env.get_template(name='window_position.js')

def register(func):
    """
    デコレータ moray.expose の実装
    JavaScriptから呼び出す関数を登録
    
    Attributes:
        func (function): 登録する関数
    """

    module = func.__module__
    func_name = func.__name__
    
    _expose_module.setdefault(module, {})
    _expose_module[module][func_name] = func

def call(module, func_name, args):
    """
    関数を呼び出す
    
    Attributes:
        module (str): 呼び出すモジュール名
        func_name (str): 呼び出す関数名
        args (dict): 引数
    
    Returns:
        関数の実行結果
    """
    
    func = _expose_module[module][func_name]
    return func(*args)

def _js_renderer(func):
    """
    デコレータ
    JavaScriptのヘッダー情報を付与
    
    Attributes:
        func (func): JavaScriptレンダリング関数
    
    Returns:
        HTTPResponse: ヘッダー情報が付与されたJavaScript
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        body = func(*args, **kwargs)
        res = HTTPResponse(status=200, body=body)
        res.set_header('Content-type', 'text/javascript')
        return res
    return wrapper

@_js_renderer
def render_js_module(module):
    """
    テンプレートからJavaScriptを生成
    
    Attributes:
        module (str): 呼び出すモジュール名
    
    Returns:
        生成されたJavaScript
    """
    
    # 公開したPython関数名からモジュール作成
    list_func_name = list(_expose_module[module].keys())
    return _template_js_module.render(module=module, list_func_name=list_func_name)

@_js_renderer
def render_window_position():
    """
    画面サイズ・位置を変更するJavaScript生成
    
    Returns:
        画面サイズ・位置を変更するJavaScript
    """
    
    # 公開したPython関数名からモジュール作成
    return _template_window_position.render(size=_config.size, position=_config.position)
