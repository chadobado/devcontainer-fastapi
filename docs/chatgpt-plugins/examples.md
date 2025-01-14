# Example plugins
To get started building, we are making available a set of simple plugins that cover different authentication schemas and use cases. From our simple no authentication todo list plugin to the more powerful retrieval plugin, these examples provide a glimpse into what we hope to make possible with plugins.

During development, you can run the plugin locally on your computer or through a cloud development environment like GitHub Codespaces, Replit, or CodeSandbox.

## Plugin quickstart

We created the plugin quickstart as a starting place for developers to get a plugin up and running in less than 5 minutes. If you have not run a plugin yet and want to get acquainted with the minimal steps required to run one, consider beginning with the plugin quickstart repo.

## Learn how to build a simple todo list plugin with no auth

To start, check out the no authentication page, then define an ai-plugin.json file with the following fields:

```json
{
    "schema_version": "v1",
    "name_for_human": "TODO List (No Auth)",
    "name_for_model": "todo",
    "description_for_human": "Manage your TODO list. You can add, remove and view your TODOs.",
    "description_for_model": "Plugin for managing a TODO list, you can add, remove and view your TODOs.",
    "auth": {
        "type": "none"
    },
    "api": {
        "type": "openapi",
        "url": "PLUGIN_HOSTNAME/openapi.yaml"
    },
    "logo_url": "PLUGIN_HOSTNAME/logo.png",
    "contact_email": "support@example.com",
    "legal_info_url": "https://example.com/legal"
}
```

Note the PLUGIN_HOSTNAME should be the actual hostname of your plugin server.

Next, we can define the API endpoints to create, delete, and fetch todo list items for a specific user.

```python
import json

import quart
import quart_cors
from quart import request

# Note: Setting CORS to allow chat.openapi.com is only required when running a localhost plugin
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

_TODOS = {}


@app.post("/todos/<string:username>")
async def add_todo(username):
    request = await quart.request.get_json(force=True)
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(request["todo"])
    return quart.Response(response='OK', status=200)


@app.get("/todos/<string:username>")
async def get_todos(username):
    return quart.Response(response=json.dumps(_TODOS.get(username, [])), status=200)


@app.delete("/todos/<string:username>")
async def delete_todo(username):
    request = await quart.request.get_json(force=True)
    todo_idx = request["todo_idx"]
    if 0 <= todo_idx < len(_TODOS[username]):
        _TODOS[username].pop(todo_idx)
    return quart.Response(response='OK', status=200)


@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("ai-plugin.json") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the manifest
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the OpenAPI spec
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/yaml")


def main():
    app.run(debug=True, host="0.0.0.0", port=5002)


if __name__ == "__main__":
    main()
```

Last, we need to set up and define a OpenAPI specification to match the endpoints defined on our local or remote server. You do not need to expose the full functionality of your API via the specification and can instead choose to let ChatGPT have access to only certain functionality.

There are also many tools that will automatically turn your server definition code into an OpenAPI specification so you don’t need to do it manually. In the case of the Python code above, the OpenAPI specification will look like:

```yaml
openapi: 3.0.1
info:
    title: TODO Plugin
    description: A plugin that allows the user to create and manage a TODO list using ChatGPT. If you do not know the user's username, ask them first before making queries to the plugin. Otherwise, use the username "global".
    version: "v1"
servers:
    - url: PLUGIN_HOSTNAME
paths:
    /todos/{username}:
        get:
            operationId: getTodos
            summary: Get the list of todos
            parameters:
                - in: path
                  name: username
                  schema:
                      type: string
                  required: true
                  description: The name of the user.
            responses:
                "200":
                    description: OK
                    content:
                        application/json:
                            schema:
                                $ref: "#/components/schemas/getTodosResponse"
        post:
            operationId: addTodo
            summary: Add a todo to the list
            parameters:
                - in: path
                  name: username
                  schema:
                      type: string
                  required: true
                  description: The name of the user.
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/addTodoRequest"
            responses:
                "200":
                    description: OK
        delete:
            operationId: deleteTodo
            summary: Delete a todo from the list
            parameters:
                - in: path
                  name: username
                  schema:
                      type: string
                  required: true
                  description: The name of the user.
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/deleteTodoRequest"
            responses:
                "200":
                    description: OK

components:
    schemas:
        getTodosResponse:
            type: object
            properties:
                todos:
                    type: array
                    items:
                        type: string
                    description: The list of todos.
        addTodoRequest:
            type: object
            required:
                - todo
            properties:
                todo:
                    type: string
                    description: The todo to add to the list.
                    required: true
        deleteTodoRequest:
            type: object
            required:
                - todo_idx
            properties:
                todo_idx:
                    type: integer
                    description: The index of the todo to delete.
                    required: true
```

