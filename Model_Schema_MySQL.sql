
CREATE TABLE `Users` (
    `UserID` INT AUTO_INCREMENT PRIMARY KEY,
    `Username` VARCHAR(255) NOT NULL,
    `Email` VARCHAR(255) NOT NULL UNIQUE,
    `PasswordHash` CHAR(60) NOT NULL,
    `CreatedAt` DATETIME NOT NULL,
    `LastLogin` DATETIME DEFAULT NULL,
    `Role` VARCHAR(50) DEFAULT NULL
) ENGINE=InnoDB;

CREATE TABLE `Quiz` (
    `QuizID` INT AUTO_INCREMENT PRIMARY KEY,
    `Title` VARCHAR(255) NOT NULL,
    `Description` TEXT,
    `CreatedBy` INT NOT NULL,
    `CreatedAt` DATETIME NOT NULL,
    `UpdatedAt` DATETIME NOT NULL,
    `IsPublished` BOOLEAN NOT NULL,
    CONSTRAINT `fk_Quiz_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB;

CREATE TABLE `Question` (
    `QuestionID` INT AUTO_INCREMENT PRIMARY KEY,
    `QuizID` INT NOT NULL,
    `Text` TEXT NOT NULL,
    `CreatedAt` DATETIME NOT NULL,
    `QuestionType` VARCHAR(50) NOT NULL,
    `Sequence` INT NOT NULL,
    CONSTRAINT `fk_Question_QuizID` FOREIGN KEY (`QuizID`) REFERENCES `Quiz` (`QuizID`)
) ENGINE=InnoDB;

CREATE TABLE `Answer` (
    `AnswerID` INT AUTO_INCREMENT PRIMARY KEY,
    `QuestionID` INT NOT NULL,
    `Text` TEXT NOT NULL,
    CONSTRAINT `fk_Answer_QuestionID` FOREIGN KEY (`QuestionID`) REFERENCES `Question` (`QuestionID`)
) ENGINE=InnoDB;

CREATE TABLE `AnswerAttribute` (
    `AttributeID` INT AUTO_INCREMENT PRIMARY KEY,
    `AnswerID` INT NOT NULL,
    `AttributeName` VARCHAR(255) NOT NULL,
    `Weight` DECIMAL(10,2) NOT NULL,
    CONSTRAINT `fk_AnswerAttribute_AnswerID` FOREIGN KEY (`AnswerID`) REFERENCES `Answer` (`AnswerID`)
) ENGINE=InnoDB;

CREATE TABLE `UserQuizAttempt` (
    `AttemptID` INT AUTO_INCREMENT PRIMARY KEY,
    `QuizID` INT NOT NULL,
    `UserID` INT NOT NULL,
    `StartedAt` DATETIME NOT NULL,
    `CompletedAt` DATETIME DEFAULT NULL,
    CONSTRAINT `fk_UserQuizAttempt_QuizID` FOREIGN KEY (`QuizID`) REFERENCES `Quiz` (`QuizID`),
    CONSTRAINT `fk_UserQuizAttempt_UserID` FOREIGN KEY (`UserID`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB;

CREATE TABLE `UserAnswer` (
    `UserAnswerID` INT AUTO_INCREMENT PRIMARY KEY,
    `AttemptID` INT NOT NULL,
    `QuestionID` INT NOT NULL,
    `AnswerID` INT NOT NULL,
    `AnsweredAt` DATETIME NOT NULL,
    CONSTRAINT `fk_UserAnswer_AttemptID` FOREIGN KEY (`AttemptID`) REFERENCES `UserQuizAttempt` (`AttemptID`),
    CONSTRAINT `fk_UserAnswer_QuestionID` FOREIGN KEY (`QuestionID`) REFERENCES `Question` (`QuestionID`),
    CONSTRAINT `fk_UserAnswer_AnswerID` FOREIGN KEY (`AnswerID`) REFERENCES `Answer` (`AnswerID`)
) ENGINE=InnoDB;

CREATE TABLE `AttributeThreshold` (
    `AttributeThresholdID` INT AUTO_INCREMENT PRIMARY KEY,
    `QuizID` INT NOT NULL,
    `AttributeName` VARCHAR(255) NOT NULL,
    `ThresholdValue` DECIMAL(10,2) NOT NULL,
    `Description` TEXT DEFAULT NULL,
    `GradingInstruction` TEXT DEFAULT NULL,
    CONSTRAINT `fk_AttributeThreshold_QuizID` FOREIGN KEY (`QuizID`) REFERENCES `Quiz` (`QuizID`)
) ENGINE=InnoDB;
