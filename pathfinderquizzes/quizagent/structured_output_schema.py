# structured_output_schema.py
from pydantic import BaseModel, Field
from typing import List

class AttributeSchema(BaseModel):
    AttributeName: str = Field(..., description="The name of the attribute that this answer impacts.")
    Weight: float = Field(..., description="The numeric weight of this attribute as contributed by the answer, which will be accumulated for comparison to a threshold.")

class AnswerSchema(BaseModel):
    Text: str = Field(..., description="The answer text presented to the user.")
    attributes: List[AttributeSchema] = Field(..., description="A list of attributes associated with this answer and their corresponding weights.")

class QuestionSchema(BaseModel):
    Text: str = Field(..., description="The question text presented to the user.")
    QuestionType: str = Field(..., description="The type of the question, such as 'Multiple Choice'.")
    Sequence: int = Field(..., description="The order or sequence number of the question in the quiz.")
    answers: List[AnswerSchema] = Field(..., description="A list of possible answers for this question, each with attributes affecting the quiz outcomes.")

class OutcomeCodeSchema(BaseModel):
    CombinationCode: str = Field(..., description="The unique code representing a combination of outcomes derived from evaluating all attribute thresholds in the quiz.")
    Description: str = Field(..., description="A description of what this combination code represents in terms of user assessment.")

class AttributeThresholdSchema(BaseModel):
    AttributeName: str = Field(..., description="The name of the attribute whose accumulated weight will be evaluated.")
    ThresholdValue: float = Field(..., description="The threshold value that the accumulated attribute weight must be compared to.")
    Description: str = Field(..., description="A description of the attribute threshold, including its significance for grading.")
    GradingInstruction: str = Field(..., description="Instructions on how the attribute threshold should affect grading or outcomes.")
    LeftCodeString: str = Field(..., description="The code to use if the accumulated attribute weight is below the threshold value, contributing to the final outcome code.")
    RightCodeString: str = Field(..., description="The code to use if the accumulated attribute weight is equal to or above the threshold value, contributing to the final outcome code.")

class StructuredOutputSchema(BaseModel):
    Title: str = Field(..., description="The title of the quiz.")
    Description: str = Field(..., description="A description of the quiz.")
    QuizCategory: int = Field(..., description="An identifier for the category of the quiz.")
    CreatedBy: int = Field(..., description="The user ID of the person who created the quiz.")
    IsPublished: bool = Field(..., description="Indicates whether the quiz is published and available to users.")
    questions: List[QuestionSchema] = Field(..., description="A list of questions that make up the quiz.")
    outcomecodes: List[OutcomeCodeSchema] = Field(..., description="A list of possible outcome codes, each representing a unique combination of the LeftCodeString or RightCodeString values from all attribute thresholds.")
    attributethresholds: List[AttributeThresholdSchema] = Field(..., description="A list of attribute thresholds that determine the quiz outcome by comparing accumulated weights for each attribute to predefined thresholds.")

