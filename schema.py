MOVIE_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
      "movieId": {"type": "integer"},
      "ntop": {"type": "integer"}
    },
    "required": ["movieId"]
}