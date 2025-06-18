from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import docker
import os
import uuid

app = FastAPI()
client = docker.from_env()

BASE_WORLD_DIR = "/minecraft/worlds"  # In container
HOST_WORLD_DIR = os.path.abspath("worlds")  # On host

os.makedirs(HOST_WORLD_DIR, exist_ok=True)

class ServerRequest(BaseModel):
    version: str = "LATEST"
    port: int = 25565
    world_name: str = "default"

@app.post("/start-server")
def start_server(request: ServerRequest):
    container_name = f"mc-server-{uuid.uuid4().hex[:6]}"
    host_world_path = os.path.join(HOST_WORLD_DIR, request.world_name)
    os.makedirs(host_world_path, exist_ok=True)

    try:
        container = client.containers.run(
            image="itzg/minecraft-server",
            name=container_name,
            detach=True,
            ports={f"{request.port}/tcp": request.port},
            volumes={
                host_world_path: {"bind": "/data", "mode": "rw"}
            },
            environment={
                "EULA": "TRUE",
                "VERSION": request.version
            }
        )
        return {
            "message": "Server started",
            "container_name": container_name,
            "docker_id": container.id[:12],
            "world": request.world_name,
            "join_address": f"localhost:{request.port}"
        }
    except docker.errors.APIError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Minecraft Server API is running!"}

@app.get("/list-servers")
def list_servers():
    containers = client.containers.list(filters={"ancestor": "itzg/minecraft-server"})
    return [{"name": c.name, "id": c.id[:12], "status": c.status} for c in containers]

@app.post("/stop-server/{container_name}")
def stop_server(container_name: str):
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        return {"message": f"{container_name} stopped and removed"}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail="Container not found")
