import unittest

from api_store.actions_store_builder import build_actions_store
from api_store.api_store_builder import build_api_store


HR_OPENAPI = {
    "openapi": "3.1.0",
    "paths": {
        "/employees/": {
            "get": {"responses": {"200": {"description": "ok"}}},
            "post": {
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/EmployeeCreate"}
                        }
                    }
                },
                "responses": {"200": {"description": "created"}},
            },
        },
        "/employees/{emp_id}/terminate": {
            "put": {
                "parameters": [
                    {
                        "name": "emp_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/TerminateRequest"}
                        }
                    }
                },
                "responses": {"200": {"description": "terminated"}},
            }
        },
    },
    "components": {
        "schemas": {
            "EmployeeCreate": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "role": {"type": "string"},
                    "salary": {"type": "number"},
                },
            },
            "TerminateRequest": {
                "type": "object",
                "properties": {"effective_date": {"type": "string"}},
            },
        }
    },
}


class ActionStoreTests(unittest.TestCase):
    def test_hr_spec_exposes_create_and_terminate_only(self):
        api_store = build_api_store(HR_OPENAPI)
        actions = build_actions_store(api_store)

        self.assertEqual(
            set(actions),
            {"post_employees", "put_employees_emp_id_terminate"},
        )
        self.assertNotIn("get_employees", actions)
        self.assertEqual(
            actions["post_employees"]["inputs"]["body"],
            {"name": "string", "role": "string", "salary": "number"},
        )
        terminate = actions["put_employees_emp_id_terminate"]["inputs"]
        self.assertEqual(terminate["path_params"], {"emp_id": "integer"})
        self.assertEqual(terminate["body"], {"effective_date": "string"})


if __name__ == "__main__":
    unittest.main()
