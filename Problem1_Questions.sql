USE company;

INSERT INTO DEPARTMENT
(Dnumber, Dname, mgr_ssn, mgr_start_date)
VALUES
(4, 'Quality Assurance', '100000001', '2026-10-20');

DELETE FROM EMPLOYEE
WHERE ssn = '100000001';

INSERT INTO PROJECT
(Pnumber, Pname, Plocation, Dno)
VALUES
(104, 'Test Project', 'Cairo', 999);