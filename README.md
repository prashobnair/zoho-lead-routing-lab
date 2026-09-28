# zoho-lead-routing-lab (moved)

This project moved to [zoho-implementation-toolkit](https://github.com/prashobnair/zoho-implementation-toolkit) as the `lead_routing` module. Its full commit history was preserved there.

It routes inbound leads to queues in simulation — qualified, duplicate-candidate, or human review. It never sends anything.

## Use it now

```sh
pip install https://github.com/prashobnair/zoho-implementation-toolkit/releases/download/v0.1.0/zohokit-0.1.0-py3-none-any.whl
```

or

```sh
uv tool install git+https://github.com/prashobnair/zoho-implementation-toolkit@v0.1.0
```

The old `python cli.py leads.json` is now:

```sh
zohokit lead-routing route leads.json [--default-region IN]
```

Note the hyphen: the command group is `lead-routing` while the module folder is `lead_routing`. Reports render with `--format json|table|markdown|html` and `--out`.

## Links

- Module guide: https://prashobnair.github.io/zoho-implementation-toolkit/modules/lead_routing/
- What changed versus this repo: https://prashobnair.github.io/zoho-implementation-toolkit/legacy-parity/
- Source: https://github.com/prashobnair/zoho-implementation-toolkit/tree/main/src/zohokit/modules/lead_routing

This repository is archived and read-only.
