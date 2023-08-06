"""
呼び出す関数を管理
呼び出す・呼び出される関数を制御
"""

import json, logging, random, threading, time
from datetime import datetime

import moray
from moray import _checker
from moray._module import py
from moray.exception import MorayRuntimeError, MorayTimeoutError

_ID = 'id'
_RETURN = 'return'
_CALL = 'call'
_EXPOSE = 'expose'
_METHOD = 'method'
_MODULE = 'module'
_FUNC_NAME = 'func_name'
_ARGS = 'args'
_RESULT = 'result'
_IS_SUCCESS = 'is_success'

_js_funcs ={}
_call_result = {}

_logger = logging.getLogger(__name__)

class WebsocketReact(threading.Thread):
    """
    受信したメッセージによって処理を実行するスレッドクラス
    
    Attributes:
        ws (geventwebsocket.websocket.WebSocket): WebSocket接続オブジェクト
        msg (str): 受信したメッセージ
    """
    
    def __init__(self, ws, msg):
        super().__init__()
        self.__ws = ws
        self.__msg = msg
        self.__parsed_msg = None
    
    @property
    def ws(self):
        """
        読み取り専用WebSocket接続オブジェクト
        
        Returns:
            WebSocket接続オブジェクト
        """
        
        return self.__ws
    
    @moray._error_handle(_logger)
    def run(self):
        """
        受信したメッセージによって処理を実行
        
        Raises:
            MorayRuntimeError: 入力値エラー
        """
        
        _logger.debug('received data: {0}'.format(self.__msg))
        
        self.__parsed_msg = json.loads(self.__msg)
        method = self.__parsed_msg[_METHOD]
        _checker.check_str(method, _METHOD)
        
        if method == _CALL:
            self.__called()
        elif method == _RETURN:
            self.__returned()
        elif method == _EXPOSE:
            self.__exposed()
        else:
            raise MorayRuntimeError('not correct "{0}".'.format(_METHOD))
    
    def __called(self):
        """
        呼び出されたPythonの関数を実行
        """
        
        id = self.__parsed_msg[_ID]
        _checker.check_str(id, _ID)
        module = self.__parsed_msg[_MODULE]
        _checker.check_str(module, _MODULE)
        func_name = self.__parsed_msg[_FUNC_NAME]
        _checker.check_str(func_name, _FUNC_NAME)
        args = self.__parsed_msg[_ARGS]
        _checker.check_list_or_tuple(args, _ARGS)
        
        result, is_success = _call_py_func(module, func_name, args)
        
        return_msg = {}
        return_msg[_ID] = id
        return_msg[_RETURN] = True
        return_msg[_RESULT] = result
        return_msg[_IS_SUCCESS] = is_success
        msg = json.dumps(return_msg)
        
        _logger.debug('send data: {0}'.format(msg))
        self.__ws.send(msg)
    
    def __returned(self):
        """
        呼び出したJavaScriptの結果を格納
        """
        
        id = self.__parsed_msg[_ID]
        _checker.check_str(id, _ID)
        is_success = self.__parsed_msg[_IS_SUCCESS]
        _checker.check_bool(is_success, _IS_SUCCESS)
        result = self.__parsed_msg[_RESULT]
        _checker.check_str(result, _RESULT)
        
        _call_result[id] = {
            _IS_SUCCESS: is_success,
            _RESULT: result
        }
    
    def __exposed(self):
        """
        exposeされたJavaScript関数を登録
        """
        
        func_name = self.__parsed_msg[_FUNC_NAME]
        _checker.check_str(func_name, _FUNC_NAME)
        setattr(moray.js, func_name, _create_js_func(self.__ws, func_name))
        _logger.debug('exposed Javascript function: {0}'.format(func_name))

def _call_py_func(module, func_name, args):
    """
    exposeした関数を呼び出す
    
    Attributes:
        module (str): 呼び出すモジュール名
        func_name (str): 呼び出す関数名
        args (dict): 引数
    
    Returns:
        関数の実行結果
        実行成否(True:成功, False:失敗)
    """
    
    try:
        result = py.call(module, func_name, args)
        return result, True
    except Exception as e:
        result = 'called python function is faild.'
        _logger.exception(result)
        return result, False

def _create_js_func(ws, func_name):
    """
    PythonからJavaScriptを呼ぶ関数を生成
    
    Attributes:
        ws (geventwebsocket.websocket.WebSocket): WebSocket接続オブジェクト
        func_name (str): 関数名
    
    Returns:
        生成したPythonからJavaScriptを呼ぶ関数
    """
    
    _js_funcs.setdefault(ws, [])
    if not func_name in _js_funcs[ws]:
        _js_funcs[ws].append(func_name)
    
    def call_js(*args):
        """
        PythonからJavaScriptを呼ぶ関数
        
        Attributes:
            args: 引数
            
        Raises:
            MorayRuntimeError: 呼び出したJavaScript側でエラー発生
        
        Returns:
            実行結果取得関数
        """
        
        ws = threading.current_thread().ws
        
        if ws not in _js_funcs:
            raise MorayRuntimeError('websocket is not connected.')
        
        if func_name not in _js_funcs[ws]:
            raise MorayRuntimeError('"{0}" is not exposed.'.format(func_name))
        
        id = _uniqueId()
        
        call_msg = {}
        call_msg[_ID] = id
        call_msg[_RETURN] = False
        call_msg[_FUNC_NAME] = func_name
        call_msg[_ARGS] = args
        msg = json.dumps(call_msg)
        
        _logger.debug('send data: {0}'.format(msg))
        ws.send(msg)
        
        def get_result():
            """
            実行結果取得関数
            
            Returns:
                実行結果
            
            Raises:
                MorayRuntimeError: 呼び出したJavaScript側でエラー発生
                MorayTimeoutError: 実行結果取得タイムアウトエラー
            
            Note:
                _call_result にはJavaScriptからの返却時の処理で格納される
            """
            
            start_time = time.time()
            while time.time() - start_time < 10:
                if id in _call_result:
                    result = _call_result[id][_RESULT]
                    is_success = _call_result[id][_IS_SUCCESS]
                    del _call_result[id]
                    if is_success:
                        return result
                    else:
                        raise MorayRuntimeError(result)
                
                time.sleep(1)
            
            raise MorayTimeoutError('Could not receive execution results from JavaScript.')
        
        return get_result
    
    return call_js

def unexpose(ws):
    """
    exposeされたJavaScript関数を登録解除
    
    Attributes:
        ws (geventwebsocket.websocket.WebSocket): WebSocket接続オブジェクト
    """
    
    # exposeされたJavaScript関数がない場合は終了
    if not ws in _js_funcs:
        return
    
    # exposeされたJavaScript関数を登録解除
    js_funcs =_js_funcs[ws]
    del _js_funcs[ws]
    
    for _, v in _js_funcs.items():
        for func_name in tuple(js_funcs):
            if func_name in v:
                js_funcs.remove(func_name)
    
    for func_name in js_funcs:
        delattr(moray.js, func_name)
        _logger.debug('unexposed Javascript function: {0}'.format(func_name))

def _uniqueId(strong = 1000):
    """
    日付を基にユニークキー生成
    ロジックはJavaScript版と同じ
    
    Attributes:
        strong (int, optional): 乱数の範囲
    
    Returns:
        生成したユニークキー
    """
    
    return hex(int(datetime.now().timestamp() * 1000))[2:] + hex(int(random.random() * strong))[2:]