## Learn how to build a simple todo list plugin with service level auth

To start, check out the service level authentication page and then define an ai-plugin.json file with the following fields:

```json
{
    "schema_version": "v1",
    "name_for_human": "TODO List (service auth)",
    "name_for_model": "todo",
    "description_for_human": "Manage your TODO list. You can add, remove and view your TODOs.",
    "description_for_model": "Plugin for managing a TODO list, you can add, remove and view your TODOs.",
    "auth": {
        "type": "service_http",
        "authorization_type": "bearer",
        "verification_tokens": {
            "openai": "Replace_this_string_with_the_verification_token_generated_in_the_ChatGPT_UI"
        }
    },
    "api": {
        "type": "openapi",
        "url": "https://example.com/openapi.yaml"
    },
    "logo_url": "https://example.com/logo.png",
    "contact_email": "support@example.com",
    "legal_info_url": "https://example.com/legal"
}
```

Notice that the verification token is required for service level authentication plugins. The token is generated during the plugin installation process in the ChatGPT web UI after you set the service access token.

You will also need to update "Example.com" to the name of your remote server.

Next, we can define the API endpoints to create, delete, and fetch todo list items for a specific user. The endpoints also check that the user is authenticated.

```python
import json

import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__))

# This key can be anything, though you will likely want a randomly generated sequence.
_SERVICE_AUTH_KEY = "REPLACE_ME"
_TODOS = {}

def assert_auth_header(req):
    assert req.headers.get(
        "Authorization", None) == f"Bearer {_SERVICE_AUTH_KEY}"

@app.post("/todos/<string:username>")
async def add_todo(username):
    assert_auth_header(quart.request)
    request = await quart.request.get_json(force=True)
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(request["todo"])
    return quart.Response(response='OK', status=200)

@app.get("/todos/<string:username>")
async def get_todos(username):
    assert_auth_header(quart.request)
    return quart.Response(response=json.dumps(_TODOS.get(username, [])), status=200)

@app.delete("/todos/<string:username>")
async def delete_todo(username):
    assert_auth_header(quart.request)
    request = await quart.request.get_json(force=True)
    todo_idx = request["todo_idx"]
    if 0 <= todo_idx < len(_TODOS[username]):
        _TODOS[username].pop(todo_idx)
    return quart.Response(response='OK', status=200)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5002)

if __name__ == "__main__":
    main()
```

Last, we need to set up and define a OpenAPI specification to match the endpoints defined on our remote server. In general, the OpenAPI specification would look the same regardless of the authentication method. Using an automatic OpenAPI generator will reduce the chance of errors when creating your OpenAPI specification.

```yaml
openapi: 3.0.1
info:
    title: TODO Plugin
    description: A plugin that allows the user to create and manage a TODO list using ChatGPT. If you do not know the user's username, ask them first before making queries to the plugin. Otherwise, use the username "global".
    version: "v1"
servers:
    - url: https://example.com
paths:
    /todos/{username}:
        get:
            operationId: getTodos
            summary: Get the list of todos
            parameters:
                - in: path
                  name: username
                  schema:
                      type: string
                  required: true
                  description: The name of the user.
            responses:
                "200":
                    description: OK
                    content:
                        application/json:
                            schema:
                                $ref: "#/components/schemas/getTodosResponse"
        post:
            operationId: addTodo
            summary: Add a todo to the list
            parameters:
                - in: path
                  name: username
                  schema:
                      type: string
                  required: true
                  description: The name of the user.
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/addTodoRequest"
            responses:
                "200":
                    description: OK
        delete:
            operationId: deleteTodo
            summary: Delete a todo from the list
            parameters:
                - in: path
                  name: username
                  schema:
                      type: string
                  required: true
                  description: The name of the user.
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/deleteTodoRequest"
            responses:
                "200":
                    description: OK

components:
    schemas:
        getTodosResponse:
            type: object
            properties:
                todos:
                    type: array
                    items:
                        type: string
                    description: The list of todos.
        addTodoRequest:
            type: object
            required:
                - todo
            properties:
                todo:
                    type: string
                    description: The todo to add to the list.
                    required: true
        deleteTodoRequest:
            type: object
            required:
                - todo_idx
            properties:
                todo_idx:
                    type: integer
                    description: The index of the todo to delete.
                    required: true
```

