from starlette.applications import Starlette
from starlette.responses import PlainTextResponse,HTMLResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import Response
import uvicorn
from libs.stock_object.stock_obj import StockObj




async def app(scope, receive, send):
    assert scope['type'] == 'http'
    request = Request(scope, receive)
    content = '%s %s' % (request.method, request.url.path)
    response = Response(content, media_type='text/plain')
    await response(scope, receive, send)



def homepage(request):
    return HTMLResponse(
        """
        <h1 align="center">Stock Prediction Using Various DL Models </h1>

        <form align="center">
        <p>Please select your stock:</p>
          <input type="radio" id="FB" name="stock" value="FB">
          <label for="FB">FB</label><br>
          <input type="radio" id="WMT" name="stock" value="WMT">
          <label for="WMT">WMT</label><br>
          
        <br>  

        <p>Please select model:</p>
            <input type="radio" id="perceptron" name="model" value="perceptron">
            <label for="perceptron">perceptron</label><br>
            <input type="radio" id="simple_rnn" name="model" value="simple_rnn">
            <label for="simple_rnn">Simple RNN</label><br>
            
        <br>  

        <p>Please select time scale</p>
            <input type="radio" id="1m" name="time_scale" value="1m">
            <label for="1m">1m</label><br>
            <input type="radio" id="2m" name="time_scale" value="2m">
            <label for="2m">2m</label><br>
            <input type="radio" id="5m" name="time_scale" value="5m">
            <label for="5m">5m</label><br>
        
        <br>  
              
        
        <input type="submit" value="Submit">
        </form>

    """)

def user_me(request):
    username = "John Doe"
    return PlainTextResponse('Hello, %s!' % username)



def user(request):
    username = request.path_params['username']
    return PlainTextResponse('Hello, %s!' % username)

async def websocket_endpoint(websocket):
    await websocket.accept()
    await websocket.send_text('Hello, websocket!')
    await websocket.close()

def startup():
    print('Ready to go')

routes = [
    Route('/', homepage),
    Route('/user/me', user_me),
    Route('/user/{username}', user),
    WebSocketRoute('/ws', websocket_endpoint),
    Mount('/static', StaticFiles(directory="static")),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup])




if __name__ == "__main__":
    uvicorn.run("web_platform:app", host="127.0.0.1", port=8000, log_level="info")
