### Entities and Attributes

1. **User**
   - UserID (Integer)
   - Username (String)
   - Email (String)
   - PasswordHash (String)
   - CreatedAt (DateTime)
   - LastLogin (DateTime, Optional)
   - Role (String, Optional)

2. **Quiz**
   - QuizID (Integer)
   - Title (String)
   - Description (String)
   - CreatedBy (UserID, Integer)
   - CreatedAt (DateTime)
   - UpdatedAt (DateTime)
   - IsPublished (Boolean)

3. **Question**
   - QuestionID (Integer)
   - QuizID (Integer)
   - Text (String)
   - CreatedAt (DateTime)
   - QuestionType (String)
   - Sequence (Integer)

4. **Answer**
   - AnswerID (Integer)
   - QuestionID (Integer)
   - Text (String)
   - CreatedAt (DateTime)

5. **AnswerAttribute**
   - AttributeID (Integer)
   - AnswerID (Integer)
   - AttributeName (String)
   - AttributeValue (Decimal)
 

6. **UserQuizAttempt**
   - AttemptID (Integer)
   - QuizID (Integer)
   - UserID (Integer)
   - StartedAt (DateTime)
   - CompletedAt (DateTime, Optional)
   - Score (String, Optional)


7. **UserAnswer**
   - UserAnswerID (Integer)
   - AttemptID (Integer)
   - QuestionID (Integer)
   - AnswerID (Integer)
   - AnsweredAt (DateTime)




## API Endpoints with Data Types and Simplified Responses

### Getting All Quizzes (Simplified)
- **Endpoint:** `GET /api/quizzes`
- **Function:** Retrieves all published quizzes, returning only quiz names, descriptions, and IDs.
- **Returns:** JSON array of objects with `QuizID`, `Title`, and `Description`.

### Getting a Quiz by ID
- **Endpoint:** `GET /api/quizzes/{quizId}`
- **Function:** Retrieves a specific quiz by its ID, including all its questions and possible answers.
- **Parameters:** `quizId` (Integer) - The unique identifier for the quiz.
- **Returns:** JSON object including `QuizID`, `Title`, `Description`, and an array of `Questions` each with `QuestionID`, `Text`, and `Answers`.

### Creating a Quiz
- **Endpoint:** `POST /api/quizzes`
- **Function:** Allows authenticated users to create a new quiz.
- **Payload:** JSON object containing `Title`, `Description`, and `IsPublished`.
- **Returns:** JSON object with `QuizID`, `Title`, `Description`.

### Adding Questions to a Quiz
- **Endpoint:** `POST /api/quizzes/{quizId}/questions`
- **Function:** Adds a new question to a quiz for authenticated users.
- **Parameters:** `quizId` (Integer) - The unique identifier for the quiz.
- **Payload:** JSON object containing `Text`, `QuestionType`, and `Sequence`.
- **Returns:** JSON object with `QuestionID`, `Text`, `QuestionType`.

### Posting Answers for a Quiz Attempt
- **Endpoint:** `POST /api/quizzes/{quizId}/attempts`
- **Function:** Submits answers for a quiz attempt, tracking the attempt's timing.
- **Parameters:** `quizId` (Integer) - The unique identifier for the quiz.
- **Payload:** JSON array of `Answers`, each with `QuestionID` and `AnswerID`.
- **Returns:** JSON object with `AttemptID`, `QuizID`, `UserID`, `StartedAt`, `CompletedAt`.

### Submitting Answers with Attributes for a Quiz Attempt
- **Endpoint:** `POST /api/quizzes/{quizId}/attempts/{attemptId}/answers`
- **Function:** Allows submitting answers along with selected attributes for each answer during a quiz attempt.
- **Parameters:** 
  - `quizId` (Integer) - The unique identifier for the quiz.
  - `attemptId` (Integer) - The unique identifier for the attempt.
- **Payload:** JSON array of objects, each with `QuestionID`, `AnswerID`, and an array of `Attributes` with `AttributeName` and `Weight`.
- **Returns:** Confirmation of submission, potentially with scores or results based on the quiz logic.

### AI Assistant for Building Quiz (Optional)
- **Endpoint:** `GET /api/aiassistant`
- **Function:** Offers AI-driven suggestions or auto-generated questions/answers based on input or theme.
- **Query Parameters:** (Optional) `theme`, `numQuestions` - Parameters to guide the generation of quiz content.
- **Returns:** JSON array of suggested `Questions` and `Answers`, each question including a list of possible answers.

#### Note:
- For **Creating a Quiz**, **Adding Questions**, and **Posting Answers**, authenticated users must include a valid authentication token in their request headers.
- The actual structure of JSON payloads and responses should be adjusted based on the specific requirements of your application and the details of your implementation.
- Error handling and validation messages are not detailed here but are crucial for a robust API.

