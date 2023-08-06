"""
chromeをアプリモードで起動するためのコマンドを生成する
"""

import sys, os

from moray.exception import SupportError

name = 'chrome'

def create_command(path, url, cmdline_args):
    """
    起動コマンド生成
    
    Attributes:
        path (str): chromeコマンドのパス
        url (str): 接続先のURL
        cmdline_args (list<str>): コマンドライン引数
    
    Returns:
        list<str>: 生成された起動コマンド
    """
    
    return [path, '--app=' + url] + cmdline_args

def find_path():
    """
    chromeの実行ファイルパスを取得
    
    Returns:
        str: chromeの実行ファイルパス
    
    Raises:
        SupportError: 対象外OSの場合
    """
    
    if sys.platform in ('win32', 'win64'):
        
        # Windowsの場合
        return _find_chrome_windows()
    else:
        
        # 対象外OSの場合
        # このOSはサポート対象外のOSです。
        error_msg = 'This OS is not a supported OS.'
        raise SupportError(error_msg)

def _find_chrome_windows():
    """
    Windowsのchromeの実行ファイルパスを取得
    
    Returns:
        str: Windowsのchromeの実行ファイルパス
    
    Raises:
        FileNotFoundError: ブラウザ実行ファイル不明
    """
    
    import winreg
    reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'
    
    # HKEY_CURRENT_USER: 現在のユーザーのレジストリ設定
    # HKEY_LOCAL_MACHINE: すべてのユーザーのレジストリ設定
    for reg_entry in winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE:
        try:
            
            # レジストリからchromeの実行ファイルパスを取得
            with winreg.OpenKey(reg_entry, reg_path, 0, winreg.KEY_READ) as reg_key:
                chrome_path = winreg.QueryValueEx(reg_key, None)[0]
                if os.path.isfile(chrome_path):
                    return chrome_path
        except Exception as e:
            pass
    
    # chrome.exe が見つかりませんでした
    error_msg = '"chrome.exe" is not found.'
    raise FileNotFoundError(error_msg)
