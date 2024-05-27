def get_json_handler():
    import logging 
    import json
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                'level': record.levelname,
                'message': record.msg,
                'time': self.formatTime(record, self.datefmt),
                'filename': record.filename,
                'lineno': record.lineno
            }
            if hasattr(record, 'request'):
                log_record['request'] = {
                    'method': record.request.method,
                    'url': record.request.url,
                    'remote_addr': record.request.remote_addr
                }
            return json.dumps(log_record)
        
    json_formatter = JSONFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(json_formatter)
    return handler