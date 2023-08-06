import os
import sys
import json
import math
import datetime
import email.utils
import traceback as _traceback
from dateutil.tz import tzoffset, tzlocal
import http.client
from http.cookies import SimpleCookie
from cgi import FieldStorage
from omnitools import dt2yyyymmddhhmmss, ApacheHeadersDict, str2html


_SERVER = dict(os.environ)
for k in _SERVER.keys():
    if k.startswith("REDIRECT_"):
        _SERVER[k.replace("REDIRECT_", "")] = _SERVER[k]
arguments = FieldStorage(environ=os.environ)
arguments = {k: [_.value for _ in arguments[k]] if isinstance(arguments[k], list) else arguments[k].value for k in arguments}
_GET = arguments
_POST = arguments
_SESSION = SimpleCookie()
_COOKIE = {k: v.value for k, v in SimpleCookie(_SERVER["HTTP_COOKIE"]).items()} if "HTTP_COOKIE" in _SERVER else {}
# need to vet it manually as it depends on the system
_HEADERS = ApacheHeadersDict({k: v for k, v in _SERVER.items() if k not in [
    "DOCUMENT_ROOT",
    "LANG",
    "CONTEXT_DOCUMENT_ROOT",
    "SERVER_SIGNATURE",
    "SERVER_SOFTWARE",
    "SERVER_PORT",
    "REMOTE_PORT",
    "SCRIPT_NAME",
    "SERVER_ADMIN",
    "LANGUAGE",
    "QUERY_STRING",
    "REDIRECT_QUERY_STRING",
    "GATEWAY_INTERFACE",
    "REQUEST_URI",
    "SERVER_PROTOCOL",
    "PYTHONIOENCODING",
    "SERVER_ADDR",
    "LC_ALL",
    "SCRIPT_FILENAME",
    "PATH",
    "CONTEXT_PREFIX",
]})
default_content_type = {
    "Content-Type": "text/html; charset=utf-8"
}
__response = {
    "status_code": 200,
    "headers": {},
    "content": b"",
    "cache": b""
}
__response["headers"].update(default_content_type)
__methods = {}
PRINTED = {
    "STATUS": False,
    "HEADERS": False,
}


def obj_to_bytes(obj):
    if isinstance(obj, str):
        obj = obj.encode()
    elif not isinstance(obj, bytes):
        try:
            obj = str2html(json.dumps(obj, indent=2))
        except:
            obj = str2html(str(obj))
        obj = obj.encode()
    return obj


def log(obj, fp: str = None):
    obj = obj_to_bytes(obj)
    now = dt2yyyymmddhhmmss().encode()
    open(fp or "log.log", "ab").write(now+b" "+obj+b"\n")


def log_construct(fp: str = None):
    def _log(obj):
        return log(obj, fp)

    return _log


def set_status(code: int):
    if not PRINTED["STATUS"]:
        __response["status_code"] = code
    else:
        raise Exception("status_code printed: {}, {}".format(
            PRINTED["STATUS"],
            __response["status_code"])
        )


def set_header(k, v):
    __response["headers"][k] = v


def flush():
    _generate_headers()
    _print(__response["content"])
    __response["content"] = b""
    sys.stdout.buffer.flush()


def _print(obj):
    sys.stdout.buffer.write(obj_to_bytes(obj))


def print(obj = "", end=b"\n"):
    obj = obj_to_bytes(obj)
    __response["content"] += obj
    __response["cache"] += obj
    if end:
        end = obj_to_bytes(end)
        __response["content"] += end
        __response["cache"] += end


def traceback(tag_name: str = "code", class_name: str = "traceback", style: str = "", limit=None, chain=True):
    return "<{tag} class='{}' style='{}'>{}</{tag}>".format(
        class_name,
        style,
        str2html(_traceback.format_exc(limit, chain)),
        tag=tag_name
    )


