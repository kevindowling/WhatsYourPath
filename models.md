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

