#!/usr/bin/env python3

import os
import time

class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def log(self, level, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        log_message = f'[{timestamp}] [{level.upper()}] {message}\n'
        try:
            with open(self.log_file, 'a') as f:
                f.write(log_message)
        except Exception as e:
            print(f"Error logging message: {e}")

    def debug(self, message):
        self.log('debug', message)

    def info(self, message):
        self.log('info', message)

    def warning(self, message):
        self.log('warning', message)

    def error(self, message):
        self.log('error', message)