def _generate_headers():
    if not PRINTED["STATUS"]:
        _print("{}: {}\n".format("Status", __response["status_code"]))
        PRINTED["STATUS"] = True
    if not PRINTED["HEADERS"]:
        for k, v in __response["headers"].items():
            _print("{}: {}\n".format(k, v))
        session = _SESSION.output()
        if session:
            session += "\n"
        _print(session)
        _print("\n")
        PRINTED["HEADERS"] = True


def _generate_response():
    _generate_headers()
    content = __response.pop("content")
    _print(content)
    status_code = __response.pop("status_code")
    if not content and status_code >= 500 and status_code <= 599:
        if status_code in http.client.responses:
            msg = http.client.responses[status_code]
            status_message = "<h1>{} {}</h1><br/><p>{}</p>".format(status_code, msg, "The server has no response regarding this error.")
            _print(status_message)


def _should_return_304(fp: str = None):
    if not fp or not os.path.isfile(fp):
        return False
    lastmodified = math.floor(os.path.getmtime(fp))
    lastmodified2 = datetime.datetime.fromtimestamp(lastmodified, tz=tzoffset(None, 0))
    set_header("Last-Modified", lastmodified2.strftime('%a, %d %b %Y %H:%M:%S GMT'))
    if "If-Modified-Since" in _HEADERS:
        ims = email.utils.parsedate(_HEADERS["If-Modified-Since"])[:6]
        if ims:
            ims = datetime.datetime(*ims).timestamp()
            ims += tzlocal().utcoffset(datetime.datetime.now(tzlocal())).total_seconds()
            if ims >= lastmodified:
                return True
    return False


def should_return_304(*args, **kwargs):
    def _304():
        return _should_return_304(*args, **kwargs)

    return _304


def _max_age(age: int = 0):
    return "max-age={}".format(age)


def _cache_control():
    set_header("Cache-Control", _max_age() + ", must-revalidate")


def _should_read_from_cache_file():
    last_modiied = 999
    if_modified_since = 123
    if if_modified_since >= last_modiied:
        # cache = pickle.loads(open(_SERVER["SCRIPT_NAME"]+"cache", "rb").read())
        # set_status(cache["status_code"])
        # for k, v in cache["headers"]:
        #    set_header(k, v)
        # print(cache["cache"], end="")
        return True
    else:
        return False


def _write_to_cache_file(cache):
    # cache.pop("response")
    # open(_SERVER["SCRIPT_NAME"]+"cache", "wb").write(pickle.dumps(cache))
    return


def execute(
        method: str = "get", cacheable: bool = False,
        cache_ctrl = _cache_control,
        cache_norm = should_return_304(),
        cache_strat = _should_read_from_cache_file,
        cache_store = _write_to_cache_file,
        enable_tb: bool = True, traceback_kwargs: dict = None
    ):
    def wrapper(method_main):
        limit = None
        chain = True
        try:
            limit = traceback_kwargs["limit"]
        except:
            pass
        try:
            chain = traceback_kwargs["chain"]
        except:
            pass
        def _execute():
            try:
                if cacheable:
                    cache_ctrl()
                if cacheable and cache_norm():
                    set_status(304)
                elif not cacheable or (cacheable and not cache_strat()):
                    method_main()
                    if cacheable and __response["status_code"] == 200:
                        cache_store(__response)
            except:
                log(_traceback.format_exc(limit, chain))
                __response.pop("cache")
                __response["headers"].update(default_content_type)
                if enable_tb:
                    tb = traceback(**(traceback_kwargs or {}))
                else:
                    tb = "<h1>500 Internal Server Error</h1><br/><p>HTML stack trace is disabled.<br/>Check traceback log.</p>"
                __response["content"] = tb.encode()
                try:
                    set_status(500)
                except:
                    log(_traceback.format_exc())
            try:
                _generate_response()
            except:
                log(_traceback.format_exc())
                try:
                    set_status(500)
                except:
                    log(_traceback.format_exc())

        __methods[method] = _execute
        return _execute

    return wrapper


def main():
    method = _SERVER["REQUEST_METHOD"].lower()
    if method in __methods:
        __methods[method]()
    else:
        set_status(405)

