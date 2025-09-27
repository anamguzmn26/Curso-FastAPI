from prometheus_client import Counter, Histogram, Gauge
import psutil

class APIMetrics:
    def __init__(self, domain: str = 'bakery'):
        self.request_counter = Counter(f'{domain}_requests_total', 'Total de requests', ['method','endpoint','status'])
        self.response_time = Histogram(f'{domain}_response_duration_seconds','Response time',['method','endpoint'], buckets=[0.1,0.25,0.5,1,2.5,5])
        self.system_cpu = Gauge(f'{domain}_cpu_usage_percent','CPU')

    def record_request(self, method, endpoint, status, duration):
        try:
            self.request_counter.labels(method=method, endpoint=endpoint, status=str(status)).inc()
            self.response_time.labels(method=method, endpoint=endpoint).observe(duration)
        except Exception:
            pass

    def update_system_metrics(self):
        try:
            self.system_cpu.set(psutil.cpu_percent())
        except Exception:
            pass
