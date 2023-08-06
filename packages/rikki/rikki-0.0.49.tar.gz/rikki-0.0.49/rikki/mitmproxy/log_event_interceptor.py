import re
from rikki.mitmproxy.util import build_flow
from rikki.mitmproxy.model import Request
from mitmproxy.addons import eventstore
from mitmproxy.log import LogEntry

class LogEventInterceptor(eventstore.EventStore):

    def __init__(self, delegate, size=10000):
        super().__init__(size=size)
        self._delegate = delegate

    def add_log(self, entry: LogEntry) -> None:
        self.data.append(entry)
        self.sig_add.send(self, entry=entry)
        x = re.search(r"(\s[^\s]*:\d*)(\s\(.*\))?", entry.msg)

        host = ''
        port = ''
        ip = ''

        if x and x.group(1):
            hostGroup = x.group(1).strip().split(':')
            host = hostGroup[0]
            port = hostGroup[1]
        if x and x.group(2):
            ipGroup = x.group(2).strip().split(':')
            ip = ipGroup[0]    

        if host:
            self._delegate.request(build_flow(request = Request(host=host, port=int(port))))