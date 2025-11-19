SELECT
    users.id,
    users.email,
    COUNT(tasks.id) AS task_count
FROM users
LEFT JOIN tasks ON tasks.user_id = users.id
WHERE users.active = TRUE
GROUP BY users.id, users.email
ORDER BY task_count DESC;
