#region Logging
LOG_FORMAT: str = '[%(asctime)s] [%(levelname)s] %(message)s at %(pathname)s, line %(lineno)d, Function: %(funcName)s'
"""
Format String for the logger. 

For available variables, see https://docs.python.org/3/library/logging.html#logrecord-attributes
"""
LOG_TO_CONSOLE: bool = True
"""
If True, logs to Stdout
"""
#endregion