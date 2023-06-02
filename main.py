from typing import Optional
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.staticfiles import StaticFiles
import os
import redis

redis_client = redis.StrictRedis(host="0.0.0.0", port=6379, db=0, decode_responses=True)

app = FastAPI()
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")

# Set the default working directory to /workspace
os.chdir("workspace")

# Route to list all TODOs


@app.get("/todos")
def list_todos():
    todos = {}
    for key in redis_client.keys():
        if key != "todo_id":
            todos[key] = "[" + key + "] " + str(redis_client.get(key))
    return todos


# Route to list a specific TODO


@app.get("/todos/{todo_id}")
def list_todo(todo_id: int):
    todo = redis_client.get(str(todo_id))
    if todo:
        return {"todo_id": todo_id, "todo": todo}
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


# Route to add a TODO


@app.post("/todos")
def add_todo(todo: str):
    # Generate a unique todo_id
    todo_id = redis_client.incr("todo_id")
    redis_client.set(str(todo_id), todo)
    return {"todo_id": todo_id, "todo": todo}


# Route to delete a TODO


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if not redis_client.exists(str(todo_id)):
        raise HTTPException(status_code=404, detail="Todo not found")
    redis_client.delete(str(todo_id))
    return {"result": "Todo deleted"}


# Route to set the current working directory


@app.post("/cwd")
def set_cwd(dir_path: str):
    os.chdir(dir_path)
    return {"result": "CWD changed"}


# Route to get the current working directory


@app.get("/cwd")
def get_cwd():
    return {"cwd": os.getcwd()}


# Route to get list of files and directories in the current directory


@app.get("/directories")
def get_current_directory_contents():
    return {"contents": os.listdir()}


# Route to get list of files and directories in a specific directory


@app.get("/directories/{dir_path}")
def get_directory_contents(dir_path: str):
    if not os.path.isdir(dir_path):
        raise HTTPException(status_code=404, detail="Directory not found")
    return {"contents": os.listdir(dir_path)}


# Route to create a directory


@app.post("/directories/{dir_path}")
def create_directory(dir_path: str):
    os.makedirs(dir_path, exist_ok=True)
    return {"result": "Directory created"}


# Route to delete a directory


@app.delete("/directories/{dir_path}")
def delete_directory(dir_path: str):
    if not os.path.isdir(dir_path):
        raise HTTPException(status_code=404, detail="Directory not found")
    os.rmdir(dir_path)
    return {"result": "Directory deleted"}


# Route to rename a directory


@app.put("/directories/{dir_path}")
def rename_directory(dir_path: str, new_dir_path: str):
    if not os.path.isdir(dir_path):
        raise HTTPException(status_code=404, detail="Directory not found")
    os.rename(dir_path, new_dir_path)
    return {"result": "Directory renamed"}


# Route to create a file


@app.post("/files/{file_path}")
def create_file(
    file_path: str,
    file: Optional[UploadFile] = None,
    file_content: Optional[str] = None,
):
    if file:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
    elif file_content:
        with open(file_path, "w") as buffer:
            buffer.write(file_content)
    else:
        with open(file_path, "w") as buffer:
            buffer.write("")
    return {"result": "File created"}


# Route to read a file


@app.get("/files/{file_path}")
def read_file(file_path: str):
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(file_path, "r") as file:
        return {"result": file.read()}


# Route to update a file


@app.put("/files/{file_path}")
def update_file(file_path: str, file: UploadFile):
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return {"result": "File updated"}


# Route to delete a file


@app.delete("/files/{file_path}")
def delete_file(file_path: str):
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    os.remove(file_path)
    return {"result": "File deleted"}


# Route to rename a file


@app.put("/files/{file_path}")
def rename_file(file_path: str, new_file_path: str):
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    os.rename(file_path, new_file_path)
    return {"result": "File renamed"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
