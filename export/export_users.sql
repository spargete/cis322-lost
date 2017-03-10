\echo 'username,password,role,active'
SELECT u.username, u.password, r.role_name, u.active FROM users AS u INNER JOIN user_is ON u.user_pk=user_fk INNER JOIN roles AS r ON role_fk=r.role_pk;