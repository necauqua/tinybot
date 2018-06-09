
import logging

__all__ = 'get'

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

FORMAT = '[{asctime}.{msecs:03.0f}][{name:^14}][{levelname:>8}] - {message}'
ch.setFormatter(logging.Formatter(FORMAT, '1%F|%T', '{'))

root = logging.getLogger('tinybot')
root.setLevel(logging.DEBUG)
root.addHandler(ch)

# so that importing this stupid package makes at least some sense
get = logging.getLogger
