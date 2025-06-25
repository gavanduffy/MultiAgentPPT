import logging
from fastapi import FastAPI, APIRouter, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from server import ConversationServer
from dotenv import load_dotenv

load_dotenv()

logfile = "api.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(module)s - %(funcName)s - %(message)s",
    handlers=[
        logging.FileHandler(logfile, mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
app = FastAPI()

# Enable CORS for frontend React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_request_body(request: Request, call_next):
    if request.method == "POST":
        body = await request.body()
        logging.info(f"Request to {request.url.path} with body: {body.decode('utf-8')}")
    else:
        logging.info(f"Request to {request.url.path}")
    response = await call_next(request)
    return response
router = APIRouter()
agent_server = ConversationServer(router)

# 添加 ping 路由
@app.api_route("/ping", methods=["GET", "POST"])
async def ping():
    return "Pong"
app.include_router(router)

# 启动服务
if __name__ == "__main__":
    import uvicorn
    print(f"启动A2A的多Agent协调者后端服务，端口为13000")
    uvicorn.run(app, host="0.0.0.0", port=13000)
