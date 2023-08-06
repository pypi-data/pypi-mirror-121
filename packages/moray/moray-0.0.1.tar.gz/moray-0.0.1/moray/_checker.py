"""
moray内で使用する型チェックロジック
"""

import re
from pathlib import Path

from moray.exception import MorayRuntimeError

def check_not_None(value, name):
    """
    Noneチェック
    
    Attributes:
        value: チェック対象変数
        name (str): チェック対象項目名
    
    Raises:
        MorayRuntimeError: チェックエラー
    """
    
    if value is None:
        msg = '"{0}" is None.'.format(name)
        raise MorayRuntimeError(msg)

def check_str(value, name):
    """
    strチェック
    
    Attributes:
        value: チェック対象変数
        name (str): チェック対象項目名
    
    Raises:
        MorayRuntimeError: チェックエラー
    """
    
    if type(value) is not str:
        msg = '"{0}" is not "str" type.'.format(name)
        raise MorayRuntimeError(msg)

def check_int(value, name):
    """
    intチェック
    
    Attributes:
        value: チェック対象変数
        name (str): チェック対象項目名
    
    Raises:
        MorayRuntimeError: チェックエラー
    """
    
    if type(value) is not int:
        msg = '"{0}" is not "int" type.'.format(name)
        raise MorayRuntimeError(msg)

def check_bool(value, name):
    """
    boolチェック
    
    Attributes:
        value: チェック対象変数
        name (str): チェック対象項目名
    
    Raises:
        MorayRuntimeError: チェックエラー
    """
    
    if type(value) is not bool:
        msg = '"{0}" is not "bool" type.'.format(name)
        raise MorayRuntimeError(msg)

def check_list_or_tuple(value, name):
    """
    list of tupleチェック
    
    Attributes:
        value: チェック対象変数
        name (str): チェック対象項目名
    
    Raises:
        MorayRuntimeError: チェックエラー
    """
    
    if type(value) is not list and type(value) is not tuple:
        msg = '"{0}" is not "list" or "tuple" type.'.format(name)
        raise MorayRuntimeError(msg)

def check_not_whitespace(value, name):
    """
    空白はエラー
    
    Attributes:
        value (str): チェック対象変数
        name (str): チェック対象項目名
    
    Raises:
        MorayRuntimeError: チェックエラー
    """
    
    value = value.strip(' ')
    if value == '':
        msg = '"{0}" is whitespace.'.format(name)
        raise MorayRuntimeError(msg)

def check_exist(value):
    """
    存在チェック
    
    Attributes:
        value (str): チェック対象変数
    
    Raises:
        MorayRuntimeError: チェックエラー
    """
    
    value = Path(value.strip(' '))
    if not value.exists():
        msg = '"{0}" is not exist.'.format(str(value))
        raise MorayRuntimeError(msg)

def check_2_int_list_or_tuple(value, name):
    """
    list<int, int> or tuple<int, int>チェック
    
    Attributes:
        value (list or tuple): チェック対象変数
        name (str): チェック対象項目名
    
    Raises:
        MorayRuntimeError: チェックエラー
    """
    
    # 要素数チェック
    msg = '"{0}" has only 2 "int" type.'.format(name)
    if len(value) != 2:
        raise MorayRuntimeError(msg)
    
    # 要素内の型チェック
    for item in value:
        if type(item) is not int:
            raise MorayRuntimeError(msg)

def check_host(value, name):
    """
    HOSTチェック
        localhost
        xxx.xxx.xxx.xxx(0 <= xxx <= 255)
    
    Attributes:
        value (str): サーバのホスト
        name (str): チェック対象項目名
    
    Raises:
        MorayRuntimeError: チェックエラー
    """
    
    msg = '"{0}" is not "localhost" or "xxx.xxx.xxx.xxx".(0 <= xxx <= 255)'.format(name)
    if value == 'localhost':
        return
    elif re.match(r'\d+\.\d+\.\d+\.\d+', value) is None:
        raise MorayRuntimeError(msg)
    else:
        for num in value.split('.'):
            if int(num) < 0 or 255 < int(num):
                raise MorayRuntimeError(msg)

def check_port(value, name):
    """
    PORTチェック
        port = 0 or 1025 <= port <= 65535
    
    Attributes:
        value (int): サーバのポート番号
        name (str): チェック対象項目名
    
    Raises:
        MorayRuntimeError: チェックエラー
    """
    
    if value == 0:
        pass
    elif value < 1025 or 65535 < value:
        msg = '"{0}" is less than 1025 or greater than 65535.'.format(name)
        raise MorayRuntimeError(msg)
