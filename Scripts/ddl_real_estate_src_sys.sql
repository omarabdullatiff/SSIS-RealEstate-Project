use master ;

IF NOT EXISTS (
    SELECT 1
    FROM sys.databases
    WHERE name = 'real_estate_oltp_src_sys'
)
BEGIN
    CREATE DATABASE real_estate_src_sys;
END

Go
use real_estate_oltp_src_sys
GO

CREATE TABLE Customers (
    customer_id INT IDENTITY PRIMARY KEY,
    full_name NVARCHAR(100),
    phone NVARCHAR(20),
    email NVARCHAR(100),
    city NVARCHAR(50),
    created_date DATETIME DEFAULT GETDATE(),
    last_updated DATETIME
);

CREATE TABLE Agents (
    agent_id INT IDENTITY PRIMARY KEY,
    agent_name NVARCHAR(100),
    phone NVARCHAR(20),
    hire_date DATE,
    created_date DATETIME DEFAULT GETDATE(),
    last_updated DATETIME
);

CREATE TABLE Property_Types (
    property_type_id INT IDENTITY PRIMARY KEY,
    type_name NVARCHAR(50)
);

CREATE TABLE Properties (
    property_id INT IDENTITY PRIMARY KEY,
    property_type_id INT,
    city NVARCHAR(50),
    price DECIMAL(12,2),
    area_sq_m INT,
    created_date DATETIME DEFAULT GETDATE(),
    last_updated DATETIME,
    CONSTRAINT fk_property_type
        FOREIGN KEY (property_type_id) REFERENCES Property_Types(property_type_id)
);

CREATE TABLE Transactions (
    transaction_id INT IDENTITY PRIMARY KEY,
    property_id INT,
    customer_id INT,
    agent_id INT,
    transaction_date DATE,
    total_amount DECIMAL(12,2),
    status NVARCHAR(20),
    created_date DATETIME DEFAULT GETDATE(),
    last_updated DATETIME,
    CONSTRAINT fk_trans_property FOREIGN KEY (property_id) REFERENCES Properties(property_id),
    CONSTRAINT fk_trans_customer FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    CONSTRAINT fk_trans_agent FOREIGN KEY (agent_id) REFERENCES Agents(agent_id)
);
