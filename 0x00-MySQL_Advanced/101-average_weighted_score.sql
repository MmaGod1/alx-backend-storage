-- Creates a stored procedure ComputeAverageWeightedScoreForUsers that 
-- computes and store the average weighted score for all students.

DELIMITER //

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users u
    JOIN (
        SELECT c.user_id, 
               SUM(c.score * p.weight) / NULLIF(SUM(p.weight), 0) AS average_score
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        GROUP BY c.user_id
    ) AS weighted_scores ON u.id = weighted_scores.user_id
    SET u.average_score = weighted_scores.average_score;
END //

DELIMITER ;
