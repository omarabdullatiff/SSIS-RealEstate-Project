use master

GO
IF NOT EXISTS (SELECT 1 FROM sys.databases WHERE name = 'RealEstate_Staging_DB')
BEGIN
    CREATE DATABASE RealEstate_Staging_DB;
END
GO

USE RealEstate_Staging_DB;
GO

CREATE TABLE stg_Customers (
    customer_id INT,
    full_name NVARCHAR(100),
    phone NVARCHAR(20),
    email NVARCHAR(100),
    city NVARCHAR(50),
    created_date DATETIME,
    last_updated DATETIME
);

CREATE TABLE stg_Agents (
    agent_id INT,
    agent_name NVARCHAR(100),
    phone NVARCHAR(20),
    hire_date DATE,
    created_date DATETIME,
    last_updated DATETIME
);

CREATE TABLE stg_Property_Types (
    property_type_id INT,
    type_name NVARCHAR(50)
);

CREATE TABLE stg_Properties (
    property_id INT,
    property_type_id INT,
    city NVARCHAR(50),
    price DECIMAL(12,2),
    area_sq_m INT,
    created_date DATETIME,
    last_updated DATETIME
);

CREATE TABLE stg_Transactions (
    transaction_id INT,
    property_id INT,
    customer_id INT,
    agent_id INT,
    transaction_date DATE,
    total_amount DECIMAL(12,2),
    status NVARCHAR(20),
    created_date DATETIME,
    last_updated DATETIME
);

CREATE TABLE stg_MarketingLeads (
    lead_id INT,
    linked_customer_id INT NULL,
    name NVARCHAR(100),
    email NVARCHAR(100),
    phone NVARCHAR(20),
    city NVARCHAR(50),
    lead_source NVARCHAR(50),
    created_date DATETIME
);

CREATE TABLE stg_ExternalPropertyPrices (
    external_property_id INT,
    linked_property_id INT NULL,
    city NVARCHAR(50),
    external_price DECIMAL(12,2),
    source NVARCHAR(50)
);

GO

PRINT 'All Staging Tables Created Successfully in RealEstate_Staging';
