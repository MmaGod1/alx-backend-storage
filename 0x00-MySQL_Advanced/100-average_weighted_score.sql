-- Creates a stored procedure ComputeAverageWeightedScoreForUser that
-- computes and store the average weighted score for a student.

DELIMITER //

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser; 

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;

    -- Calculate total weighted score and total weight
    SELECT SUM(c.score * p.weight) INTO total_score
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    SELECT SUM(p.weight) INTO total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- Update the user's average score in the users table
    IF total_weight > 0 THEN
        UPDATE users SET average_score = total_score / total_weight WHERE id = user_id;
    ELSE
        UPDATE users SET average_score = 0 WHERE id = user_id;
    END IF;
END //

DELIMITER ;
