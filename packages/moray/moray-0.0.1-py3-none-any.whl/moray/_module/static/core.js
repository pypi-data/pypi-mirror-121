import positioning_window from '/moray/core/window_position'

// 画面サイズ・位置変更
positioning_window();

// morayオブジェクト
let moray = new Object();
moray.onclose = function(evt){};

// WebSocketオブジェクト
let ws;

// 公開したJavaScript関数
let exposed_js = {};

// 呼び出し中データ
let calling_promise = {};

// 未送信データ
let unsended_data = [];

// ブラウザがWebSocketに対応しているかチェック
if (!window.WebSocket) {
    if (window.MozWebSocket) {
        window.WebSocket = window.MozWebSocket;
    } else {
        throw new Error("Your browser doesn't support WebSockets.");
    }
}

// WebSocket接続
let host = window.location.host;
ws = new WebSocket('ws://' + host + '/moray/ws');
ws.onopen = function(evt) {

    // 未送信データを送信
    let data_length = unsended_data.length;
    for(let i = 0; i < data_length; i++){
        ws.send(unsended_data.pop());
    }
}
ws.onmessage = function(evt) {
    let data = JSON.parse(evt.data);

    // 呼び出したPythonからの返却値の場合
    if (data.return) {

        // IDを確認
        if (!(data.id in calling_promise)) {
            return;
        }

        // 成否結果をPromise結果に登録
        if (data.is_success) {
            calling_promise[data.id].resolve(data.result);
        } else {
            calling_promise[data.id].reject(data.result);
        }
        delete calling_promise[data.id];

    // PythonからのJavScript関数呼び出しの場合
    } else {
        let result;
        let is_success = true;

        // JavScript関数呼び出し
        try {
            result = exposed_js[data.func_name].apply(null, data.args);
            if (typeof result === "undefined") {
                result = null;
            }
        } catch (e) {
            is_success = false;
            result = 'called javascript function is faild.';
            console.log(e);
        }

        // JavScript関数の実行結果を返却
        let return_data = JSON.stringify({
            id: data.id,
            method: 'return',
            result: result,
            is_success: is_success
        });
        ws.send(return_data);
    }
}
ws.onclose = function(evt) {
    moray.onclose(null);
}

// 一意なIDを作成
let uniqueId = function(digits) {
    var strong = typeof digits !== 'undefined' ? digits : 1000;
    return Date.now().toString(16) + Math.floor(strong * Math.random()).toString(16);
}

// メッセージ送信
let send_msg = function(data) {
    if (ws.readyState == WebSocket.OPEN) {
        ws.send(data);
    } else {
        unsended_data.push(data);
    }
}

// pythonを呼び出す
let call_python = function(module, func_name, args) {

    // 一意なIDを作成
    let id = uniqueId();

    // 引数をリスト化
    let arg_array = [];
    for(let i = 0; i < args.length; i++){
        arg_array.push(args[i]);
    }

    // 送信文字列作成
    let data = JSON.stringify({
        id: id,
        method: 'call',
        module: module,
        func_name: func_name,
        args: arg_array
    });

    // Python側にデータ送信
    return new Promise((reso, reje) => {
        send_msg(data);
        calling_promise[id] = {resolve: reso, reject: reje};
    });
}

// JavaScriptの関数を公開
moray.expose = function(func) {

    // 公開するJavaScriptの関数を登録
    let func_name = func.name;
    exposed_js[func_name] = func;

    // JavaScriptの関数をPython側に公開
    let data = JSON.stringify({
        method: 'expose',
        func_name: func_name
    });
    send_msg(data);
}

export {call_python, moray};
