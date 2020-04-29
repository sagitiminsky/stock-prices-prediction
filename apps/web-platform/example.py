from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def homepage(request):
    return JSONResponse({'web-platform'})


app = Starlette(debug=True, routes=[
    Route('/', homepage),
])