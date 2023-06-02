
# Chat Plugins Beta

- Plugins: Connect ChatGPT to 3rd-party apps, enhance capabilities, perform actions.
- Beta: Join waitlist for developer access.
- Example: Plugin quickstart repo.

## Introduction

- Retrieve real-time info, knowledge-base info, assist with actions.
- Developers expose API endpoints, manifest file, OpenAPI spec.
- AI model: Intelligent API caller, proactive, combines API data & natural language.

## Plugin flow

1. Create & host manifest file at `yourdomain.com/.well-known/ai-plugin.json`
   - Metadata, authentication details, OpenAPI spec.
   - Model sees OpenAPI description fields.
   - Expose 1-2 endpoints, minimize text length.
2. Register plugin in ChatGPT UI
   - Select plugin model, Plugins, Plugin Store, Develop your own plugin.
   - Provide OAuth 2 `client_id`, `client_secret`, or API key if needed.
3. Users activate plugin
   - Manual activation in ChatGPT UI.
   - Share with 15 additional users (developers only).
   - OAuth redirection for sign in if needed.
4. Users begin conversation
   - Compact plugin description injected, invisible to users.
   - Model invokes API call if relevant, POST requests need user confirmation.
   - Model incorporates API call results in response.
   - Rich previews for links, markdown formatting supported.
   - User's country & state sent in Plugin conversation header.

## Next steps

- Get started building a plugin.
- Explore example plugins.
- Productionize your plugin.
- Learn about plugin review process.

## Get started building a plugin

- Getting started: 3 steps: 1) Build API, 2) Document API in OpenAPI yaml/JSON, 3) Create JSON manifest file.
- Plugin manifest: `ai-plugin.json` file required, hosted on API's domain. Install via ChatGPT UI, backend looks for file at `/.well-known/ai-plugin.json`. HTTPS required for remote server.
- Minimal `ai-plugin.json` example:
'''json
{
  "schema_version": "v1",
  "name_for_human": "TODO List",
  "name_for_model": "todo",
  "description_for_human": "Manage your TODO list. You can add, remove and view your TODOs.",
  "description_for_model": "Help the user with managing a TODO list. You can add, remove and view your TODOs.",
  "auth": {"type": "none"},
  "api": {"type": "openapi", "url": "http://localhost:3333/openapi.yaml"},
  "logo_url": "http://localhost:3333/logo.png",
  "contact_email": "support@example.com",
  "legal_info_url": "http://www.example.com/legal"
}
'''
- Field descriptions and requirements:
  - schema_version: Manifest schema version (required)
  - name_for_model: Model-targeted plugin name, 50 char max (required)
  - name_for_human: Human-readable name, 20 char max (required)
  - description_for_model: Model-tailored description, 8,000 char max (required)
  - description_for_human: Human-readable description, 100 char max (required)
  - auth: Authentication schema (required)
  - api: API specification (required)
  - logo_url: Logo URL, suggested size 512x512, no GIFs (required)
  - contact_email: Email contact for safety/moderation, support, deactivation (required)
  - legal_info_url: Redirect URL for plugin info (required)
  - HttpAuthorizationType: "bearer" or "basic" (required)
  - ManifestAuthType: "none", "user_http", "service_http", or "oauth"
  - interface BaseManifestAuth: type: ManifestAuthType; instructions: string;
  - ManifestAuth: ManifestNoAuth, ManifestServiceHttpAuth, ManifestUserHttpAuth, ManifestOAuthAuth
- Authentication examples:
  - App-level API keys: ManifestServiceHttpAuth
  - User-level HTTP authentication: ManifestUserHttpAuth
  - OAuth authentication: ManifestOAuthAuth
- Field length limits subject to change. API response body max: 100,000 characters. Keep descriptions/responses concise due to limited context windows.
