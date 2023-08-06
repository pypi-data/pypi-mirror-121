from k8kat.res.svc.kat_svc import KatSvc
from werkzeug.utils import cached_property

from kama_sdk.model.supplier.base.supplier import Supplier
from kama_prom_plugin.models.prom_client import prom_client
from kama_prom_plugin.models.prom_data_supplier import PromDataSupplier


class PromStateSupplier(Supplier):

  @cached_property
  def is_online(self):
    return PromDataSupplier({}).do_ping()

  @cached_property
  def svc(self) -> KatSvc:
    return prom_client.find_prom_svc()

  @cached_property
  def is_in_cluster(self):
    return prom_client.is_prom_server_in_cluster()

  @cached_property
  def status(self):
    return "online" if self.is_online else "offline"

  @cached_property
  def action_preview_str(self):
    if self.is_in_cluster:
      return "http://localhost"
    else:
      return prom_client.get_prom_ext_url()

  @cached_property
  def action_spec(self):
    if self.is_in_cluster:
      return dict(
        type='port_forward',
        uri=dict(
          pod_port=self.svc.first_tcp_port_num(),
          pod_name=self.svc.name,
          namespace=self.svc.namespace,
        )
      )
    else:
      return dict(
        type='www',
        uri=prom_client.get_prom_ext_url()
      )
