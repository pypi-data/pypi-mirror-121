import httpx


class InvalidApiKey(Exception):
    """ Invalid api key, or no key set"""


class Integromat:
    def __init__(self, api_key):
        if not api_key:
            raise InvalidApiKey()
        self.api_key = api_key
        self.base_url = "https://api.integromat.com/v1"
        self.default_headers = {
            "Authorization": f"Token {self.api_key}",
            "x-imt-apps-sdk-version": "1.3.9"
        }


class IMTBasic(Integromat):
    def __init__(self, api_key):
        super().__init__(api_key)

    def whoami(self):
        r = httpx.get(self.base_url + "/whoami", headers=self.default_headers)
        return r.json()


class AioIMTBasic(IMTBasic):
    def __init__(self, api_key):
        super().__init__(api_key)

    async def whoami(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(self.base_url + "/whoami", headers=self.default_headers)
            return r.json()


class Apps(Integromat):
    def __init__(self, api_key):
        super().__init__(api_key)

    def list_apps(self):
        r = httpx.get(self.base_url + "/app", headers=self.default_headers)
        return r.json()

    def create_app(self,
                   name,
                   label,
                   theme='#CCCCCC',
                   language='en',
                   private=True,
                   countries=None):
        if countries is None:
            countries = ['us']
        body = {
            'name': name,
            'label': label,
            'theme':  theme,
            'language': language,
            'private': private,
            'countries': countries
        }
        r = httpx.post(self.base_url + "/app",
                       json=body,
                       headers=self.default_headers)
        return r.json()

    def delete_app(self, name, version):
        r = httpx.delete(self.base_url + f"/app/{name}/{version}", headers=self.default_headers)
        return r.json()


class AioApps(Integromat):
    def __init__(self, api_key):
        super().__init__(api_key)

    async def list_apps(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(self.base_url + "/app", headers=self.default_headers)
            return r.json()

    async def create_app(self,
                         name,
                         label,
                         theme='#CCCCCC',
                         language='en',
                         private=True,
                         countries=None):
        if countries is None:
            countries = ['us']
        body = {
            'name': name,
            'label': label,
            'theme':  theme,
            'language': language,
            'private': private,
            'countries': countries
        }
        async with httpx.AsyncClient() as client:
            r = await client.post(self.base_url + "/app",
                                  json=body,
                                  headers=self.default_headers)
            return r.json()

    async def delete_app(self, name, version):
        async with httpx.AsyncClient() as client:
            r = await client.delete(self.base_url + f"/app/{name}/{version}", headers=self.default_headers)
            return r.json()


MTYPE_ACTION = 4
MTYPE_SEARCH = 9
MTYPE_TRIGGER = 1
MTYPE_INSTANT = 10
MTYPE_RESPONDER = 11
MTYPE_UNIVERSAL = 12


class Modules(Integromat):
    def __init__(self, api_key, app_name, app_version):
        super().__init__(api_key)
        self.base_url = self.base_url + f"/app/{app_name}/{app_version}/module"

    def list(self):
        r = httpx.get(self.base_url, headers=self.default_headers)
        return r.json()

    def create(self, name, label, description, type_id=MTYPE_ACTION):
        body = {
          "name": name,
          "label": label,
          "type_id": type_id,
          "description": description
        }
        r = httpx.post(self.base_url, json=body, headers=self.default_headers)
        return r.json()

    def add_connection(self, module, connection_name):
        headers = {
            ** self.default_headers,
            "content-type": "text/plain"
        }
        r = httpx.put(self.base_url + f"/{module}/connection", content=connection_name, headers=headers)
        return r.json()

    def add_webhook(self, module, webhook_name):
        headers = {
            ** self.default_headers,
            "content-type": "text/plain"
        }
        r = httpx.put(self.base_url + f"/{module}/webhook", content=webhook_name, headers=headers)
        return r.json()

    def update_communications(self, module, body):
        r = httpx.put(self.base_url + f"/{module}/api", json=body, headers=self.default_headers)
        return r.json()

    def update_parameters(self, module, body):
        r = httpx.put(self.base_url + f"/{module}/parameters", json=body, headers=self.default_headers)
        return r.json()

    def update_mappable_parameters(self, module, body):
        r = httpx.put(self.base_url + f"/{module}/expect", json=body, headers=self.default_headers)
        return r.json()

    def update_interface(self, module, body):
        r = httpx.put(self.base_url + f"/{module}/interface", json=body, headers=self.default_headers)
        return r.json()

    def update_samples(self, module, body):
        r = httpx.put(self.base_url + f"/{module}/samples", json=body, headers=self.default_headers)
        return r.json()

    def update_scope(self, module, body):
        r = httpx.put(self.base_url + f"/{module}/scope", json=body, headers=self.default_headers)
        return r.json()


class RPCs(Integromat):
    def __init__(self, api_key, app_name, app_version):
        super().__init__(api_key)
        self.base_url = self.base_url + f"/app/{app_name}/{app_version}/rpc"

    def create(self, name, label):
        body = {
            "name": name,
            "label": label
        }
        r = httpx.post(self.base_url, json=body, headers=self.default_headers)
        return r.json()

    def add_connection(self, rpc_name, connection_name):
        headers = {
            ** self.default_headers,
            "content-type": "text/plain"
        }
        r = httpx.put(self.base_url + f"/{rpc_name}/connection", content=connection_name, headers=headers)
        return r.json()

    def list(self):
        r = httpx.get(self.base_url, headers=self.default_headers)
        return r.json()

    def update_communications(self, rpc_name, body):
        r = httpx.put(self.base_url + f"/{rpc_name}/api", json=body, headers=self.default_headers)
        return r.json()

    def update_parameters(self, rpc_name, body):
        r = httpx.put(self.base_url + f"/{rpc_name}/parameters", json=body, headers=self.default_headers)
        return r.json()


class Functions(Integromat):
    def __init__(self, api_key, app_name, app_version):
        super().__init__(api_key)
        self.base_url = self.base_url + f"/app/{app_name}/{app_version}/function"

    def create(self, name):
        body = {
            "name": name
        }
        r = httpx.post(self.base_url, json=body, headers=self.default_headers)
        return r.json()

    def list(self):
        r = httpx.get(self.base_url, headers=self.default_headers)
        return r.json()

    def update_code(self, function_name, code):
        headers = {
            'Content-Type': 'application/javascript',
            **self.default_headers,
        }
        with httpx.Client() as client:
            if function_name not in code:
                raise Exception('Function name does not match in code')
            r = client.put(self.base_url + f"/{function_name}/code", content=code, headers=headers)
            return r.json()

    def update_test(self, function_name, code):
        headers = {
            'Content-Type': 'application/javascript',
            **self.default_headers,
        }
        with httpx.Client() as client:
            if function_name not in code:
                raise Exception('Function name does not match in code')
            r = client.put(self.base_url + f"/{function_name}/test", content=code, headers=headers)
            return r.json()


class Webhooks(Integromat):
    def __init__(self, api_key, app_name):
        super().__init__(api_key)
        self.base_url = self.base_url + f"/app/{app_name}/webhook"

    def create(self, label, wh_type='web'):
        body = {
            "label": label,
            'type': wh_type
        }
        r = httpx.post(self.base_url, json=body, headers=self.default_headers)
        return r.json()

    def list(self):
        r = httpx.get(self.base_url, headers=self.default_headers)
        return r.json()

    def update_communications(self, webhook, body):
        r = httpx.put(self.base_url + f"/{webhook}/api", json=body, headers=self.default_headers)
        return r.json()

    def add_connection(self, webhook, connection_name):
        headers = {
            ** self.default_headers,
            "content-type": "text/plain"
        }
        r = httpx.put(self.base_url + f"/{webhook}/connection", content=connection_name, headers=headers)
        return r.json()

    def update_parameters(self, webhook, body):
        r = httpx.put(self.base_url + f"/{webhook}/parameters", json=body, headers=self.default_headers)
        return r.json()

    def update_attach(self, webhook, body):
        r = httpx.put(self.base_url + f"/{webhook}/attach", json=body, headers=self.default_headers)
        return r.json()

    def update_detach(self, webhook, body):
        r = httpx.put(self.base_url + f"/{webhook}/detach", json=body, headers=self.default_headers)
        return r.json()

    def update_scope(self, webhook, body):
        r = httpx.put(self.base_url + f"/{webhook}/scope", json=body, headers=self.default_headers)
        return r.json()


class General(Integromat):
    def __init__(self, api_key, app_name, app_version):
        super().__init__(api_key)
        self.base_url = self.base_url + f"/app/{app_name}/{app_version}"

    def update_base(self, body):
        r = httpx.put(self.base_url + "/base", json=body, headers=self.default_headers)
        return r.json()

    def update_common(self, body):
        r = httpx.put(self.base_url + "/common", json=body, headers=self.default_headers)
        return r.json()

    def update_readme(self, body):
        headers = {
            'Content-Type': 'text/markdown',
            **self.default_headers,
        }
        r = httpx.put(self.base_url + "/readme", content=body, headers=headers)
        return r.json()

    def update_groups(self, body):
        r = httpx.put(self.base_url + "/groups", json=body, headers=self.default_headers)
        return r.json()


class Connections(Integromat):
    def __init__(self, api_key, app_name):
        super().__init__(api_key)
        self.base_url = self.base_url + f"/app/{app_name}/connection"

    def create(self, label, wh_type='oauth-refresh'):
        body = {
            "label": label,
            'type': wh_type
        }
        r = httpx.post(self.base_url, json=body, headers=self.default_headers)
        return r.json()

    def list(self):
        r = httpx.get(self.base_url, headers=self.default_headers)
        return r.json()

    def update_communications(self, connection, body):
        r = httpx.put(self.base_url + f"/{connection}/api", json=body, headers=self.default_headers)
        return r.json()

    def update_common(self, connection, body):
        r = httpx.put(self.base_url + f"/{connection}/common", json=body, headers=self.default_headers)
        return r.json()

    def update_scopes(self, connection, body):
        r = httpx.put(self.base_url + f"/{connection}/scopes", json=body, headers=self.default_headers)
        return r.json()

    def update_default_scope(self, connection, body):
        r = httpx.put(self.base_url + f"/{connection}/scope", json=body, headers=self.default_headers)
        return r.json()

    def update_parameters(self, connection, body):
        r = httpx.put(self.base_url + f"/{connection}/parameters", json=body, headers=self.default_headers)
        return r.json()
