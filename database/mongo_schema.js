// ---------------------------------------------------
// Database: text_ai_db
// ---------------------------------------------------
db = db.getSiblingDB("text_ai_db");

// ---------------------------------------------------
// Collection: summaries
// ---------------------------------------------------
db.createCollection("summaries", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["input_text", "summary", "created_at"],
      properties: {
        input_text: {
          bsonType: "string",
          description: "Original input text"
        },
        summary: {
          bsonType: "string",
          description: "Generated summary"
        },
        input_length: {
          bsonType: "int"
        },
        summary_length: {
          bsonType: "int"
        },
        created_at: {
          bsonType: "date"
        }
      }
    }
  }
});


// ---------------------------------------------------
// Collection: plagiarism_checks
// ---------------------------------------------------
db.createCollection("plagiarism_checks", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["input_text", "overall_similarity", "created_at"],
      properties: {
        input_text: {
          bsonType: "string"
        },
        comparison_texts: {
          bsonType: "array",
          items: {
            bsonType: "string"
          }
        },
        overall_similarity: {
          bsonType: "double"
        },
        matches: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["compared_text", "similarity_score"],
            properties: {
              compared_text: {
                bsonType: "string"
              },
              similarity_score: {
                bsonType: "double"
              }
            }
          }
        },
        created_at: {
          bsonType: "date"
        }
      }
    }
  }
});


// ---------------------------------------------------
// Collection: autocorrections
// ---------------------------------------------------
db.createCollection("autocorrections", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["input_text", "corrected_text", "created_at"],
      properties: {
        input_text: {
          bsonType: "string"
        },
        corrected_text: {
          bsonType: "string"
        },
        corrections: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["original", "corrected"],
            properties: {
              original: {
                bsonType: "string"
              },
              corrected: {
                bsonType: "string"
              },
              message: {
                bsonType: "string"
              }
            }
          }
        },
        created_at: {
          bsonType: "date"
        }
      }
    }
  }
});


// ---------------------------------------------------
// Collection: users (Optional - future auth)
// ---------------------------------------------------
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "created_at"],
      properties: {
        email: {
          bsonType: "string"
        },
        password_hash: {
          bsonType: "string"
        },
        created_at: {
          bsonType: "date"
        }
      }
    }
  }
});


// ---------------------------------------------------
// Indexes (Production Optimization)
// ---------------------------------------------------
db.summaries.createIndex({ created_at: -1 });
db.plagiarism_checks.createIndex({ created_at: -1 });
db.autocorrections.createIndex({ created_at: -1 });
db.users.createIndex({ email: 1 }, { unique: true });
