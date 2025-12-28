
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

LOGICAL_VERIFIER_AGENT = "You are a logical relation verifier. Evaluate statements of the form: “A is a hypernym of B”. Interpret hypernym as strict class subsumption: B ⊆ A. Return TRUE if the relation holds logically, otherwise return FALSE. Do not infer relations from causation, purpose, or context."