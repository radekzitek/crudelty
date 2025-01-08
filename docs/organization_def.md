Definition of the organization:

Organization attributes:

- Name
- Address
- Phone
- Email
- Website
- Top department
- Departments

Department attributes:

- Name
- Description
- Parent department
- Subdepartments
- Head of department
- Employees

Position attributes:

- Name
- Description
- Department
- Holder employee
    (one employee can hold multiple positions)

Team attributes:

- Name
- Description
- Team leader
- Parent team
- Subteams
- Employees
    (one employee can be a member of multiple teams)

Employee attributes:

- Name
- Email
- Phone


Entity relationships:

Entities and Their Attributes:

Organization:

OrganizationID (Primary Key, Auto-incrementing Integer or UUID)
Name (Text)
Address (Text)
Phone (Text)
Email (Text)
Website (Text)
TopDepartmentID (Foreign Key referencing Department.DepartmentID)
Department:

DepartmentID (Primary Key, Auto-incrementing Integer or UUID)
Name (Text)
Description (Text)
ParentDepartmentID (Foreign Key referencing Department.DepartmentID, Self-referencing for hierarchy, can be NULL for top-level departments)
HeadOfDepartmentID (Foreign Key referencing Employee.EmployeeID)
OrganizationID (Foreign Key referencing Organization.OrganizationID)
Position:

PositionID (Primary Key, Auto-incrementing Integer or UUID)
Name (Text)
Description (Text)
DepartmentID (Foreign Key referencing Department.DepartmentID)
Team:

TeamID (Primary Key, Auto-incrementing Integer or UUID)
Name (Text)
Description (Text)
TeamLeaderID (Foreign Key referencing Employee.EmployeeID)
ParentTeamID (Foreign Key referencing Team.TeamID, Self-referencing for hierarchy, can be NULL for top-level teams)
OrganizationID (Foreign Key referencing Organization.OrganizationID)
Employee:

EmployeeID (Primary Key, Auto-incrementing Integer or UUID)
Name (Text)
Email (Text)
Phone (Text)
OrganizationID (Foreign Key referencing Organization.OrganizationID)
Relationships:

Organization - Department (One-to-Many):

One Organization can have many Departments.
Each Department belongs to one Organization.
Relationship Name: Has_Departments
Department - Department (One-to-Many, Self-Referencing):

One Department (parent) can have many sub-Departments.
Each sub-Department belongs to one parent Department.
Relationship Name: Parent_Of
Department - Employee (One-to-Many):

One Department can have many Employees as members.
Each Employee belongs to one Department.
Relationship name: Belongs_To_Department
Department - Employee (One-to-One):

One Department has one Employee as its head.
Each Employee can be the head of at most one Department.
Relationship Name: Heads
Employee - Position (Many-to-Many):

One Employee can hold many Positions.
One Position can be held by many Employees.
Relationship Name: Holds
Associative Entity (Junction Table): EmployeePosition
EmployeeID (Foreign Key referencing Employee.EmployeeID)
PositionID (Foreign Key referencing Position.PositionID)
StartDate (Date - optional, for tracking when the employee started in the position)
EndDate (Date - optional, for tracking when the employee ended the position)
Position - Department (Many-to-One):

One Department can have many Positions
One Position belongs to one Department
Relationship name: Belongs_To_Position
Team - Team (One-to-Many, Self-Referencing):

One Team (parent) can have many sub-Teams.
Each sub-Team belongs to one parent Team.
Relationship Name: Parent_Of
Team - Employee (One-to-Many):

One Team has one Employee as its leader.
One Employee can lead one Team.
Relationship Name: Leads
Employee - Team (Many-to-Many):

One Employee can be a member of many Teams.
One Team can have many Employees as members.
Relationship Name: Member_Of
Associative Entity (Junction Table): TeamMember
EmployeeID (Foreign Key referencing Employee.EmployeeID)
TeamID (Foreign Key referencing Team.TeamID)
JoinDate (Date - optional, for tracking when the employee joined the team)
Team - Organization (One-to-Many):

One Organization can have many Teams.
Each Team belongs to one Organization.
Relationship Name: Has_Teams
Simplified ER Diagram Conceptualization:

[Organization] 1 -- * [Department] * -- 1 [Department] (Hierarchy)
[Organization] 1 -- * [Team] * -- 1 [Team] (Hierarchy)
[Organization] 1 -- * [Employee]
[Department] 1 -- 1 [Employee] (Heads)
[Department] * -- * [Employee] (Belongs_To_Department)
[Department] * -- 1 [Position]
[Employee] * -- * [Position] (via EmployeePosition)
[Employee] * -- * [Team] (via TeamMember)
[Team] 1 -- 1 [Employee] (Leads)
Key Points:

Primary Keys: I've used ID fields (e.g., OrganizationID, DepartmentID) as primary keys. You can choose appropriate data types (e.g., auto-incrementing integers, UUIDs).
Foreign Keys: Foreign keys are used to represent the relationships between entities.
Many-to-Many Relationships: The Employee-Position and Employee-Team relationships are many-to-many, so they are implemented using associative entities (junction tables) EmployeePosition and TeamMember.
Self-Referencing Relationships: The Department-Department and Team-Team relationships are self-referencing to represent the hierarchical structure within departments and teams.
One-to-Many between Organization and Employee: This relationship ensure that every employee is associated with one organization.
This detailed entity-relationship model provides a solid foundation for designing a database to represent your organizational structure. You can use this model to create tables in a relational database system like MySQL, PostgreSQL, or SQL Server. Please let me know if you have any other questions.