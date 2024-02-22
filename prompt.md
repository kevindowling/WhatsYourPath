### Application

Web app for creating quizes like "What's the right job for me?" or "What's my personality type?" and retrieving the quizes via an api

### Current Data Model

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

5. **AnswerAttribute**
   - AttributeID (Integer)
   - AnswerID (Integer)
   - AttributeName (String)
   - Weight (Decimal)

6. **UserQuizAttempt**
   - AttemptID (Integer)
   - QuizID (Integer)
   - UserID (Integer)
   - StartedAt (DateTime)
   - CompletedAt (DateTime)

7. **UserAnswer**
   - UserAnswerID (Integer)
   - AttemptID (Integer)
   - QuestionID (Integer)
   - AnswerID (Integer)
   - AnsweredAt (DateTime)

8. **AttributeThreshold**
   - AttributeThresholdID (Integer)
   - QuizID (Integer)
   - AttributeName (String)
   - ThresholdValue (Decimal)
   - Description (String, Optional)
   - GradingInstruction (String)

### Current API Endpoints:

## Getting All Published Quizzes
- **Endpoint:** `GET /api/quizzes/published`
- **Function:** Retrieves all published quizzes, returning only quiz names, descriptions, and IDs.
- **Returns:** JSON array of objects with `QuizID`, `Title`, and `Description`.

## Getting All Quiz Categories
- **Endpoint:** `GET /api/quiz-categories`
- **Function:** Retrieves a list of all unique quiz categories.
- **Returns:** JSON array of strings representing the unique categories.

## Getting Published Quizzes by Category
- **Endpoint:** `GET /api/quizzes/published/{category}`
- **Function:** Retrieves all published quizzes for a specific category, returning quiz names, descriptions, and IDs.
- **Parameters:** `category` - The category of the quizzes to retrieve.
- **Returns:** JSON array of objects with `QuizID`, `Title`, and `Description`.

## Getting Quiz Details by ID
- **Endpoint:** `GET /api/quizzes/{quizId}`
- **Function:** Retrieves detailed information about a specific quiz, including questions and answer options.
- **Parameters:** `quizId` - The ID of the quiz to retrieve.
- **Returns:** JSON object with quiz details, including `QuizID`, `Title`, `Description`, `Category`, `Questions` (with `QuestionID`, `Text`, `QuestionType`, `Answers`).

## Submitting Quiz Answers
- **Endpoint:** `POST /api/quizzes/{quizId}/submit`
- **Function:** Receives the user's answers for a quiz, calculates the result based on answer attributes, and returns the calculated result.
- **Parameters:** `quizId` - The ID of the quiz being attempted.
- **Body:** JSON object containing `UserID`, `Answers` (array of objects with `QuestionID` and `AnswerID`).
- **Returns:** JSON object with the result, including `ResultName`, `ResultDescription`, and any additional advice or recommendations.


### Prompt

Create endpoints for the following.
1. Creating a quiz
2. Adding a question to User's quiz
3. Adding an AnswerAttribute to an answer from User's quiz
4. Adding an AttributeThreshold to User's quiz
5. Updating an AttributeThreshold `ThresholdValue`, `Description`, or `GradingInstruction` of User's quiz
6. Removing a question from User's quiz

A token will be given to the user and the quizes will be returned from that user's token value.

Output your response in a codeblock 