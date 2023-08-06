"""
このモジュールで使用するユーザ定義例外
"""

class MorayRuntimeError(RuntimeError):
    """
    このライブラリ内のRuntimeError
    """
    
    pass

class SupportError(MorayRuntimeError):
    """
    サポート対象外のものに対する例外
    """
    
    pass

class ConfigurationError(MorayRuntimeError):
    """
    設定に関する例外
    """
    
    pass

class MorayTimeoutError(MorayRuntimeError):
    """
    タイムアウトに関する例外
    """
    
    pass
