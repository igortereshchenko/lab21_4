--heroku pg:psql

CREATE TABLE "Student" (
    student_id int PRIMARY KEY,
    student_university VARCHAR(255) NOT NULL,
    student_faculty VARCHAR(255) NOT NULL,
    student_group VARCHAR(255) NOT NULL,
    student_name VARCHAR(255) NOT NULL,
    student_surname VARCHAR(255) NOT NULL,
    student_birthday DATE,
    student_date_enrollment DATE NOT NULL DEFAULT CURRENT_DATE,
    student_date_expelled DATE,
    UNIQUE (student_university,
            student_faculty,
            student_group,
            student_name,
            student_surname )
);

CREATE SEQUENCE student_id_sequence START 1;


CREATE TABLE "Professor" (
    professor_id int PRIMARY KEY,
    professor_university VARCHAR(255) NOT NULL,
    professor_department VARCHAR(255) NOT NULL,
    professor_name VARCHAR(255) NOT NULL,
    professor_surname VARCHAR(255) NOT NULL,
    professor_degree VARCHAR(255),
    professor_date_enrollment DATE NOT NULL DEFAULT CURRENT_DATE,
    professor_date_expelled DATE,
    professor_birthday DATE,
    UNIQUE ( professor_university,
             professor_department,
             professor_name,
             professor_surname )
);

CREATE SEQUENCE professor_id_sequence START 1;

---------------------------------------------------------

CREATE TABLE "Univer" (
    id int PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    year DATE,
    degree VARCHAR(255)
);

CREATE SEQUENCE table_id_sequence START 1;

CREATE OR REPLACE FUNCTION incr_table() RETURNS trigger AS $$
        BEGIN
            NEW.id = nextval('table_id_sequence');
            return NEW;
        END;

$$  LANGUAGE plpgsql;

CREATE TRIGGER table_increment
    BEFORE insert ON "Univer"
    FOR EACH ROW
    EXECUTE PROCEDURE incr_table();

----------------------------------------------------------

CREATE TABLE "Discipline" (
    discipline_university VARCHAR(255),
    discipline_faculty VARCHAR(255),
    discipline_name VARCHAR(255),
    discipline_exam BOOLEAN NOT NULL,
    discipline_hours_for_semester INT,
    univ_fk int,
    PRIMARY KEY (discipline_university, discipline_faculty, discipline_name),
    FOREIGN KEY (univ_fk) REFERENCES "Univer"(id)
);

CREATE TABLE "StudentRecordBook" (
    student_id_fk int,
    discipline_university_fk VARCHAR(255),
    discipline_faculty_fk VARCHAR(255),
    discipline_name_fk VARCHAR(255),
    professor_id_fk int,

    semester_mark INT DEFAULT 0,
    final_mark INT DEFAULT 0,
    exam_passed DATE,
    PRIMARY KEY (student_id_fk,
                 discipline_university_fk,
                 discipline_faculty_fk,
                 discipline_name_fk,
                 professor_id_fk),
    FOREIGN KEY (student_id_fk) REFERENCES "Student"(student_id),
    FOREIGN KEY (discipline_university_fk,
                 discipline_faculty_fk,
                 discipline_name_fk) REFERENCES "Discipline"(discipline_university,
                                                           discipline_faculty,
                                                           discipline_name),
    FOREIGN KEY (professor_id_fk) REFERENCES "Professor"(professor_id)
);

CREATE OR REPLACE FUNCTION check_fun() RETURNS trigger AS $$
        DECLARE
           uni VARCHAR(255);
           faculty VARCHAR(255);
        BEGIN
            select student_university, student_faculty into uni, faculty from "Student"
            where student_id=NEW.student_id_fk;
            if uni = NEW.discipline_university_fk and NEW.discipline_faculty_fk = faculty then
                select professor_university into uni from "Professor"
                where professor_id = NEW.professor_id_fk;
                if uni = NEW.discipline_university_fk then
                    return NEW;
                else
                    RAISE EXCEPTION 'professor from another university';
                end if;
            else
                RAISE EXCEPTION 'student and discipline from another uni or faculty';
            end if;
        END;

$$  LANGUAGE plpgsql;

CREATE TRIGGER check_insert_record_book
    BEFORE insert ON "StudentRecordBook"
    FOR EACH ROW
    EXECUTE PROCEDURE check_fun();



CREATE OR REPLACE FUNCTION incr_student() RETURNS trigger AS $$
        BEGIN
            NEW.student_id = nextval('student_id_sequence');
            return NEW;
        END;

$$  LANGUAGE plpgsql;

CREATE TRIGGER student_increment
    BEFORE insert ON "Student"
    FOR EACH ROW
    EXECUTE PROCEDURE incr_student();


CREATE OR REPLACE FUNCTION incr_professor() RETURNS trigger AS $$
        BEGIN
            NEW.professor_id = nextval('professor_id_sequence');
            return NEW;
        END;

$$  LANGUAGE plpgsql;

CREATE TRIGGER professor_increment
    BEFORE insert ON "Professor"
    FOR EACH ROW
    EXECUTE PROCEDURE incr_professor();

-- create trigger for sequence and for before insert into record book (check uni, faculty
-- same for student and discipline and uni same for professor)

drop table "StudentRecordBook";
drop table "Student";
drop table "Professor";
drop table "Discipline";
drop sequence professor_id_sequence;
drop sequence student_id_sequence;