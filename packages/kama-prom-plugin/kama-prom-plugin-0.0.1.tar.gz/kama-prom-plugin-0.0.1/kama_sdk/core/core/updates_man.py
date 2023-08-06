from datetime import datetime
from typing import Dict, List, Optional

from kama_sdk.core.core import hub_api_client, consts
from kama_sdk.utils import utils, env_utils
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core import config_man as cman_mod
from kama_sdk.core.core.types import ReleaseDict, InjectionsDesc, K8sResDict, KteaDict
from kama_sdk.utils.utils import deep_merge
from kama_sdk.core.ktea.ktea_provider import ktea_client
from kama_sdk.model.base import pure_provider_ids
from kama_sdk.model.supplier.base.supplier import Supplier


def is_using_latest_injection() -> bool:
  bundle = latest_injection_bundle()
  return bundle is None


def fetch_next_update() -> Optional[ReleaseDict]:
  config_man.write_last_update_checked(str(datetime.now()))
  return None


def latest_injection_bundle() -> Optional[InjectionsDesc]:
  if config_man.is_real_deployment():
    resp = hub_api_client.get('/injectors/compile')
    if resp.ok:
      return resp.json()['data']
    else:
      print(f"[kama_sdk::updates_man] err requesting injection {resp.status_code}")
      return None
  else:
    provider_id = pure_provider_ids.mock_injection_bundle_id
    model = Supplier.inflate(provider_id)
    return model.resolve() if model else None


def fetch_update(release_id: str, space=None) -> Optional[ReleaseDict]:
  if config_man.is_real_deployment():
    space = space or consts.APP_SPACE_ID
    resp = hub_api_client.get(f'/releases/{release_id}', space=space)
    if resp.ok:
      return dict(**resp.json()['bundle'], space=space)
    else:
      print(f"[kama_sdk::updates_man] err requesting update {resp.status_code}")
  else:
    model = Supplier.inflate(release_id)
    return model.resolve() if model else None


def next_available() -> Optional[ReleaseDict]:
  if config_man.is_real_deployment():
    resp = hub_api_client.get(f'/releases/available')
    data = resp.json() if resp.status_code < 205 else None
    return data['bundle'] if data else None
  else:
    provider_id = pure_provider_ids.mock_app_release_id
    model = Supplier.inflate(provider_id)
    return model.resolve() if model else None


def fetch_all(spaces: List[str]) -> List[ReleaseDict]:
  release_dicts: List[ReleaseDict] = []
  if config_man.is_real_deployment():
    for space in spaces:
      selector = {cman_mod.SPACE_KW: space}
      resp = hub_api_client.get(f'/releases', **selector)
      if resp.status_code < 205:
        tx = lambda b: {**b, 'space': space}
        bundles: List[ReleaseDict] = resp.json().get('data')
        release_dicts.extend(list(map(tx, bundles)))
    return release_dicts
  else:
    query = {"labels.supplies": "mock-release"}
    suppliers = Supplier.inflate_all(q=query)
    return [s.resolve() for s in suppliers]


def _gen_injection_telem(keys: List[str]):
  all_vars = config_man.get_user_vars()
  return {k: all_vars[k] for k in keys}


def preview_injection(injection: InjectionsDesc) -> Dict:
  old_defaults = config_man.get_publisher_inj_vars()
  # old_manifest = ktea_client().template_manifest_std()

  # kt = Supplier.inflate("sdk.supplier.injections_ktea")

  new_defaults = deep_merge(old_defaults, injection['standard'])

  # new_resources = []
  # if len(injection['inline']) > 0 and kt:
  #   new_resources = ktea_client(ktea=kt).dry_run(
  #     values=injection['inline'],
  #   )
  #
  # new_manifest = [r for r in old_manifest]
  #
  # def find_twin(res: K8sResDict) -> Optional[int]:
  #   for (i, _res) in enumerate(new_manifest):
  #     if utils.are_res_same(res, _res):
  #       return i
  #   return None
  #
  # for new_res in new_resources:
  #   old_version_ind = find_twin(new_res)
  #   if old_version_ind:
  #     old_version = new_manifest[old_version_ind]
  #     new_manifest[old_version_ind] = deep_merge(old_version, new_res)
  #   else:
  #     new_manifest.append(new_res)

  return dict(
    defaults=dict(
      old=old_defaults,
      new=new_defaults
    ),
    # manifest=dict(
    #   old=old_manifest,
    #   new=new_manifest
    # )
  )


def preview(release_dict: ReleaseDict, space: str) -> Dict:
  config_man.invalidate_cmap()

  old_def_vars = config_man.get_default_vars(space=space)
  old_manifest = ktea_client(space=space).template_manifest_std()

  new_ktea_dict = updated_release_ktea(release_dict)
  new_ktea_client = ktea_client(ktea=new_ktea_dict)

  new_def_lvl_vars = new_ktea_client.load_default_values()

  new_manifest_vars = deep_merge(
    new_def_lvl_vars,
    config_man.get_publisher_inj_vars(space=space),
    config_man.get_user_vars(space=space)
  )
  new_manifest = new_ktea_client.template_manifest(new_manifest_vars)

  return dict(
    diff=dict(
      defaults=dict(
        old=old_def_vars,
        new=new_def_lvl_vars
      ),
      templated_manifest=dict(
        old=old_manifest,
        new=new_manifest
      )
    )
  )


def commit_new_ktea(update_dict: ReleaseDict):
  new_ktea = updated_release_ktea(update_dict)
  config_man.patch_ktea(new_ktea)


def commit_new_defaults_from_update(update_dict: ReleaseDict):
  new_ktea = updated_release_ktea(update_dict)
  new_defaults = ktea_client(ktea=new_ktea).load_default_values()
  config_man.write_default_vars(new_defaults)


def updated_release_ktea(release: ReleaseDict) -> KteaDict:
  new_ktea = KteaDict(version=release['version'])
  old_ktea = config_man.get_ktea_config()
  old_type = old_ktea.get('type')

  if new_type := release.get('ktea_type'):
    new_ktea['type'] = new_type

  if new_uri := release.get('ktea_uri'):
    new_ktea['uri'] = new_uri

  if new_type and not new_type == old_type:
    msg = f"change from {old_ktea.get('type')} -> {new_type}"
    print(f"[kama_sdk:updates_man] WARN update ktea type {msg}")

  return {**old_ktea, **new_ktea}
