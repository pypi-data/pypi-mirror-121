import json
import os

import click
from pathlib import Path
from integromat_wrapper.integromat import General, Apps, Webhooks, Connections, Functions, Modules, MTYPE_ACTION, \
    MTYPE_SEARCH, MTYPE_TRIGGER, MTYPE_INSTANT, MTYPE_RESPONDER, MTYPE_UNIVERSAL, RPCs


def publish_file(path, api_key, name, version, section, sectiontype,
                 object_name, object_type, object_label, object_connection, object_webhook):
    if not path.exists():
        click.echo(f'      Skipping: File does not exist {section} - {sectiontype} - {path.absolute()}', color=True)
        return
    click.echo(f'      {section} - {sectiontype} - {path.absolute()}')
    with open(path) as f:
        # General
        if section == 'general':
            _cls = General(api_key, name, version)
            if sectiontype == 'base':
                data = json.load(f)
                r = _cls.update_base(data)
                if r != {}:
                    click.echo(f"            Failed to upload {r}")
            if sectiontype == 'common':
                data = json.load(f)
                r = _cls.update_common(data)
                if r != {}:
                    click.echo(f"            Failed to upload {r}")

        # Webhooks
        if section == 'webhooks':
            _cls = Webhooks(api_key, name)
            found_webhooks = _cls.list()
            r = {"name": name}
            if not any([x.get('label') == object_label for x in found_webhooks]):
                r = _cls.create(object_label)
                _cls.add_connection(r.get('name'), object_connection)

            # Do actions
            if sectiontype == "communication":
                r = _cls.update_communications(r.get('name'), json.load(f))
                if r != {}:
                    click.echo(f"            Failed to upload {r}")
            if sectiontype == "attach":
                r = _cls.update_attach(r.get('name'), json.load(f))
                if r != {}:
                    click.echo(f"            Failed to upload {r}")
            if sectiontype == "detach":
                r = _cls.update_detach(r.get('name'), json.load(f))
                if r != {}:
                    click.echo(f"            Failed to upload {r}")
            if sectiontype == "parameters":
                r = _cls.update_parameters(r.get('name'), json.load(f))
                if r != {}:
                    click.echo(f"            Failed to upload {r}")
            if sectiontype == "scope":
                r = _cls.update_scope(r.get('name'), json.load(f))
                if r != {}:
                    click.echo(f"            Failed to upload {r}")

        # Connections
        if section == "connections":
            _cls = Connections(api_key, name)
            found_conns = _cls.list()
            if not any([x.get('label') == object_label for x in found_conns]):
                _cls.create(object_label, wh_type='apikey')

            # Do actions
            if sectiontype == "communication":
                r = _cls.update_communications(name, json.load(f))
                if r != {}:
                    click.echo(f"            Failed to upload {r}")
            if sectiontype == "common":
                r = _cls.update_common(name, json.load(f))
                if r != {}:
                    click.echo(f"            Failed to upload {r}")
            if sectiontype == "scope":
                r = _cls.update_scopes(name, json.load(f))
                if r != {}:
                    click.echo(f"            Failed to upload {r}")
            if sectiontype == "scopes":
                r = _cls.update_default_scope(name, json.load(f))
                if r != {}:
                    click.echo(f"            Failed to upload {r}")
            if sectiontype == "parameters":
                r = _cls.update_parameters(name, json.load(f))
                if r != {}:
                    click.echo(f"            Failed to upload {r}")

        # Functions
        if section == "functions":
            _cls = Functions(api_key, name, version)
            found_functions = _cls.list()
            if not any([x.get('label') == object_name for x in found_functions]):
                _cls.create(object_name)

            # Do actions
            if sectiontype == "function":
                r = _cls.update_code(object_name, f.read())
                if r != {}:
                    click.echo(f"            Failed to upload {r}")

        # Modules
        if section == "modules":
            _cls = Modules(api_key, name, version)
            found_functions = _cls.list()
            if not any([x.get('label') == object_name for x in found_functions]):
                uses_connection = True
                uses_webhook = False
                if object_type == 'action':
                    _type_id = MTYPE_ACTION
                if object_type == 'search':
                    _type_id = MTYPE_SEARCH
                if object_type == 'trigger':
                    _type_id = MTYPE_TRIGGER
                if object_type == 'instant':
                    uses_connection = False
                    uses_webhook = True
                    _type_id = MTYPE_INSTANT
                if object_type == 'responder':
                    _type_id = MTYPE_RESPONDER
                if object_type == 'universal':
                    _type_id = MTYPE_UNIVERSAL
                r = _cls.create(object_name, object_label, '', type_id=_type_id)
                if uses_connection:
                    _cls.add_connection(r.get('name'), object_connection)
                if uses_webhook:
                    _cls.add_webhook(r.get('name'), object_webhook)

                # Do actions
                if sectiontype == "communication":
                    r = _cls.update_communications(object_name, json.load(f))
                    if r != {}:
                        click.echo(f"            Failed to upload {r}")
                if sectiontype == "parameters":
                    r = _cls.update_parameters(object_name, json.load(f))
                    if r != {}:
                        click.echo(f"            Failed to upload {r}")
                if sectiontype == "mappable":
                    r = _cls.update_mappable_parameters(object_name, json.load(f))
                    if r != {}:
                        click.echo(f"            Failed to upload {r}")
                if sectiontype == "interface":
                    r = _cls.update_interface(object_name, json.load(f))
                    if r != {}:
                        click.echo(f"            Failed to upload {r}")
                if sectiontype == "samples":
                    r = _cls.update_samples(object_name, json.load(f))
                    if r != {}:
                        click.echo(f"            Failed to upload {r}")
                if sectiontype == "scope":
                    r = _cls.update_scope(object_name, json.load(f))
                    if r != {}:
                        click.echo(f"            Failed to upload {r}")

        # Rpcs
        if section == "rpcs":
            _cls = RPCs(api_key, name, version)
            found_rpcs = _cls.list()
            if not any([x.get('label') == object_name for x in found_rpcs]):
                r = _cls.create(object_name, object_label)
                _cls.add_connection(r.get('name'), object_connection)

            # Do actions
            if sectiontype == "communication":
                r = _cls.update_communications(object_name, json.load(f))
                if r != {}:
                    click.echo(f"            Failed to upload {r}")
            if sectiontype == "parameters":
                r = _cls.update_parameters(object_name, json.load(f))
                if r != {}:
                    click.echo(f"            Failed to upload {r}")


