<div align="center">

# [FastStream](https://github.com/airtai/faststream) Monitoring Example

[![python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Test](https://github.com/draincoder/pyproject/actions/workflows/ci.yaml/badge.svg)](https://github.com/draincoder/pyproject/actions/workflows/ci.yaml)

</div>

## Example of monitoring settings for FastStream

[FastStream OpenTelemetry documentation](https://faststream.ag2.ai/latest/getting-started/observability/opentelemetry/)\
[FastStream Prometheus documentation](https://faststream.ag2.ai/latest/getting-started/observability/prometheus/)

* Three [**FastStream**](https://github.com/ag2ai/faststream) services
* Exporting traces to **Grafana Tempo** via **gRPC**
* Visualization of traces via **Grafana**
* Collecting metrics and exporting using **Prometheus**
* [**Grafana dashboard**](https://grafana.com/grafana/dashboards/22130-faststream-metrics/) for metrics
* Examples with custom spans
* Configured **docker-compose** with the entire infrastructure

## How to run the example

1. Clone project
```shell
git clone https://github.com/draincoder/faststream-monitoring.git
```
2. Start application
```shell
docker compose --profile exchange --profile grafana up --build -d
```
3. Open **Grafana** on `http://127.0.0.1:3000` with login `admin` and password `admin`
4. Go to **Explore** - **Tempo**
5. Enter TraceQL query `{}`
6. Go to **Dashboards** - **FastStream Metrics**

![Trace example](https://imgur.com/EziQgpy.png)
![Metrics example](https://imgur.com/J0aGEFB.png)
