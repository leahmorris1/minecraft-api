README - Minecraft Server API

🚀 Features

    - Start a new Minecraft server (via Docker)

    - Stop and remove a server

    - List active/previous Minecraft containers

    - View logs for a given server

    - Interactive Swagger UI

📦 Prerequisites

    - Python 3.8+

    - Docker installed and running

    - pip install fastapi uvicorn docker

🔧 Run the API
    ```
    uvicorn main:app --reload
    docker run -d -p 8000:8000 --name minecraft-api-server -v /var/run/docker.sock:/var/run/docker.sock minecraft-api
    ```
    - Visit 'http://localhost:8000/docs' to explore Swagger UI and test endpoints

🎮 How to Connect in Minecraft

Once the server is running:
    - Open Minecraft Java Edition

    - Click on Multiplayer

    - Click Add Server

    - Enter:

        - Server Name: anything you like

        - Server Address: localhost:<port> (e.g., localhost:25565)

    - Join!

⚠️ If you're not on the same machine (e.g., connecting from another device), replace localhost with the host's IP address.


📘 Example Requests
    - POST /start-server
    ```
    {
        "version": "1.20.4",
        "port": 25565,
        "world_name": "customworld"
    }
    ```
    - POST 
        /stop-server/mc-server-abc123
        Stop and remove a server container.

    - GET 
        /list-servers
        Returns running and stopped Minecraft containers.

    - GET 
        /logs/mc-server-abc123
        Get full logs from the specified container.