## Learn how to build a simple sports stats plugin

This plugin is an example of a simple sports stats API. Please keep in mind our domain policy and usage policies when considering what to build.

To start, define an ai-plugin.json file with the following fields:

```json
{
    "schema_version": "v1",
    "name_for_human": "Sport Stats",
    "name_for_model": "sportStats",
    "description_for_human": "Get current and historical stats for sport players and games.",
    "description_for_model": "Get current and historical stats for sport players and games. Always display results using markdown tables.",
    "auth": {
        "type": "none"
    },
    "api": {
        "type": "openapi",
        "url": "PLUGIN_HOSTNAME/openapi.yaml"
    },
    "logo_url": "PLUGIN_HOSTNAME/logo.png",
    "contact_email": "support@example.com",
    "legal_info_url": "https://example.com/legal"
}
```
Note the PLUGIN_HOSTNAME should be the actual hostname of your plugin server.

Next, we define a mock API for a simple sports service plugin.

```python
import json
import requests
import urllib.parse

import quart
import quart_cors
from quart import request

# Note: Setting CORS to allow chat.openapi.com is only required when running a localhost plugin
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")
HOST_URL = "https://example.com"

@app.get("/players")
async def get_players():
    query = request.args.get("query")
    res = requests.get(
        f"{HOST_URL}/api/v1/players?search={query}&page=0&per_page=100")
    body = res.json()
    return quart.Response(response=json.dumps(body), status=200)


@app.get("/teams")
async def get_teams():
    res = requests.get(
        "{HOST_URL}/api/v1/teams?page=0&per_page=100")
    body = res.json()
    return quart.Response(response=json.dumps(body), status=200)


@app.get("/games")
async def get_games():
    query_params = [("page", "0")]
    limit = request.args.get("limit")
    query_params.append(("per_page", limit or "100"))
    start_date = request.args.get("start_date")
    if start_date:
        query_params.append(("start_date", start_date))
    end_date = request.args.get("end_date")

    if end_date:
        query_params.append(("end_date", end_date))
    seasons = request.args.getlist("seasons")

    for season in seasons:
        query_params.append(("seasons[]", str(season)))
    team_ids = request.args.getlist("team_ids")

    for team_id in team_ids:
        query_params.append(("team_ids[]", str(team_id)))

    res = requests.get(
        f"{HOST_URL}/api/v1/games?{urllib.parse.urlencode(query_params)}")
    body = res.json()
    return quart.Response(response=json.dumps(body), status=200)


@app.get("/stats")
async def get_stats():
    query_params = [("page", "0")]
    limit = request.args.get("limit")
    query_params.append(("per_page", limit or "100"))
    start_date = request.args.get("start_date")
    if start_date:
        query_params.append(("start_date", start_date))
    end_date = request.args.get("end_date")

    if end_date:
        query_params.append(("end_date", end_date))
    player_ids = request.args.getlist("player_ids")

    for player_id in player_ids:
        query_params.append(("player_ids[]", str(player_id)))
    game_ids = request.args.getlist("game_ids")

    for game_id in game_ids:
        query_params.append(("game_ids[]", str(game_id)))
    res = requests.get(
        f"{HOST_URL}/api/v1/stats?{urllib.parse.urlencode(query_params)}")
    body = res.json()
    return quart.Response(response=json.dumps(body), status=200)


@app.get("/season_averages")
async def get_season_averages():
    query_params = []
    season = request.args.get("season")
    if season:
        query_params.append(("season", str(season)))
    player_ids = request.args.getlist("player_ids")

    for player_id in player_ids:
        query_params.append(("player_ids[]", str(player_id)))
    res = requests.get(
        f"{HOST_URL}/api/v1/season_averages?{urllib.parse.urlencode(query_params)}")
    body = res.json()
    return quart.Response(response=json.dumps(body), status=200)


@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("ai-plugin.json") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the manifest
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the OpenAPI spec
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/yaml")


def main():
    app.run(debug=True, host="0.0.0.0", port=5001)


if __name__ == "__main__":
    main()
```

