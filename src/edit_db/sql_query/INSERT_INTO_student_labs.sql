INSERT INTO "student_laboratory" (id_lab, id_student, id_teacher, id_discipline, loading_time, url, status, valid, score, count_try) VALUES
(1, 1, 12, 1, '2023-09-20 22:00:00', 'http://example.com/lab1/student1', true,false, 90, 1),
(2, 1, null, 1, '2023-10-15 22:00:00', 'http://example.com/lab1/student1', true,true, 80, 1),
(1, 2, null, 1, '2023-09-21 00:00:00', 'http://example.com/lab1/student2', false,false, 0, 1),
(2, 2, 11, 1, '2023-10-16 00:00:00', 'http://example.com/lab2/student2', true,true, 60, 2),
(1, 3, null, 1, '2023-09-20 23:30:00', 'http://example.com/lab1/student3', true,true, 90, 1),
(2, 3, 11, 1, '2023-10-15 23:30:00', 'http://example.com/lab2/student3', true,true, 90, 1),
(1, 4, null, 1, '2023-09-20 23:00:00', 'http://example.com/lab1/student4', false,true, 80, 2),
(2, 4, null, 1, '2023-10-15 23:00:00', 'http://example.com/lab2/student4', true,true, 80, 2),
(1, 5, 12, 1, '2023-09-21 01:00:00', 'http://example.com/lab1/student5', false,true, 0, 1),
(3, 5, null, 1, '2023-10-16 01:00:00', 'http://example.com/lab3/student5', true,true, 65, 3),
(4, 10, null, 1, '2023-10-15 23:30:00', 'http://example.com/lab4/student10', true,true, 90, 1),
(1, 4, null, 1, '2023-09-20 23:00:00', 'http://example.com/lab1/student4', true,true, 80, 2),
(2, 7, null, 1, '2023-10-15 23:00:00', 'http://example.com/lab2/student4', true,true, 80, 2),
(5, 6, null, 1, '2023-09-21 01:00:00', 'http://example.com/lab5/student6', false,true, 0, 1),
(5, 9, null, 1, '2023-10-16 03:00:00', 'http://example.com/lab5/student9', true,true, 65, 3),
(1, 5, null, 1, '2023-10-21 01:00:00', 'http://example.com/lab1/student5', true,true, 60, 2),
(1, 4, 11, 1, '2023-09-20 23:00:00', 'http://example.com/lab1/student4', true,true, 80, 2),
(6, 7, 12, 2, '2024-04-15 23:00:00', 'http://example.com/la6/student4', true,true, 80, 2),
(8, 6, 12, 2, '2024-06-01 21:20:00', 'http://example.com/lab8/student6', false,true, 0, 1),
(9, 9, null, 2, '2024-05-16 23:52:00', 'http://example.com/lab9/student9', true,true, 65, 3),
(6, 10, null, 2, '2024-05-28 15:10:00', 'http://example.com/lab1/student5', true,true, 60, 2);