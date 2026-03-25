# coding: utf-8
"""Generic async HTTP request helper (no site-specific headers injected here)."""
import httpx
import urllib3.exceptions

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def async_request(method, url, proxy=None, **kwargs):
    """
    Thin async HTTP client wrapper.

    Header injection (Cookie, User-Agent, Referer) is done by callers that
    have access to site-specific configuration; this helper stays generic.
    """
    from doujinshi_dl import constant

    headers = kwargs.pop('headers', {})

    if proxy is None:
        proxy = constant.CONFIG.get('proxy', '')

    if isinstance(proxy, str) and not proxy:
        proxy = None

    # Remove 'timeout' from kwargs to avoid duplicate keyword argument since
    # httpx.AsyncClient accepts it as a constructor arg or request arg.
    timeout = kwargs.pop('timeout', 30)

    async with httpx.AsyncClient(headers=headers, verify=False, proxy=proxy,
                                 timeout=timeout) as client:
        response = await client.request(method, url, **kwargs)

    return response
