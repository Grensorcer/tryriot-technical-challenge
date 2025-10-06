from context import api
import schemathesis

app = api.setup()

schema = schemathesis.openapi.from_asgi(app.openapi_url, app)
schema.config.checks.update(excluded_check_names=["positive_data_acceptance"])
schema.config.output.sanitization.update(enabled=False)

@schema.parametrize()
def test_routes(case):
    case.call_and_validate()
