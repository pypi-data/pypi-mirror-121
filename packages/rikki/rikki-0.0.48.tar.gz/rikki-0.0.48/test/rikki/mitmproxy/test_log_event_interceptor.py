from rikki.mitmproxy.model import Request
from mitmproxy.log import LogEntry
from mitmproxy import http
from rikki.mitmproxy.delegate_accumulate import Accumulate, AccumulateFilterConfig
from rikki.mitmproxy.log_event_interceptor import LogEventInterceptor
from unittest import TestCase

class PersistAccumulate(Accumulate):

    def __init__(self, filter_config: AccumulateFilterConfig):
        super().__init__(filter_config)
        self.last_flow: http.HTTPFlow = None

    def request(self, flow: http.HTTPFlow):
        self.last_flow = flow


class TestLogEventInterceptor(TestCase):

    def test_should_parse_host(self):
        accumulate = PersistAccumulate(filter_config=AccumulateFilterConfig())
        instance = LogEventInterceptor(delegate=accumulate)

        instance.add_log(LogEntry(msg='127.0.0.1:61217: server connect mail-attachment.googleusercontent.com:443 (142.250.179.161:443)', level=''))

        assert accumulate.last_flow.request.host == 'mail-attachment.googleusercontent.com'
        assert accumulate.last_flow.request.port == 443

    def test_should_not_fail_with_incorrect_input(self):
        accumulate = PersistAccumulate(filter_config=AccumulateFilterConfig())
        instance = LogEventInterceptor(delegate=accumulate)

        instance.add_log(LogEntry(msg='127.0.0.1:61217: server connect ', level=''))

        assert accumulate.last_flow == None

        instance.add_log(LogEntry(msg='127.0.0.1:61217: server connect mail-attachment.googleusercontent.com:443', level=''))

        assert accumulate.last_flow.request.host == 'mail-attachment.googleusercontent.com'
        assert accumulate.last_flow.request.port == 443

    def test_should_be_positive_compatible_with_accumulate(self):
        accumulate = Accumulate(filter_config=AccumulateFilterConfig(request=Request(host='mail-attachment.googleusercontent.com')))
        instance = LogEventInterceptor(delegate=accumulate)

        instance.add_log(LogEntry(msg='127.0.0.1:61217: server connect mail-attachment.googleusercontent.com:443 (142.250.179.161:443)', level=''))

        assert accumulate.accumulated_items[0].request.host == 'mail-attachment.googleusercontent.com'
        assert accumulate.accumulated_items[0].request.port == 443

    def test_should_be_negative_compatible_with_accumulate(self):
        accumulate = Accumulate(filter_config=AccumulateFilterConfig())
        instance = LogEventInterceptor(delegate=accumulate)

        instance.add_log(LogEntry(msg='127.0.0.1:61217: server connect mail-attachment.googleusercontent.com:443 (142.250.179.161:443)', level=''))

        assert len(accumulate.accumulated_items) == 0      