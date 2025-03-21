from pathlib import Path

import snappi
from dotenv import dotenv_values

from .k8s import svc_ext_ip_and_ports


def otg_api(k8s_svc: str, port_name, transport):
    env = dotenv_values()
    ip, ports = svc_ext_ip_and_ports(
        k8s_svc,
        env.get("K8S_NAMESPACE"),
    )
    otg_api: snappi.Api = snappi.api(
        location=f"https://{ip}:{ports.get(port_name)}",
        transport=transport,
        verify=False,
    )
    return otg_api


def otg_http_api(k8s_svc: str):
    return otg_api(k8s_svc, "https", snappi.Transport.HTTP)


def otg_grpc_api(k8s_svc: str):
    return otg_api(k8s_svc, "grpc", snappi.Transport.GRPC)


def configure_otg(api: snappi.Api, filepath: Path):
    config: snappi.Config = api.config()
    with open(filepath) as f:
        payload = config.deserialize(f.read())
    api.set_config(payload)


def unconfigure_otg(api: snappi.Api):
    config: snappi.Config = api.config()
    payload = config.deserialize("{}")
    api.set_config(payload)


def otg_transmit_stopped(otg_http_api: snappi.Api, flow_names: list):
    mreq = otg_http_api.metrics_request()
    mreq.flow.flow_names = flow_names
    mres: snappi.MetricsResponse = otg_http_api.get_metrics(mreq)
    miter: snappi.FlowMetricIter = mres.flow_metrics[0]
    print("FLOW METRICS", miter, sep="\n")
    return miter.transmit == miter.STOPPED
