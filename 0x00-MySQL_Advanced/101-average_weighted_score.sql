-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store average weighted score for all students
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    UPDATE users AS Users,
        (SELECT Users.id, SUM(score * weight) / SUM(weight) AS avg_weight
        FROM users AS Users
        JOIN corrections as Corrct ON Users.id=Corrct.user_id
        JOIN projects AS Proj ON Corrct.project_id=Proj.id
        GROUP BY Users.id)
    AS AVGW
    SET Users.average_score = AVGW.avg_weight
    WHERE Users.id=AVGW.id;
END
$$
DELIMITER ;
