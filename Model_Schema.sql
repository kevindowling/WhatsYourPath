-- Users table
CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL,
    CreatedAt DATETIME NOT NULL,
    LastLogin DATETIME,
    Role VARCHAR(255)
);

-- Quizzes table
CREATE TABLE Quizzes (
    QuizID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title VARCHAR(255) NOT NULL,
    Description TEXT NOT NULL,
    CreatedBy INTEGER NOT NULL,
    CreatedAt DATETIME NOT NULL,
    UpdatedAt DATETIME NOT NULL,
    IsPublished BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (CreatedBy) REFERENCES Users(UserID)
);

-- Questions table
CREATE TABLE Questions (
    QuestionID INTEGER PRIMARY KEY AUTOINCREMENT,
    QuizID INTEGER NOT NULL,
    Text VARCHAR(255) NOT NULL,
    CreatedAt DATETIME NOT NULL,
    QuestionType VARCHAR(255) NOT NULL,
    Sequence INTEGER NOT NULL,
    FOREIGN KEY (QuizID) REFERENCES Quizzes(QuizID)
);

-- Answers table
CREATE TABLE Answers (
    AnswerID INTEGER PRIMARY KEY AUTOINCREMENT,
    QuestionID INTEGER NOT NULL,
    Text VARCHAR(255) NOT NULL,
    CreatedAt DATETIME NOT NULL,
    FOREIGN KEY (QuestionID) REFERENCES Questions(QuestionID)
);

-- AnswerAttributes table
CREATE TABLE AnswerAttributes (
    AttributeID INTEGER PRIMARY KEY AUTOINCREMENT,
    AnswerID INTEGER NOT NULL,
    AttributeName VARCHAR(255) NOT NULL,
    AttributeValue DECIMAL NOT NULL,
    FOREIGN KEY (AnswerID) REFERENCES Answers(AnswerID)
);

-- UserQuizAttempts table
CREATE TABLE UserQuizAttempts (
    AttemptID INTEGER PRIMARY KEY AUTOINCREMENT,
    QuizID INTEGER NOT NULL,
    UserID INTEGER NOT NULL,
    StartedAt DATETIME NOT NULL,
    CompletedAt DATETIME,
    Score VARCHAR(255),
    FOREIGN KEY (QuizID) REFERENCES Quizzes(QuizID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- UserAnswers table
CREATE TABLE UserAnswers (
    UserAnswerID INTEGER PRIMARY KEY AUTOINCREMENT,
    AttemptID INTEGER NOT NULL,
    QuestionID INTEGER NOT NULL,
    AnswerID INTEGER NOT NULL,
    AnsweredAt DATETIME NOT NULL,
    FOREIGN KEY (AttemptID) REFERENCES UserQuizAttempts(AttemptID),
    FOREIGN KEY (QuestionID) REFERENCES Questions(QuestionID),
    FOREIGN KEY (AnswerID) REFERENCES Answers(AnswerID)
);