@click.command()
@click.option('--path', default=None, help='path to project')
@click.option('--api_key', default=None, help='set api key for publishing')
@click.argument('app_name')
def deploy(path, api_key, app_name: str):
    if not path:
        path = '.'
    path = Path(path)

    api_key = os.getenv('INTEGROMAT_APIKEY', api_key)

    click.echo(f'Starting deploy: {path.absolute()}')

    # Check if app exists. Create if it does not.
    imt_apps = Apps(api_key)
    found_apps = imt_apps.list_apps()
    if not any([x.get('label') == app_name for x in found_apps]):
        r = imt_apps.create_app(app_name.lower().replace(' ', ''), app_name)
        name = r.get('name')
        version = r.get('version')
    else:
        name = [x for x in found_apps if x.get('label') == app_name][0].get('name')
        version = [x for x in found_apps if x.get('label') == app_name][0].get('version')

    def _pf(fp, s, st, on=None, ot=None, ol=None, oc=None, ow=None):
        publish_file(path / fp, api_key, name, version, s, st, on, ot, ol, oc, ow)

    # handle general configs
    _pf("base.imljson", 'general', 'base')
    _pf("common.imljson", 'general', 'common')
    _pf("readme.imljson", 'general', 'readme')

    # handle connections
    connection_map = {}
    if (path / "connections").exists():
        for p in (path / "connections").iterdir():
            if p.is_dir():
                click.echo(f"Deploying connections: {p.name}")
                manifest = p / "manifest.json"
                if not manifest.exists():
                    break
                with open(manifest) as _m:
                    _manifest = json.loads(_m.read())
                    _on = _manifest.get('name', p.name)
                    _ol = _manifest.get('label', p.name)
                connection_map[_on] = _ol
                _pf(f"connections/{p.name}/api.imljson", "connections", "communication", _on, None, _ol)
                _pf(f"connections/{p.name}/common.imljson", "connections", "common", _on, None, _ol)
                _pf(f"connections/{p.name}/scopes.imljson", "connections", "scopes", _on, None, _ol)
                _pf(f"connections/{p.name}/scope.imljson", "connections", "scope", _on, None, _ol)
                _pf(f"connections/{p.name}/parameters.imljson", "connections", "parameters", _on, None, _ol)

    # get connections
    _cls = Connections(api_key, name)
    connections = _cls.list()

    # handle webhooks
    webhooks_map = {}
    if (path / "webhooks").exists():
        for p in (path / "webhooks").iterdir():
            if p.is_dir():
                click.echo(f"Deploying webhooks: {p.name}")
                _on = p.name
                manifest = p / "manifest.json"
                if not manifest.exists():
                    break
                with open(manifest) as _m:
                    _manifest = json.loads(_m.read())
                    _on = _manifest.get('name', p.name)
                    _ol = _manifest.get('label', p.name)
                    webhooks_map[_on] = _ol
                _oc = next((x for x in connections
                            if x.get('label') == connection_map[_manifest.get('connection')]), None).get('name')
                _pf(f"webhooks/{p.name}/api.imljson", "webhooks", "communication", _on, None, _ol, _oc)
                _pf(f"webhooks/{p.name}/attach.imljson", "webhooks", "attach", _on, None, _ol, _oc)
                _pf(f"webhooks/{p.name}/detach.imljson", "webhooks", "detach", _on, None, _ol, _oc)
                _pf(f"webhooks/{p.name}/parameters.imljson", "webhooks", "parameters", _on, None, _ol, _oc)
                _pf(f"webhooks/{p.name}/scope.imljson", "webhooks", "scope", _on, None, _ol, _oc)

    # get connections
    _cls = Webhooks(api_key, name)
    webhooks = _cls.list()

    # handle functions
    if (path / "function").exists():
        for p in (path / "function").iterdir():
            if p.is_dir():
                click.echo(f"Deploying functions: {p.name}")
                _on = p.name
                _pf(f"function/{_on}/code.js", "functions", "function", _on)

    # handle modules
    if (path / "module").exists():
        for p in (path / "module").iterdir():
            if p.is_dir():
                click.echo(f"Deploying modules: {p.name}")
                _on = p.name
                manifest = p / "manifest.json"
                if not manifest.exists():
                    break
                with open(manifest) as _m:
                    _manifest = json.loads(_m.read())
                    _on = _manifest.get('name', p.name)
                    _ol = _manifest.get('label', p.name)
                    _ot = _manifest.get('type')
                _oc = next((x for x in connections
                            if x.get('label') == connection_map.get(_manifest.get('connection'))), {}).get('name')
                _ow = next((x for x in webhooks if x.get('label') == webhooks_map.get(_manifest.get('webhook'))),
                           {}).get('name')
                _pf(f"module/{_on}/api.imljson", "modules", "communication", _on, _ot, _ol, _oc, _ow)
                _pf(f"module/{_on}/parameters.imljson", "modules", "parameters", _on, _ot, _ol, _oc, _ow)
                _pf(f"module/{_on}/expect.imljson", "modules", "mappable", _on, _ot, _ol, _oc, _ow)
                _pf(f"module/{_on}/interface.imljson", "modules", "interface", _on, _ot, _ol, _oc, _ow)
                _pf(f"module/{_on}/samples.imljson", "modules", "samples", _on, _ot, _ol, _oc, _ow)

    # handle rpcs
    if (path / "rpc").exists():
        for p in (path / "rpc").iterdir():
            if p.is_dir():
                click.echo(f"Deploying RPCs: {p.name}")
                _on = p.name
                manifest = p / "manifest.json"
                if not manifest.exists():
                    break
                with open(manifest) as _m:
                    _manifest = json.loads(_m.read())
                    _on = _manifest.get('name', p.name)
                    _ol = _manifest.get('label', p.name)
                _oc = next((x for x in connections
                            if x.get('label') == connection_map[_manifest.get('connection')]), None).get('name')
                _pf(f"rpc/{_on}/api.imljson", "rpcs", "communication", _on, None, _ol, _oc)
                _pf(f"rpc/{_on}/parameters.imljson", "rpcs", "parameters", _on, None, _ol, _oc)


if __name__ == '__main__':
    deploy()
