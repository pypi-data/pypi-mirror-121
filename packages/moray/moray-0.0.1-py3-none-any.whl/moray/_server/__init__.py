"""
morayで起動する内部サーバ設定
http://localhost:port/
"""

import bottle, logging, pkg_resources, os, socket, time
from bottle.ext.websocket import GeventWebSocketServer, websocket
from functools import wraps
from threading import Thread

import moray
from moray import _config, _module
from moray._module import py

_root_static_module = pkg_resources.resource_filename('moray', r'_module\static')

app = bottle.Bottle()
_websockets=[]

_logger = logging.getLogger(__name__)

def _log_to_logger(func):
    """
    Bottleログ出力プラグイン
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        # リクエスト情報ログ出力
        request = bottle.request
        request_str = '{0} {1} {2}'.format(request.remote_addr, request.method, request.urlparts.path)
        _logger.info('Request: {0}'.format(request_str))
        
        try:
            # app.routeを設定した関数を呼び出す
            result = func(*args, **kwargs)
            
            # レスポンス情報ログ出力
            if isinstance(result, bottle.HTTPResponse):
                
                # ステータスコード取得
                status_code = result.status_code
                response_str = 'Response: {0} {1}'.format(request_str, status_code)
                
                # ログレベルを分けてログ出力
                if status_code < 400:
                    _logger.info(response_str)
                else:
                    _logger.error(response_str)
                
                # 返り値がない場合のログ出力
            elif result is None:
                _logger.info('No Response: {0}'.format(request_str))
                
                # 返り値の型が正常でない場合のログ出力
            else:
                _logger.warn('resonse is not "HTTPResponse" type or "None".')
                _logger.warn('Response: {0} {1}'.format(request_str, 'xxx'))
                
                # サーバ側に処理を任せるためにそのまま返却
                pass
            
            return result
        except Exception as e:
            _logger.exception('inner Bottle server catched exception.')
            
            # サーバ側に処理を任せるためにリスロー
            raise
    return wrapper

# Bottleログ出力プラグインインストール
app.install(_log_to_logger)

@app.route('/moray/confirm_running')
def run_check():
    """
    サーバ起動確認用
    
    Returns:
        固定メッセージページ
    """
    
    return

@app.route('/moray/core/window_position')
def window_position_script():
    """
    画面サイズ・位置を変更するJavaScriptを生成
    
    Returns:
        画面サイズ・位置を変更するJavaScript
    """
    
    return py.render_window_position()

@app.route('/moray/py/<py_module>.js')
def py_module_script(py_module):
    """
    JavaScriptからPythonを呼び出すためのjsモジュールを生成
    
    Returns:
        JavaScriptからPythonを呼び出すためのjsモジュール
    """
    
    return py.render_js_module(py_module)

@app.route('/moray/static/<static_module>')
def static_module_script(static_module):
    """
    静的jsモジュールを生成
    
    Returns:
        静的jsモジュール
    """
    
    return bottle.static_file('{0}.js'.format(static_module), root=_root_static_module)

@app.route('/moray.js')
def moray_script():
    """
    JavaScript関数を公開するためのjsモジュールを生成
    
    Returns:
        JavaScript関数を公開するためのjsモジュール
    """
    
    return bottle.static_file('moray.js', root=_root_static_module)

@app.route('/moray/ws', apply=[websocket])
def bottle_websocket(ws):
    """
    WebSocketの受け取り口
    
    Attributes:
        ws (geventwebsocket.websocket.WebSocket): WebSocket接続オブジェクト
    """
    
    _logger.info('WebSocket is opened.')
    
    _websockets.append(ws)
    while True:
        msg = ws.receive()
        if msg is None:
            break
        
        # スレッドを分けて処理
        deamon_t = _module.WebsocketReact(ws, msg)
        deamon_t.setDaemon(False)
        deamon_t.start()
    
    # websocketが閉じられた際の処理
    deamon_t = Thread(target=_onclose_websocket, args=(ws,))
    deamon_t.setDaemon(False)
    deamon_t.start()

@app.route('/')
@app.route('/<path:path>')
def page(path = 'index.html'):
    """
    root配下のファイルを返却
        .html, .js, .css など
    
    Returns:
        root配下のページ
    """
    if path[-1] == '/':
        path += 'index.html'
    
    return bottle.static_file(path, root=_config.root)

def run():
    """
    サーバ起動
    """
    
    _logger.debug('running moray on "{0}:{1}".'.format(_config.host, _config.port))
    app.run(
        host = _config.host,
        port = _config.port,
        reloader = False,
        debug = False,
        server = GeventWebSocketServer,
        quiet = True
    )

def generate_port(port):
    """
    ポート番号を生成
    
    Returns:
        int: 生成したポート番号
    """
    
    if port == 0:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('localhost', 0))
            port = sock.getsockname()[1]
    
    return port

def generate_start_url():
    """
    初期表示URLを生成
    
    Returns:
        str: 初期表示URL
    """
    
    return 'http://localhost:{0}/{1}'.format(_config.port, _config.start_page)

def generate_confirm_running_url():
    """
    サーバ起動確認用URLを生成
    
    Returns:
        str: サーバ起動確認用URL
    """
    
    return 'http://localhost:{0}/moray/confirm_running'.format(_config.port)

@moray._error_handle(_logger, True)
def _onclose_websocket(ws):
    """
    WebSocketが閉じられた際の処理
    
    Attributes:
        ws (geventwebsocket.websocket.WebSocket): WebSocket接続オブジェクト
    """
    
    _logger.info('closing WebSocket.')
    
    # websocketに紐づくメモリを解放
    _module.unexpose(ws)
    _websockets.remove(ws)
    _logger.info('WebSocket is closed.')
    
    # 接続がない場合は終了
    check_exist_websocket()

def check_exist_websocket():
    """
    websocketの接続有無をチェック
    接続がない場合は終了
    """
    
    if len(_websockets) == 0:
        time.sleep(3)
        if len(_websockets) == 0:
            _logger.info('exiting moray application.')
            os._exit(0)
