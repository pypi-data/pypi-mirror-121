<a href="https://jgltechnologies.com/discord">
<img src="https://discord.com/api/guilds/844418702430175272/embed.png">
</a>

# aiohttp-ratelimiter

aiohttp-ratelimiter is a high performance rate limiter for the aiohttp.web framework.


Install from git
```
python -m pip install git+https://github.com/Nebulizer1213/aiohttp-ratelimiter
```

Install from pypi
```
python -m pip install aiohttp-ratelimiter
```

<br>


Example

```python
from aiohttp import web
from aiohttplimiter import default_keyfunc, Limiter

app = web.Application()
routes = web.RouteTableDef()

limiter = Limiter(keyfunc=default_keyfunc)

@routes.get("/")
# This endpoint can only be requested 1 time per second per IP address
@limiter.limit("1/1")
async def home(request):
    return web.Response(text="test")

app.add_routes(routes)
web.run_app(app)
```

<br>

You can exempt an IP from ratelimiting using the exempt_ips kwarg.

```python
from aiohttplimiter import Limiter, default_keyfunc
from aiohttp import web

app = web.Application()
routes = web.RouteTableDef()

# 192.168.1.245 is exempt from ratelimiting.
# Keep in mind that exempt_ips takes a set not a list.
limiter = Limiter(keyfunc=default_keyfunc, exempt_ips={"192.168.1.245"})

@routes.get("/")
@limiter.limit("1/1")
async def test(request):
    return web.Response(text="test")

app.add_routes(routes)
web.run_app(app)
```

<br>

You can limit how much memory aiohttp-ratelimiter can use to store ratelimiting info with the max_memory kwargs.
This kwarg limits the max amount of gigabytes aiohttp-ratelimiter can use to store ratelimiting info. The default is None, which means aiohttp-ratelimiter can use as much as it can before throwing a MemoryError.

```python
from aiohttp import web
from aiohttplimiter import default_keyfunc, Limiter

app = web.Application()
routes = web.RouteTableDef()

# aiohttp-ratelimiter can only store 0.5 gigabytes of ratelimiting data.
# When the limit is reached the data resets.
# Please note that the number is not exact. It might be a little over 0.5.
limiter = Limiter(keyfunc=default_keyfunc, max_memory=.5)

@routes.get("/")
@limiter.limit("1/1")
def home(request):
    return web.Response(text="test")

app.add_routes(routes)
web.run_app(app)
```

<br>

If you have any middlewares, just specify the amount in the middleware_count kwarg.

```python
limiter = Limiter(keyfunc=default_keyfunc, exempt_ips={"192.168.1.235"}, middleware_count=1)
```




