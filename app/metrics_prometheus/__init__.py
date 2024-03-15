from prometheus_fastapi_instrumentator import Instrumentator, metrics

instrumentator = Instrumentator()
instrumentator.add(metrics.default())
instrumentator.add(
    metrics.requests(
        'http_codes', 'HTTP Codes', should_include_status=True, should_include_method=True,
        should_include_handler=True
    )
)
