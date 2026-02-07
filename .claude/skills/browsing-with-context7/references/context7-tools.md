# Context7 MCP Server Tools

*2 tools available*

## `resolve-library-id`

Resolve a package/product name to a Context7-compatible library ID and returns matching libraries.

### Parameters

- **`libraryName`** (`string`) *(required)*: Library name to search for and retrieve a Context7-compatible library ID.
- **`query`** (`string`) *(required)*: The user's original question or task. This is used to rank library results by relevance to what the user is trying to accomplish.

<details>
<summary>Full Schema</summary>

```json
{
  "type": "object",
  "properties": {
    "libraryName": {
      "type": "string",
      "description": "Library name to search for and retrieve a Context7-compatible library ID."
    },
    "query": {
      "type": "string",
      "description": "The user's original question or task. This is used to rank library results by relevance to what the user is trying to accomplish. IMPORTANT: Do not include any sensitive or confidential information such as API keys, passwords, credentials, or personal data in your query."
    }
  },
  "required": [
    "query",
    "libraryName"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```
</details>

## `query-docs`

Retrieves and queries up-to-date documentation and code examples from Context7 for any programming library or framework.

### Parameters

- **`libraryId`** (`string`) *(required)*: Exact Context7-compatible library ID (e.g., '/mongodb/docs', '/vercel/next.js', '/supabase/supabase', '/vercel/next.js/v14.3.0-canary.87') retrieved from 'resolve-library-id' or directly from user query in the format '/org/project' or '/org/project/version'.
- **`query`** (`string`) *(required)*: The question or task you need help with. Be specific and include relevant details.

<details>
<summary>Full Schema</summary>

```json
{
  "type": "object",
  "properties": {
    "libraryId": {
      "type": "string",
      "description": "Exact Context7-compatible library ID (e.g., '/mongodb/docs', '/vercel/next.js', '/supabase/supabase', '/vercel/next.js/v14.3.0-canary.87') retrieved from 'resolve-library-id' or directly from user query in the format '/org/project' or '/org/project/version'."
    },
    "query": {
      "type": "string",
      "description": "The question or task you need help with. Be specific and include relevant details. Good: 'How to set up authentication with JWT in Express.js' or 'React useEffect cleanup function examples'. Bad: 'auth' or 'hooks'. IMPORTANT: Do not include any sensitive or confidential information such as API keys, passwords, credentials, or personal data in your query."
    }
  },
  "required": [
    "libraryId",
    "query"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```
</details>