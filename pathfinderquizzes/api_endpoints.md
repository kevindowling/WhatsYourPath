# Quiz Platform API Endpoints

## Categories
- **GET /categories/**: Retrieve a list of all quiz categories.
- **GET /categories/{id}/**: Retrieve a specific quiz category by its ID.
- **POST /categories/**: Create a new quiz category.
- **PUT /categories/{id}/**: Update an existing quiz category.
- **DELETE /categories/{id}/**: Delete a specific quiz category.

## Quizzes
- **GET /quizzes/**: Retrieve all quizzes.
- **GET /quizzes/{id}/**: Retrieve details of a specific quiz.
- **POST /quizzes/**: Create a new quiz.
- **PUT /quizzes/{id}/**: Update an existing quiz.
- **DELETE /quizzes/{id}/**: Delete a specific quiz.

## Questions
- **GET /quizzes/{quiz_id}/questions/**: Retrieve all questions for a specific quiz.
- **GET /quizzes/{quiz_id}/questions/{question_id}/**: Retrieve a specific question within a quiz.
- **POST /quizzes/{quiz_id}/questions/**: Add a new question to a quiz.
- **PUT /quizzes/{quiz_id}/questions/{question_id}/**: Update a question in a quiz.
- **DELETE /quizzes/{quiz_id}/questions/{question_id}/**: Remove a question from a quiz.

## Answers
- **GET /questions/{question_id}/answers/**: Retrieve all answers for a specific question.
- **GET /questions/{question_id}/answers/{answer_id}/**: Retrieve details of a specific answer.
- **POST /questions/{question_id}/answers/**: Create a new answer for a question.
- **PUT /questions/{question_id}/answers/{answer_id}/**: Update an existing answer.
- **DELETE /questions/{question_id}/answers/{answer_id}/**: Delete an answer.

## User Quiz Attempts
- **GET /users/{user_id}/attempts/**: List all quiz attempts by a specific user.
- **GET /users/{user_id}/attempts/{attempt_id}/**: Retrieve details of a specific quiz attempt.
- **POST /quizzes/{quiz_id}/attempt/**: Start a new quiz attempt for a user.
- **PUT /users/{user_id}/attempts/{attempt_id}/**: Update a quiz attempt (e.g., mark as completed).
- **DELETE /users/{user_id}/attempts/{attempt_id}/**: Delete a quiz attempt.

## User Answers
- **POST /attempts/{attempt_id}/answers/**: Submit an answer for a question in a quiz attempt.
- **PUT /attempts/{attempt_id}/answers/{user_answer_id}/**: Update an answer previously submitted in a quiz attempt.
- **DELETE /attempts/{attempt_id}/answers/{user_answer_id}/**: Delete a submitted answer.

## Attribute Thresholds
- **GET /quizzes/{quiz_id}/thresholds/**: Retrieve all attribute thresholds for a quiz.
- **POST /quizzes/{quiz_id}/thresholds/**: Define a new attribute threshold for a quiz.
- **PUT /quizzes/{quiz_id}/thresholds/{threshold_id}/**: Update an existing attribute threshold.
- **DELETE /quizzes/{quiz_id}/thresholds/{threshold_id}/**: Delete an attribute threshold.

## Outcome Codes
- **GET /quizzes/{quiz_id}/outcomes/**: Retrieve all outcome codes for a quiz.
- **POST /quizzes/{quiz_id}/outcomes/**: Create a new outcome code with a specific combination of attribute thresholds.
- **PUT /quizzes/{quiz_id}/outcomes/{outcome_code_id}/**: Update an existing outcome code.
- **DELETE /quizzes/{quiz_id}/outcomes/{outcome_code_id}/**: Delete an outcome code.

## Admin
- **GET /admin/reports/**: Generate and retrieve reports (e.g., quiz statistics, user performance).
