-- Organization table
CREATE TABLE Organization (
    OrganizationID BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Address TEXT,
    Phone VARCHAR(50),
    Email VARCHAR(255),
    Website VARCHAR(255),
    TopDepartmentID BIGINT UNSIGNED,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_org_name (Name),
    INDEX idx_top_dept (TopDepartmentID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Department table
CREATE TABLE Department (
    DepartmentID BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    ParentDepartmentID BIGINT UNSIGNED,
    HeadOfDepartmentID BIGINT UNSIGNED,
    OrganizationID BIGINT UNSIGNED NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_dept_name (Name),
    INDEX idx_parent_dept (ParentDepartmentID),
    INDEX idx_head_dept (HeadOfDepartmentID),
    INDEX idx_org_dept (OrganizationID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Employee table
CREATE TABLE Employee (
    EmployeeID BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Phone VARCHAR(50),
    OrganizationID BIGINT UNSIGNED NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE INDEX idx_emp_email (Email),
    INDEX idx_emp_name (Name),
    INDEX idx_emp_org (OrganizationID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Position table
CREATE TABLE Position (
    PositionID BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    DepartmentID BIGINT UNSIGNED NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_pos_name (Name),
    INDEX idx_pos_dept (DepartmentID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Team table
CREATE TABLE Team (
    TeamID BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    TeamLeaderID BIGINT UNSIGNED,
    ParentTeamID BIGINT UNSIGNED,
    OrganizationID BIGINT UNSIGNED NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_team_name (Name),
    INDEX idx_team_leader (TeamLeaderID),
    INDEX idx_parent_team (ParentTeamID),
    INDEX idx_team_org (OrganizationID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- EmployeePosition junction table
CREATE TABLE EmployeePosition (
    EmployeeID BIGINT UNSIGNED NOT NULL,
    PositionID BIGINT UNSIGNED NOT NULL,
    StartDate DATE,
    EndDate DATE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (EmployeeID, PositionID),
    INDEX idx_emp_pos_dates (StartDate, EndDate)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TeamMember junction table
CREATE TABLE TeamMember (
    TeamID BIGINT UNSIGNED NOT NULL,
    EmployeeID BIGINT UNSIGNED NOT NULL,
    JoinDate DATE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (TeamID, EmployeeID),
    INDEX idx_team_member_date (JoinDate)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Add foreign key constraints
ALTER TABLE Organization
    ADD CONSTRAINT fk_org_top_department
    FOREIGN KEY (TopDepartmentID) REFERENCES Department(DepartmentID)
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE Department
    ADD CONSTRAINT fk_dept_parent
    FOREIGN KEY (ParentDepartmentID) REFERENCES Department(DepartmentID)
    ON DELETE SET NULL ON UPDATE CASCADE,
    ADD CONSTRAINT fk_dept_head
    FOREIGN KEY (HeadOfDepartmentID) REFERENCES Employee(EmployeeID)
    ON DELETE SET NULL ON UPDATE CASCADE,
    ADD CONSTRAINT fk_dept_org
    FOREIGN KEY (OrganizationID) REFERENCES Organization(OrganizationID)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Employee
    ADD CONSTRAINT fk_emp_org
    FOREIGN KEY (OrganizationID) REFERENCES Organization(OrganizationID)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Position
    ADD CONSTRAINT fk_pos_dept
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Team
    ADD CONSTRAINT fk_team_leader
    FOREIGN KEY (TeamLeaderID) REFERENCES Employee(EmployeeID)
    ON DELETE SET NULL ON UPDATE CASCADE,
    ADD CONSTRAINT fk_team_parent
    FOREIGN KEY (ParentTeamID) REFERENCES Team(TeamID)
    ON DELETE SET NULL ON UPDATE CASCADE,
    ADD CONSTRAINT fk_team_org
    FOREIGN KEY (OrganizationID) REFERENCES Organization(OrganizationID)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE EmployeePosition
    ADD CONSTRAINT fk_emp_pos_employee
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
    ON DELETE CASCADE ON UPDATE CASCADE,
    ADD CONSTRAINT fk_emp_pos_position
    FOREIGN KEY (PositionID) REFERENCES Position(PositionID)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE TeamMember
    ADD CONSTRAINT fk_team_member_team
    FOREIGN KEY (TeamID) REFERENCES Team(TeamID)
    ON DELETE CASCADE ON UPDATE CASCADE,
    ADD CONSTRAINT fk_team_member_employee
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
    ON DELETE CASCADE ON UPDATE CASCADE; 