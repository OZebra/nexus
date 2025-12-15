
MODEL_RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
      "name": "boolean_question_response",
      "schema": {
        "type": "object",
        "properties": {
          "answer": {
            "type": "string",
            "description": "Either 'True' or 'False' as a direct evaluation of the given statement. 'True' if you find that the statement is truthful and 'False' otherwise.",
            "enum": [
              "True",
              "False"
            ]
          },
        },
        "required": [
          "answer",
        ],
        "additionalProperties": False
      },
    "strict": True
  }
}