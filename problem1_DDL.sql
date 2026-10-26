
DROP DATABASE IF EXISTS company;
CREATE DATABASE company;
USE company;
CREATE TABLE DEPARTMENT (
    Dnumber INT NOT NULL,
    Dname VARCHAR(50) NOT NULL,
    mgr_ssn CHAR(9),
    mgr_start_date DATE,
    PRIMARY KEY (Dnumber)
);
CREATE TABLE EMPLOYEE (
    ssn CHAR(9) NOT NULL,
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    bdate DATE,
    address VARCHAR(100),
    gender CHAR(1),
    salary DECIMAL(10,2),
    Dno INT NOT NULL,
    PRIMARY KEY (ssn),
    CONSTRAINT fk_employee_department
        FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber)
);

CREATE TABLE PROJECT (
    Pnumber INT NOT NULL,
    Pname VARCHAR(100) NOT NULL,
    Plocation VARCHAR(100),
    Dno INT NOT NULL,
    PRIMARY KEY (Pnumber),
    CONSTRAINT fk_project_department
        FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber)
);
ALTER TABLE DEPARTMENT
    ADD CONSTRAINT fk_department_manager
    FOREIGN KEY (mgr_ssn) REFERENCES EMPLOYEE(ssn);
