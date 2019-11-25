
insert into "Student"(
                    student_university,
                    student_faculty,
                    student_group,
                    student_name,
                    student_surname)
values ('kpi', 'FPM', 'km-61', 'eugene', 'patrushev');

insert into "Student"(
                    student_university,
                    student_faculty,
                    student_group,
                    student_name,
                    student_surname)
values ('kpi', 'FPM', 'km-61', 'vova', 'pasko');

insert into "Student"(
                    student_university,
                    student_faculty,
                    student_group,
                    student_name,
                    student_surname)
values ('kpi', 'FPM', 'km-61', 'nikita', 'mozgovoy');

insert into "Student"(
                    student_university,
                    student_faculty,
                    student_group,
                    student_name,
                    student_surname)
values ('kpi', 'FPM', 'km-62', 'yarik', 'neznau');

-----------------------------------------------------------------------------------------------------------------------

insert into "Professor"(
                    professor_university,
                    professor_department,
                    professor_name,
                    professor_surname,
                    professor_degree)
values ('kpi', 'FPM', 'Volodimir', 'Malrchikov', 'professor');


insert into "Professor"(
                    professor_university,
                    professor_department,
                    professor_name,
                    professor_surname,
                    professor_degree)
values ('kpi', 'FPM', 'Tatiana', 'Ladogubets', 'professor');

insert into "Professor"(
                    professor_university,
                    professor_department,
                    professor_name,
                    professor_surname,
                    professor_degree)
values ('kpi', 'FPM', 'Katia', 'Adamuk', 'doctor');

insert into "Professor"(
                    professor_university,
                    professor_department,
                    professor_name,
                    professor_surname,
                    professor_degree)
values ('kpi', 'IASA', 'Denis', 'Lvovich', 'doctor');

----------------------------------------------------------------------------------------------------------------------

insert into "Univer"(
                    name,
                    address,
                    year,
                    degree )
values ('kpi', 'kpi', '2019-10-15', 'uni');


insert into "Univer"(
                    name,
                    address,
                    year,
                    degree )
values ('sheva', 'sheva', '2019-10-20', 'uni');


insert into "Univer"(
                    name,
                    address,
                    year,
                    degree )
values ('nau', 'nau', '2019-10-25', 'uni');


------------------------------------------------------------------------------------------------------------


insert into "Discipline"(discipline_university,
                       discipline_faculty,
                       discipline_name,
                       discipline_exam,
                       univ_fk,
                       discipline_hours_for_semester)
values ('kpi', 'FPM', 'Mat Analise', TRUE, 1, 130);

insert into "Discipline"(discipline_university,
                       discipline_faculty,
                       discipline_name,
                       discipline_exam,
                       univ_fk,
                       discipline_hours_for_semester)
values ('kpi', 'FPM', 'DB_2', TRUE, 1, 120);

insert into "Discipline"(discipline_university,
                       discipline_faculty,
                       discipline_name,
                       discipline_exam,
                       univ_fk,
                       discipline_hours_for_semester)
values ('kpi', 'FPM', 'English', FALSE, 1, 90);

insert into "Discipline"(discipline_university,
                       discipline_faculty,
                       discipline_name,
                       discipline_exam,
                       univ_fk,
                       discipline_hours_for_semester)
values ('kpi', 'FPM', 'Mat Stat', FALSE, 1, 60);

----------------------------------------------------------------------------------------------------------------------

insert into "StudentRecordBook"(student_id_fk,
                              discipline_university_fk,
                              discipline_faculty_fk,
                              discipline_name_fk,
                              professor_id_fk,
                              semester_mark,
                              final_mark,
                              exam_passed)
values (1, 'kpi', 'FPM', 'DB_2', 2, 45, 85, '2019-10-15');

insert into "StudentRecordBook"(student_id_fk,
                              discipline_university_fk,
                              discipline_faculty_fk,
                              discipline_name_fk,
                              professor_id_fk,
                              semester_mark,
                              final_mark,
                              exam_passed)
values (1, 'kpi', 'FPM', 'English', 3, 50, 80, '2019-10-15');

insert into "StudentRecordBook"(student_id_fk,
                              discipline_university_fk,
                              discipline_faculty_fk,
                              discipline_name_fk,
                              professor_id_fk,
                              semester_mark)
values (1, 'kpi', 'FPM', 'Mat Stat', 1, 45);

insert into "StudentRecordBook"(student_id_fk,
                              discipline_university_fk,
                              discipline_faculty_fk,
                              discipline_name_fk,
                              professor_id_fk,
                              semester_mark,
                              final_mark,
                              exam_passed)
values (2, 'kpi', 'FPM', 'DB_2', 2, 30, 60, '2019-10-18');