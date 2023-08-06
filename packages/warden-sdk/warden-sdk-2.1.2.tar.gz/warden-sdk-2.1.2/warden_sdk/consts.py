"""File containing all of the constants for the sdk.

  Typical usage example:

  from warden_sdk.consts import 
  bar = foo.FunctionBar()
  
Code reference:
- [sentry_sdk](https://github.com/getsentry/sentry-python/blob/master/sentry_sdk/consts.py)
"""

from typing import (Union, Tuple, Optional, List)

DEFAULT_QUEUE_SIZE = 100
DEFAULT_MAX_BREADCRUMBS = 100


class ClientConstructor(object):
   """Client Constructor is a base class for the default options allowed.
   """

   def __init__(
       self,
       integrations: list = [],  # type: Sequence[Integration]  # noqa: B006
       creds: Tuple[dict, str] = {
           'client_id': '',
           'client_secret': '',
       },  # type: str
       service: str = '',
       api: str = '',
       scopes: Union[list, str] = [],
       # flask: bool = True
       with_locals: bool=True, 
       max_breadcrumbs:int=DEFAULT_MAX_BREADCRUMBS,
       release:Optional[str]=None,  
       environment:Optional[str]=None, 
       server_name:Optional[str]=None,  
       shutdown_timeout:int=2,  
       in_app_include:List[str]=[], # noqa: B006
       in_app_exclude:List[str]=[], # noqa: B006
       default_integrations:bool=True,  
       dist:Optional[str]=None,
       transport=None,  # type: Optional[Union[sentry_sdk.transport.Transport, Type[sentry_sdk.transport.Transport], Callable[[Event], None]]]
       transport_queue_size:int=DEFAULT_QUEUE_SIZE,
       sample_rate:float=1.0,
       send_default_pii:bool=False,  
       http_proxy:Optional[str]=None,  
       https_proxy:Optional[str]=None,  
       ignore_errors: List[Union[type, str]]=[],  # noqa: B006
       request_bodies:str="medium", 
       before_send=None,  # type: Optional[EventProcessor]
       before_breadcrumb=None,  # type: Optional[BreadcrumbProcessor]
       debug:bool=False, 
       attach_stacktrace:bool=False,
       ca_certs:Optional[str]=None, 
       propagate_traces:bool=True, 
       traces_sample_rate:Optional[float]=None,  
       traces_sampler=None,  # type: Optional[TracesSampler]
       auto_enabling_integrations:bool=True, 
       auto_session_tracking:bool=True,
       _experiments={},  # type: Experiments  # noqa: B006
       user_fid:Optional[str]=None,
       user_scope:Optional[str]=None,  
       chatty:bool=True, 
   ):
      # type: (...) -> None
      pass


def __get_default_options():
   import inspect

   if hasattr(inspect, "getfullargspec"):
      getargspec = inspect.getfullargspec
   else:
      getargspec = inspect.getargspec  # type: ignore

   a = getargspec(ClientConstructor.__init__)
   defaults = a.defaults or ()
   return dict(zip(a.args[-len(defaults):], defaults))


DEFAULT_OPTIONS = __get_default_options()

def WARDEN_LOGGING_API_LINK(env=None):
    if env == None:
        raise Exception('Environment has not be set.')

    if env.lower() == 'development' or env.lower() == 'dev':
        return "https://dev-api.warden.ferant.io/log"
    elif env.lower() == 'production' or env.lower() == 'prod':
        return "https://api.warden.ferant.io/log"
    else:
        _env_types: List[str] = ['dev','development','prod','production']
        raise Exception(f'Environment type is not accepted. Use one of the following: \n {_env_types}')

VERSION = "2.1.2"
SDK_INFO = {
    "name": "warden.python",
    "version": VERSION,
    "packages": [{
        "name": "pypi:warden-sdk",
        "version": VERSION
    }],
}
