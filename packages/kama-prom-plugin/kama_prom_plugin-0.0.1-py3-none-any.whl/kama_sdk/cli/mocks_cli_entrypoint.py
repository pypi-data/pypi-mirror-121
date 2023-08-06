import json
from argparse import ArgumentParser
from typing import Dict, List

from k8kat.auth.kube_broker import broker
from k8kat.res.config_map.kat_map import KatMap
from k8kat.res.ns.kat_ns import KatNs
from kubernetes.client import V1Namespace, V1ObjectMeta, V1ConfigMap

from kama_sdk.core.core import config_man
from kama_sdk.core.core.consts import KAMAFILE, APP_SPACE_ID, KTEA_TYPE_SERVER

from kama_sdk.core.core.types import KteaDict, KamaDict
from kama_sdk.utils import utils, logging
from kama_sdk.utils.logging import lerr


def get_meta() -> Dict:
  return {'name': 'mock-install', 'info': 'Mock an installation'}


def run(options: Dict):
  namespace = options.get(NAMESPACE_FLAG)
  overrides_raw: List[str] = options.get(SET_FLAG) or []

  force = options.get(FORCE_FLAG, False)
  port = options.get(PORT_FLAG, 5000)

  config = compile_config(overrides_raw, port)
  create_ns_if_missing(namespace)
  if delete_cmap_if_exists(namespace, force):
    create_mocked_cmap(namespace, config)
    config_man.coerce_ns(namespace)
    logging.lwin(f"created configmap/{KAMAFILE} in namespace {namespace}")
  else:
    lerr("ConfigMap already exists, use --force to overwrite", sig="kama_sdk")


def compile_config(overrides_raw: List[str], port) -> Dict:
  overrides_fdicts = list(map(str_assign_2_flat, overrides_raw))
  overrides_dict = utils.deep_merge_flats(overrides_fdicts)

  default_config = gen_default_config(port)

  final_dict = utils.deep_merge(default_config, overrides_dict)
  return format_bundle(final_dict)


def delete_cmap_if_exists(namespace: str, force: bool) -> bool:
  if cmap := KatMap.find(KAMAFILE, namespace):
    if force:
      cmap.delete(wait_until_gone=True)
    else:
      return False
  return True


def format_bundle(bundle: Dict) -> Dict:
  new_bundle = {}
  for key, value in bundle.items():
    serialized_value = config_man.type_serialize_entry(key, value)
    new_bundle[key] = serialized_value
  return new_bundle


def str_assign_2_flat(str_assign: str) -> Dict:
  deep_key, value = str_assign.split("=")
  return {deep_key: value}


def register_arg_parser(parser: ArgumentParser):
  parser.add_argument(
    NAMESPACE_FLAG,
    help="Namespace/release name"
  )

  parser.add_argument(
    f"--{SET_FLAG}",
    action='append',
    help=f"Assignment into configmap/{KAMAFILE}"
  )

  parser.add_argument(
    f"--{FORCE_FLAG}",
    action="store_true",
    help=f"Delete namespace if it already exists"
  )

  parser.add_argument(
    f"--{PORT_FLAG}",
    help=f"KAMA prototype server port, defaults to 5000"
  )


def create_ns_if_missing(name: str):
  if existing := KatNs.find(name):
    existing.label(True, managed_by='nmachine')
    return existing.reload()
  else:
    return broker.coreV1.create_namespace(
      body=V1Namespace(
        metadata=V1ObjectMeta(
          name=name,
          labels={'managed_by': 'nmachine'}
        )
      )
    )


def create_mocked_cmap(namespace: str, app_config: Dict):
  broker.coreV1.create_namespaced_config_map(
    namespace,
    body=V1ConfigMap(
      metadata=V1ObjectMeta(
        name=KAMAFILE,
        namespace=namespace,
        labels={
          'managed_by': 'nmachine'
        }
      ),
      data={
        APP_SPACE_ID: json.dumps(app_config)
      }
    )
  )


def gen_default_config(port_num: int) -> Dict:
  return {
    config_man.INSTALL_ID_KEY: '',
    config_man.IS_PROTOTYPE_KEY: True,
    config_man.STATUS_KEY: 'running',

    config_man.KTEA_CONFIG_KEY: KteaDict(
      type=KTEA_TYPE_SERVER,
      uri="https://api.nmachine.io/ktea/nmachine/ice-kream-ktea",
      version='1.0.1'
    ),
    config_man.KAMA_CONFIG_KEY: KamaDict(
      type=KTEA_TYPE_SERVER,
      uri=f"http://localhost:{port_num}",
      version="latest"
    ),

    config_man.USER_VARS_LVL: {},
    config_man.USER_INJ_VARS_LVL: {},
    config_man.DEF_VARS_LVL: {},
  }


NAMESPACE_FLAG = "namespace"
SET_FLAG = "set"
FORCE_FLAG = "force"
PORT_FLAG = "port"
