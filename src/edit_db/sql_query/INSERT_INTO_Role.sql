INSERT INTO "role" (name, permissions) VALUES
('Преподаватель', '{"create", "read", "update", "comment", "get_student_laboratory_for_teacher", "accept", "deny", "add_laboratory", "update_laboratory", "delete_laboratory_by_id", "add_full_discipline", "update_discipline_for_teacher", "info_discipline_by_id", "delete_discipline_by_id"}'),
('Студент', '{"create", "read", "update", "delete", "info_discipline_by_id"}');
