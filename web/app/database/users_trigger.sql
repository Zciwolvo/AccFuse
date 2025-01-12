CREATE TRIGGER remove_unverified_users
AFTER INSERT ON users
FOR EACH ROW
BEGIN
  DELETE FROM users
  WHERE verified = FALSE
    AND TIMESTAMPDIFF(MINUTE, created_at, NOW()) > 60;
END$$