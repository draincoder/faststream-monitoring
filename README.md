<div align="center">

# FastStream Monitoring Example

[![python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Test](https://github.com/draincoder/pyproject/actions/workflows/ci.yaml/badge.svg)](https://github.com/draincoder/pyproject/actions/workflows/ci.yaml)

</div>

## Example of monitoring settings for FastStream

The example consists of three services and demonstrates support for distributed tracing.

1. Start application
```shell
just up
```
2. Open **Grafana** on `http://127.0.0.1:3000` with login `admin` and password `admin`
3. Go to **Explore** - **Tempo**
4. Enter TraceQL query `{}`

![Trace example](https://imgur.com/EziQgpy.png)
