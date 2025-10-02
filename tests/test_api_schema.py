from context import api
import schemathesis

base_url = "http://127.0.0.1:8000/"
app = api.setup()
print(app.router)
schema = schemathesis.openapi.from_url(base_url + app.openapi_url)
schema.config.checks.update(excluded_check_names=["positive_data_acceptance"])
schema.config.output.sanitization.update(enabled=False)

@schema.parametrize()
def test_routes(case):
    case.call_and_validate(headers={"Authorization": "Bearer secret-token"})