Last, we define our OpenAPI specification:

```yaml
openapi: 3.0.1
info:
    title: Sport Stats
    description: Get current and historical stats for sport players and games.
    version: "v1"
servers:
    - url: PLUGIN_HOSTNAME
paths:
    /players:
        get:
            operationId: getPlayers
            summary: Retrieves all players from all seasons whose names match the query string.
            parameters:
                - in: query
                  name: query
                  schema:
                      type: string
                  description: Used to filter players based on their name. For example, ?query=davis will return players that have 'davis' in their first or last name.
            responses:
                "200":
                    description: OK
    /teams:
        get:
            operationId: getTeams
            summary: Retrieves all teams for the current season.
            responses:
                "200":
                    description: OK
    /games:
        get:
            operationId: getGames
            summary: Retrieves all games that match the filters specified by the args. Display results using markdown tables.
            parameters:
                - in: query
                  name: limit
                  schema:
                      type: string
                  description: The max number of results to return.
                - in: query
                  name: seasons
                  schema:
                      type: array
                      items:
                          type: string
                  description: Filter by seasons. Seasons are represented by the year they began. For example, 2018 represents season 2018-2019.
                - in: query
                  name: team_ids
                  schema:
                      type: array
                      items:
                          type: string
                  description: Filter by team ids. Team ids can be determined using the getTeams function.
                - in: query
                  name: start_date
                  schema:
                      type: string
                  description: A single date in 'YYYY-MM-DD' format. This is used to select games that occur on or after this date.
                - in: query
                  name: end_date
                  schema:
                      type: string
                  description: A single date in 'YYYY-MM-DD' format. This is used to select games that occur on or before this date.
            responses:
                "200":
                    description: OK
    /stats:
        get:
            operationId: getStats
            summary: Retrieves stats that match the filters specified by the args. Display results using markdown tables.
            parameters:
                - in: query
                  name: limit
                  schema:
                      type: string
                  description: The max number of results to return.
                - in: query
                  name: player_ids
                  schema:
                      type: array
                      items:
                          type: string
                  description: Filter by player ids. Player ids can be determined using the getPlayers function.
                - in: query
                  name: game_ids
                  schema:
                      type: array
                      items:
                          type: string
                  description: Filter by game ids. Game ids can be determined using the getGames function.
                - in: query
                  name: start_date
                  schema:
                      type: string
                  description: A single date in 'YYYY-MM-DD' format. This is used to select games that occur on or after this date.
                - in: query
                  name: end_date
                  schema:
                      type: string
                  description: A single date in 'YYYY-MM-DD' format. This is used to select games that occur on or before this date.
            responses:
                "200":
                    description: OK
    /season_averages:
        get:
            operationId: getSeasonAverages
            summary: Retrieves regular season averages for the given players. Display results using markdown tables.
            parameters:
                - in: query
                  name: season
                  schema:
                      type: string
                  description: Defaults to the current season. A season is represented by the year it began. For example, 2018 represents season 2018-2019.
                - in: query
                  name: player_ids
                  schema:
                      type: array
                      items:
                          type: string
                  description: Filter by player ids. Player ids can be determined using the getPlayers function.
            responses:
                "200":
                    description: OK
```

## Learn how to build a simple OAuth todo list plugin

To create an OAuth plugin, we start by defining a ai-plugin.json file with the auth type set to oauth:

```json
{
    "schema_version": "v1",
    "name_for_human": "TODO List (OAuth)",
    "name_for_model": "todo_oauth",
    "description_for_human": "Manage your TODO list. You can add, remove and view your TODOs.",
    "description_for_model": "Plugin for managing a TODO list, you can add, remove and view your TODOs.",
    "auth": {
        "type": "oauth",
        "client_url": "PLUGIN_HOSTNAME/oauth",
        "scope": "",
        "authorization_url": "PLUGIN_HOSTNAME/auth/oauth_exchange",
        "authorization_content_type": "application/json",
        "verification_tokens": {
            "openai": "Replace_this_string_with_the_verification_token_generated_in_the_ChatGPT_UI"
        }
    },
    "api": {
        "type": "openapi",
        "url": "PLUGIN_HOSTNAME/openapi.yaml"
    },
    "logo_url": "PLUGIN_HOSTNAME/logo.png",
    "contact_email": "contact@example.com",
    "legal_info_url": "http://www.example.com/legal"
}
```

