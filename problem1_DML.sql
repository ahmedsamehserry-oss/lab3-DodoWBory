
USE company;
INSERT INTO DEPARTMENT (Dnumber, Dname, mgr_ssn, mgr_start_date) VALUES
(1, 'Engineering', NULL, NULL),
(2, 'Finance', NULL, NULL),
(3, 'Marketing', NULL, NULL);

INSERT INTO EMPLOYEE (ssn, fname, lname, bdate, address, gender, salary, Dno) VALUES
('100000001', 'ahmed', 'sameh', '2005-01-04', 'Alexandria', 'M', 70000, 1),
('100000002', 'mohamed', 'aber', '2005-08-12', 'Alexandria', 'M', 60000, 2),
('100000003', 'eng', 'basem', '2003-01-15', 'Alexandria', 'M', 100000, 3);

INSERT INTO PROJECT (Pnumber, Pname, Plocation, Dno) VALUES
(101, 'Portal Upgrade', 'Alexandria', 1),
(102, 'Budget Review', 'Cairo', 2),
(103, 'Brand Campaign', 'Giza', 3);

UPDATE DEPARTMENT SET mgr_ssn = '100000001', mgr_start_date = '2026-10-01' WHERE Dnumber = 1;
UPDATE DEPARTMENT SET mgr_ssn = '100000002', mgr_start_date = '2026-10-02' WHERE Dnumber = 2;
UPDATE DEPARTMENT SET mgr_ssn = '100000003', mgr_start_date = '2026-10-03' WHERE Dnumber = 3;

SELECT * FROM DEPARTMENT;
SELECT * FROM EMPLOYEE; 
SELECT * FROM PROJECT;
