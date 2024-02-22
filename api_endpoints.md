
## API Endpoints with Data Types and Simplified Responses

### Getting All Published Quizzes
- **Endpoint:** `GET /api/quizzes/published`
- **Function:** Retrieves all published quizzes, returning only quiz names, descriptions, and IDs.
- **Returns:** JSON array of objects with `QuizID`, `Title`, and `Description`.

### Getting All Quiz Categories
- **Endpoint:** `GET /api/quiz-categories`
- **Function:** Retrieves a list of all unique quiz categories.
- **Returns:** JSON array of strings representing the unique categories.

### Getting Published Quizzes by Category
- **Endpoint:** `GET /api/quizzes/published/{category}`
- **Function:** Retrieves all published quizzes for a specific category, returning quiz names, descriptions, and IDs.
- **Parameters:** `category` - The category of the quizzes to retrieve.
- **Returns:** JSON array of objects with `QuizID`, `Title`, and `Description`.

### Getting Quiz Details by ID
- **Endpoint:** `GET /api/quizzes/{quizId}`
- **Function:** Retrieves detailed information about a specific quiz, including questions and answer options.
- **Parameters:** `quizId` - The ID of the quiz to retrieve.
- **Returns:** JSON object with quiz details, including `QuizID`, `Title`, `Description`, `Category`, `Questions` (with `QuestionID`, `Text`, `QuestionType`, `Answers`).

### Submitting Quiz Answers
- **Endpoint:** `POST /api/quizzes/{quizId}/submit`
- **Function:** Receives the user's answers for a quiz, calculates the result based on answer attributes, and returns the calculated result.
- **Parameters:** `quizId` - The ID of the quiz being attempted.
- **Body:** JSON object containing `UserID`, `Answers` (array of objects with `QuestionID` and `AnswerID`).
- **Returns:** JSON object with the result, including `ResultName`, `ResultDescription`, and any additional advice or recommendations.

## Creating a Quiz
- **Endpoint:** `POST /api/quizzes`
- **Function:** Allows users to create a new quiz.
- **Authorization:** Bearer token required to validate the user.
- **Body:** JSON object containing `Title`, `Description`, `Category`, and `IsPublished` status.
- **Returns:** JSON object with the newly created `QuizID`, `Title`, `Description`, and `IsPublished` status.

## Adding a Question to User's Quiz
- **Endpoint:** `POST /api/quizzes/{quizId}/questions`
- **Function:** Allows users to add a new question to one of their quizzes.
- **Authorization:** Bearer token required. Verifies that the quiz belongs to the user.
- **Parameters:** `quizId` - The ID of the user's quiz to which the question will be added.
- **Body:** JSON object containing `Text`, `QuestionType`, and `Sequence`.
- **Returns:** JSON object with the newly added `QuestionID`, `Text`, `QuestionType`, and `Sequence`.

## Adding an AnswerAttribute to an Answer from User's Quiz
- **Endpoint:** `POST /api/quizzes/{quizId}/questions/{questionId}/answers/{answerId}/attributes`
- **Function:** Allows users to add an attribute to an answer in one of their quizzes.
- **Authorization:** Bearer token required. Verifies that the quiz and question belong to the user.
- **Parameters:** 
    - `quizId` - The ID of the user's quiz.
    - `questionId` - The ID of the question within the quiz.
    - `answerId` - The ID of the answer to which the attribute will be added.
- **Body:** JSON object containing `AttributeName` and `Weight`.
- **Returns:** JSON object with the newly added `AttributeID`, `AttributeName`, and `Weight`.

## Adding an AttributeThreshold to User's Quiz
- **Endpoint:** `POST /api/quizzes/{quizId}/attributes/thresholds`
- **Function:** Allows users to add an attribute threshold to one of their quizzes.
- **Authorization:** Bearer token required. Verifies that the quiz belongs to the user.
- **Parameters:** `quizId` - The ID of the user's quiz.
- **Body:** JSON object containing `AttributeName`, `ThresholdValue`, `Description`, and `GradingInstruction`.
- **Returns:** JSON object with the newly added `AttributeThresholdID`, `AttributeName`, `ThresholdValue`, `Description`, and `GradingInstruction`.

## Updating an AttributeThreshold of User's Quiz
- **Endpoint:** `PUT /api/quizzes/{quizId}/attributes/thresholds/{thresholdId}`
- **Function:** Allows users to update an attribute threshold in one of their quizzes.
- **Authorization:** Bearer token required. Verifies that the quiz belongs to the user.
- **Parameters:** 
    - `quizId` - The ID of the user's quiz.
    - `thresholdId` - The ID of the attribute threshold to be updated.
- **Body:** JSON object containing any of `ThresholdValue`, `Description`, and `GradingInstruction` to be updated.
- **Returns:** JSON object with the updated `AttributeThresholdID`, `AttributeName`, `ThresholdValue`, `Description`, and `GradingInstruction`.

## Removing a Question from User's Quiz
- **Endpoint:** `DELETE /api/quizzes/{quizId}/questions/{questionId}`
- **Function:** Allows users to remove a question from one of their quizzes.
- **Authorization:** Bearer token required. Verifies that the quiz and question belong to the user.
- **Parameters:** 
    - `quizId` - The ID of the user's quiz.
    - `questionId` - The ID of the question to be removed.
- **Returns:** A status message indicating the question has been successfully removed.

