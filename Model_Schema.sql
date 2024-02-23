CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    PasswordHash CHAR(60) NOT NULL, -- Assuming bcrypt is used
    CreatedAt DATETIME NOT NULL,
    LastLogin DATETIME,
    Role VARCHAR(50)
);

CREATE TABLE QuizCategory (
    QuizCategoryID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    CreatedAt DATETIME NOT NULL,
    UpdatedAt DATETIME NOT NULL
);

CREATE TABLE Quiz (
    QuizID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Description TEXT,
    QuizCategoryID INT NOT NULL,
    CreatedBy INT NOT NULL,
    CreatedAt DATETIME NOT NULL,
    UpdatedAt DATETIME NOT NULL,
    IsPublished BOOLEAN NOT NULL,
    FOREIGN KEY (CreatedBy) REFERENCES Users(UserID),
    FOREIGN KEY (QuizCategoryID) REFERENCES QuizCategory(QuizCategoryID)
);

CREATE TABLE Question (
    QuestionID INT AUTO_INCREMENT PRIMARY KEY,
    QuizID INT NOT NULL,
    Text TEXT NOT NULL,
    CreatedAt DATETIME NOT NULL,
    QuestionType VARCHAR(50) NOT NULL,
    Sequence INT NOT NULL,
    FOREIGN KEY (QuizID) REFERENCES Quiz(QuizID)
);

CREATE TABLE Answer (
    AnswerID INT AUTO_INCREMENT PRIMARY KEY,
    QuestionID INT NOT NULL,
    Text TEXT NOT NULL,
    FOREIGN KEY (QuestionID) REFERENCES Question(QuestionID)
);

CREATE TABLE AnswerAttribute (
    AttributeID INT AUTO_INCREMENT PRIMARY KEY,
    AnswerID INT NOT NULL,
    AttributeName VARCHAR(255) NOT NULL,
    Weight DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (AnswerID) REFERENCES Answer(AnswerID)
);

CREATE TABLE UserQuizAttempt (
    AttemptID INT AUTO_INCREMENT PRIMARY KEY,
    QuizID INT NOT NULL,
    UserID INT NOT NULL,
    StartedAt DATETIME NOT NULL,
    CompletedAt DATETIME,
    FOREIGN KEY (QuizID) REFERENCES Quiz(QuizID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE UserAnswer (
    UserAnswerID INT AUTO_INCREMENT PRIMARY KEY,
    AttemptID INT NOT NULL,
    QuestionID INT NOT NULL,
    AnswerID INT NOT NULL,
    AnsweredAt DATETIME NOT NULL,
    FOREIGN KEY (AttemptID) REFERENCES UserQuizAttempt(AttemptID),
    FOREIGN KEY (QuestionID) REFERENCES Question(QuestionID),
    FOREIGN KEY (AnswerID) REFERENCES Answer(AnswerID)
);

CREATE TABLE AttributeThreshold (
    AttributeThresholdID INT AUTO_INCREMENT PRIMARY KEY,
    QuizID INT NOT NULL,
    AttributeName VARCHAR(255) NOT NULL,
    ThresholdValue DECIMAL(10,2) NOT NULL,
    Description TEXT,
    GradingInstruction TEXT,
    FOREIGN KEY (QuizID) REFERENCES Quiz(QuizID)
);
