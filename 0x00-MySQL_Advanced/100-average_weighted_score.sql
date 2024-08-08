-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store average weighted score for student
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
    DECLARE avg_weight_score FLOAT;
    SET avg_weight_score = (SELECT SUM(score * weight) / SUM(weight)
			FROM users AS Users
			JOIN corrections as Corrct ON Users.id=Corrct.user_id
                        JOIN projects AS Proj ON Corct.project_id=Proj.id
                        WHERE Users.id=user_id);
    UPDATE users SET average_score = weight_avg_score WHERE id=user_id;
END
$$
DELIMITER ;)