Next, we need to define our OAuth service. This OAuth example is not intended for production use cases but rather to highlight what a simple OAuth flow will look like so developers can get experience building towards a production solution.

```python
import json

import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="*")

_TODOS = {}

@app.post("/todos/<string:username>")
async def add_todo(username):
    request = await quart.request.get_json(force=True)
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(request["todo"])
    return quart.Response(response='OK', status=200)

@app.get("/todos/<string:username>")
async def get_todos(username):
    print(request.headers)
    return quart.Response(response=json.dumps(_TODOS.get(username, [])), status=200)

@app.delete("/todos/<string:username>")
async def delete_todo(username):
    request = await quart.request.get_json(force=True)
    todo_idx = request["todo_idx"]
    # fail silently, it's a simple plugin
    if 0 <= todo_idx < len(_TODOS[username]):
        _TODOS[username].pop(todo_idx)
    return quart.Response(response='OK', status=200)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("manifest.json") as f:
        text = f.read()
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/yaml")

@app.get("/oauth")
async def oauth():
    query_string = request.query_string.decode('utf-8')
    parts = query_string.split('&')
    kvps = {}
    for part in parts:
        k, v = part.split('=')
        v = v.replace("%2F", "/").replace("%3A", ":")
        kvps[k] = v
    print("OAuth key value pairs from the ChatGPT Request: ", kvps)
    url = kvps["redirect_uri"] + f"?code={OPENAI_CODE}"
    print("URL: ", url)
    return quart.Response(
        f'<a href="{url}">Click to authorize</a>'
    )

# Sample names
OPENAI_CLIENT_ID = "id"
OPENAI_CLIENT_SECRET = "secret"
OPENAI_CODE = "abc123"
OPENAI_TOKEN = "def456"

@app.post("/auth/oauth_exchange")
async def oauth_exchange():
    request = await quart.request.get_json(force=True)
    print(f"oauth_exchange {request=}")

    if request["client_id"] != OPENAI_CLIENT_ID:
        raise RuntimeError("bad client ID")
    if request["client_secret"] != OPENAI_CLIENT_SECRET:
        raise RuntimeError("bad client secret")
    if request["code"] != OPENAI_CODE:
        raise RuntimeError("bad code")

    return {
        "access_token": OPENAI_TOKEN,
        "token_type": "bearer"
    }

def main():
    app.run(debug=True, host="0.0.0.0", port=5002)

if __name__ == "__main__":
    main()
```

Last, like with our other examples, we define a simple OpenAPI file based on the endpoints:

```yaml
openapi: 3.0.1
info:
    title: TODO Plugin
    description: A plugin that allows the user to create and manage a TODO list using ChatGPT. If you do not know the user's username, ask them first before making queries to the plugin. Otherwise, use the username "global".
    version: "v1"
servers:
    - url: PLUGIN_HOSTNAME
paths:
    /todos/{username}:
        get:
            operationId: getTodos
            summary: Get the list of todos
            parameters:
                - in: path
                  name: username
                  schema:
                      type: string
                  required: true
                  description: The name of the user.
            responses:
                "200":
                    description: OK
                    content:
                        application/json:
                            schema:
                                $ref: "#/components/schemas/getTodosResponse"
        post:
            operationId: addTodo
            summary: Add a todo to the list
            parameters:
                - in: path
                  name: username
                  schema:
                      type: string
                  required: true
                  description: The name of the user.
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/addTodoRequest"
            responses:
                "200":
                    description: OK
        delete:
            operationId: deleteTodo
            summary: Delete a todo from the list
            parameters:
                - in: path
                  name: username
                  schema:
                      type: string
                  required: true
                  description: The name of the user.
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/deleteTodoRequest"
            responses:
                "200":
                    description: OK

components:
    schemas:
        getTodosResponse:
            type: object
            properties:
                todos:
                    type: array
                    items:
                        type: string
                    description: The list of todos.
        addTodoRequest:
            type: object
            required:
                - todo
            properties:
                todo:
                    type: string
                    description: The todo to add to the list.
                    required: true
        deleteTodoRequest:
            type: object
            required:
                - todo_idx
            properties:
                todo_idx:
                    type: integer
                    description: The index of the todo to delete.
                    required: true
```