-- =====================================================
-- THRIFT STORE MANAGEMENT SYSTEM - DDL STATEMENTS
-- =====================================================

CREATE DATABASE MINIPROJECT_DBMS;
USE MINIPROJECT_DBMS;
SHOW DATABASES;
SHOW TABLES;

-- 1. CUSTOMER TABLE
CREATE TABLE Tb_Customer (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    CONSTRAINT chk_customer_name CHECK (LENGTH(FirstName) > 0 AND LENGTH(LastName) > 0)
);

-- 2. CUSTOMER PHONE TABLE (Multi-valued attribute)
CREATE TABLE Tb_CustomerPhone (
    CustomerID INT,
    Phone VARCHAR(15) NOT NULL,
    PRIMARY KEY (CustomerID, Phone),
    CONSTRAINT fk_custphone_customer FOREIGN KEY (CustomerID) 
        REFERENCES Tb_Customer(CustomerID) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT chk_phone_format CHECK (Phone REGEXP '^[0-9+()-]+$')
);

-- 3. CUSTOMER EMAIL TABLE (Multi-valued attribute)
CREATE TABLE Tb_CustomerEmail (
    CustomerID INT,
    Email VARCHAR(100) NOT NULL,
    PRIMARY KEY (CustomerID, Email),
    CONSTRAINT fk_custemail_customer FOREIGN KEY (CustomerID) 
        REFERENCES Tb_Customer(CustomerID) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT chk_email_format CHECK (Email LIKE '%@%.%')
);

-- 4. EMPLOYEE TABLE
CREATE TABLE Tb_Employee (
    EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Role VARCHAR(50) NOT NULL,
    Salary DECIMAL(10,2) NOT NULL,
    CONSTRAINT chk_salary CHECK (Salary > 0),
    CONSTRAINT chk_role CHECK (Role IN ('Manager', 'Cashier', 'Stock Clerk', 'Donation Handler', 'Sales Associate'))
);

-- 5. EMPLOYEE PHONE TABLE
CREATE TABLE Tb_EmployeePhone (
    EmployeeID INT,
    Phone VARCHAR(15) NOT NULL,
    PRIMARY KEY (EmployeeID, Phone),
    CONSTRAINT fk_empphone_employee FOREIGN KEY (EmployeeID) 
        REFERENCES Tb_Employee(EmployeeID) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT chk_emp_phone_format CHECK (Phone REGEXP '^[0-9+()-]+$')
);

-- 6. EMPLOYEE EMAIL TABLE
CREATE TABLE Tb_EmployeeEmail (
    EmployeeID INT,
    Email VARCHAR(100) NOT NULL,
    PRIMARY KEY (EmployeeID, Email),
    CONSTRAINT fk_empemail_employee FOREIGN KEY (EmployeeID) 
        REFERENCES Tb_Employee(EmployeeID) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT chk_emp_email_format CHECK (Email LIKE '%@%.%')
);

-- 7. SUPPLIER TABLE
CREATE TABLE Tb_Supplier (
    SupplierID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    CONSTRAINT chk_supplier_name CHECK (LENGTH(FirstName) > 0 AND LENGTH(LastName) > 0)
);

-- 8. SUPPLIER PHONE TABLE
CREATE TABLE Tb_SupplierPhone (
    SupplierID INT,
    Phone VARCHAR(15) NOT NULL,
    PRIMARY KEY (SupplierID, Phone),
    CONSTRAINT fk_suppphone_supplier FOREIGN KEY (SupplierID) 
        REFERENCES Tb_Supplier(SupplierID) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT chk_supp_phone_format CHECK (Phone REGEXP '^[0-9+()-]+$')
);

-- 9. SUPPLIER EMAIL TABLE
CREATE TABLE Tb_SupplierEmail (
    SupplierID INT,
    Email VARCHAR(100) NOT NULL,
    PRIMARY KEY (SupplierID, Email),
    CONSTRAINT fk_suppemail_supplier FOREIGN KEY (SupplierID) 
        REFERENCES Tb_Supplier(SupplierID) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT chk_supp_email_format CHECK (Email LIKE '%@%.%')
);

-- 10. DONOR TABLE
CREATE TABLE Tb_Donor (
    DonorID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    CONSTRAINT chk_donor_name CHECK (LENGTH(FirstName) > 0 AND LENGTH(LastName) > 0)
);

-- 11. DONOR PHONE TABLE
CREATE TABLE Tb_DonorPhone (
    DonorID INT,
    Phone VARCHAR(15) NOT NULL,
    PRIMARY KEY (DonorID, Phone),
    CONSTRAINT fk_donorphone_donor FOREIGN KEY (DonorID) 
        REFERENCES Tb_Donor(DonorID) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT chk_donor_phone_format CHECK (Phone REGEXP '^[0-9+()-]+$')
);

-- 12. CATEGORY TABLE
CREATE TABLE Tb_Category (
    CategoryID INT PRIMARY KEY AUTO_INCREMENT,
    CategoryName VARCHAR(50) NOT NULL UNIQUE,
    Description TEXT,
    CONSTRAINT chk_category_name CHECK (LENGTH(CategoryName) > 0)
);

SHOW TABLES;

-- 13. ITEM TABLE
CREATE TABLE Tb_Item (
    ItemID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    `Condition` ENUM('New', 'Like New', 'Good', 'Fair', 'Poor') NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    CategoryID INT NOT NULL,
    SupplierID INT,
    CONSTRAINT fk_item_category FOREIGN KEY (CategoryID) 
        REFERENCES Tb_Category(CategoryID) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    CONSTRAINT fk_item_supplier FOREIGN KEY (SupplierID) 
        REFERENCES Tb_Supplier(SupplierID) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
    CONSTRAINT chk_price CHECK (Price >= 0),
    CONSTRAINT chk_item_name CHECK (LENGTH(Name) > 0)
);

-- 14. INVENTORY TABLE
CREATE TABLE Tb_Inventory (
    InventoryID INT PRIMARY KEY AUTO_INCREMENT,
    ItemID INT NOT NULL,
    QuantityAvailable INT NOT NULL DEFAULT 0,
    Location VARCHAR(100) NOT NULL,
    CONSTRAINT fk_inventory_item FOREIGN KEY (ItemID) 
        REFERENCES Tb_Item(ItemID) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT chk_quantity CHECK (QuantityAvailable >= 0),
    CONSTRAINT chk_location CHECK (LENGTH(Location) > 0),
    CONSTRAINT uq_item_location UNIQUE (ItemID, Location)
);

-- 15. DONATION TABLE
CREATE TABLE Tb_Donation (
    DonationID INT PRIMARY KEY AUTO_INCREMENT,
    DD INT NOT NULL,
    MM INT NOT NULL,
    YY INT NOT NULL,
    EstimatedValue DECIMAL(10,2),
    EmployeeID INT NOT NULL,
    DonorID INT NOT NULL,
    CONSTRAINT fk_donation_employee FOREIGN KEY (EmployeeID) 
        REFERENCES Tb_Employee(EmployeeID) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    CONSTRAINT fk_donation_donor FOREIGN KEY (DonorID) 
        REFERENCES Tb_Donor(DonorID) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    CONSTRAINT chk_donation_date CHECK (DD BETWEEN 1 AND 31 AND MM BETWEEN 1 AND 12 AND YY > 1900),
    CONSTRAINT chk_estimated_value CHECK (EstimatedValue >= 0)
);

-- 16. TRANSACTION TABLE
CREATE TABLE Tb_Transaction (
    TransactionID INT PRIMARY KEY AUTO_INCREMENT,
    DD INT NOT NULL,
    MM INT NOT NULL,
    YY INT NOT NULL,
    TotalAmount DECIMAL(10,2) NOT NULL,
    PaymentMode ENUM('Cash', 'Card', 'UPI', 'Check') NOT NULL,
    CustomerID INT NOT NULL,
    EmployeeID INT NOT NULL,
    CONSTRAINT fk_transaction_customer FOREIGN KEY (CustomerID) 
        REFERENCES Tb_Customer(CustomerID) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    CONSTRAINT fk_transaction_employee FOREIGN KEY (EmployeeID) 
        REFERENCES Tb_Employee(EmployeeID) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    CONSTRAINT chk_transaction_date CHECK (DD BETWEEN 1 AND 31 AND MM BETWEEN 1 AND 12 AND YY > 1900),
    CONSTRAINT chk_total_amount CHECK (TotalAmount >= 0)
);

-- 17. TRANSACTION ITEM TABLE (Weak Entity - Bridge Table)
CREATE TABLE Tb_TransactionItem (
    TransactionID INT,
    LineNumber INT,  -- Discriminator attribute (partial key)
    ItemID INT NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,
    LineTotal DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (TransactionID, LineNumber),  -- Composite key: owner PK + discriminator
    CONSTRAINT fk_transitem_transaction FOREIGN KEY (TransactionID) 
        REFERENCES Tb_Transaction(TransactionID) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT fk_transitem_item FOREIGN KEY (ItemID) 
        REFERENCES Tb_Item(ItemID) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    CONSTRAINT chk_quantity_positive CHECK (Quantity > 0),
    CONSTRAINT chk_unitprice CHECK (UnitPrice >= 0),
    CONSTRAINT chk_linetotal CHECK (LineTotal >= 0),
    CONSTRAINT chk_linenumber CHECK (LineNumber > 0)
);

-- 18. CREATE INDEXES for Performance Optimization
CREATE INDEX idx_customer_name ON Tb_Customer(LastName, FirstName);
CREATE INDEX idx_employee_role ON Tb_Employee(Role);
CREATE INDEX idx_item_category ON Tb_Item(CategoryID);
CREATE INDEX idx_item_price ON Tb_Item(Price);
CREATE INDEX idx_transaction_date ON Tb_Transaction(YY, MM, DD);
CREATE INDEX idx_donation_date ON Tb_Donation(YY, MM, DD);
CREATE INDEX idx_inventory_item ON Tb_Inventory(ItemID);

-- =====================================================
-- PART 1: FUNCTIONS
-- =====================================================

-- Function 1: Calculate total sales for a specific customer
DELIMITER //
CREATE FUNCTION fn_CustomerTotalPurchases(cust_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total DECIMAL(10,2);
    SELECT COALESCE(SUM(TotalAmount), 0) INTO total
    FROM Tb_Transaction
    WHERE CustomerID = cust_id;
    RETURN total;
END //
DELIMITER ;

-- Function 2: Get inventory value for a specific category
DELIMITER //
CREATE FUNCTION fn_CategoryInventoryValue(cat_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total_value DECIMAL(10,2);
    SELECT COALESCE(SUM(i.Price * inv.QuantityAvailable), 0) INTO total_value
    FROM Tb_Item i
    JOIN Tb_Inventory inv ON i.ItemID = inv.ItemID
    WHERE i.CategoryID = cat_id;
    RETURN total_value;
END //
DELIMITER ;

-- Function 3: Calculate employee's total transaction amount processed
DELIMITER //
CREATE FUNCTION fn_EmployeeSalesTotal(emp_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total DECIMAL(10,2);
    SELECT COALESCE(SUM(TotalAmount), 0) INTO total
    FROM Tb_Transaction
    WHERE EmployeeID = emp_id;
    RETURN total;
END //
DELIMITER ;

-- Function 4: Get donor's total donation value
DELIMITER //
CREATE FUNCTION fn_DonorTotalValue(donor_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total DECIMAL(10,2);
    SELECT COALESCE(SUM(EstimatedValue), 0) INTO total
    FROM Tb_Donation
    WHERE DonorID = donor_id;
    RETURN total;
END //
DELIMITER ;

-- Function 5: Calculate average item price in a category
DELIMITER //
CREATE FUNCTION fn_CategoryAvgPrice(cat_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE avg_price DECIMAL(10,2);
    SELECT COALESCE(AVG(Price), 0) INTO avg_price
    FROM Tb_Item
    WHERE CategoryID = cat_id;
    RETURN avg_price;
END //
DELIMITER ;

-- Function 6: Count items by condition
DELIMITER //
CREATE FUNCTION fn_CountItemsByCondition(item_condition VARCHAR(20))
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE item_count INT;
    SELECT COUNT(*) INTO item_count
    FROM Tb_Item
    WHERE `Condition` = item_condition;
    RETURN item_count;
END //
DELIMITER ;

-- =====================================================
-- PART 2: STORED PROCEDURES
-- =====================================================

-- Procedure 1: Add new customer with phone and email
DELIMITER //
CREATE PROCEDURE sp_AddCustomer(
    IN p_FirstName VARCHAR(50),
    IN p_LastName VARCHAR(50),
    IN p_Phone VARCHAR(15),
    IN p_Email VARCHAR(100)
)
BEGIN
    DECLARE new_cust_id INT;
    
    INSERT INTO Tb_Customer (FirstName, LastName)
    VALUES (p_FirstName, p_LastName);
    
    SET new_cust_id = LAST_INSERT_ID();
    
    INSERT INTO Tb_CustomerPhone (CustomerID, Phone)
    VALUES (new_cust_id, p_Phone);
    
    INSERT INTO Tb_CustomerEmail (CustomerID, Email)
    VALUES (new_cust_id, p_Email);
    
    SELECT new_cust_id AS CustomerID, 'Customer added successfully' AS Message;
END //
DELIMITER ;

-- Procedure 2: Process a new transaction
DELIMITER //
CREATE PROCEDURE sp_ProcessTransaction(
    IN p_CustomerID INT,
    IN p_EmployeeID INT,
    IN p_PaymentMode VARCHAR(10),
    IN p_DD INT,
    IN p_MM INT,
    IN p_YY INT
)
BEGIN
    DECLARE new_trans_id INT;
    
    INSERT INTO Tb_Transaction (DD, MM, YY, TotalAmount, PaymentMode, CustomerID, EmployeeID)
    VALUES (p_DD, p_MM, p_YY, 0.00, p_PaymentMode, p_CustomerID, p_EmployeeID);
    
    SET new_trans_id = LAST_INSERT_ID();
    
    SELECT new_trans_id AS TransactionID, 'Transaction created. Add items using sp_AddTransactionItem' AS Message;
END //
DELIMITER ;

-- Procedure 3: Add item to transaction and update inventory
DELIMITER //
CREATE PROCEDURE sp_AddTransactionItem(
    IN p_TransactionID INT,
    IN p_ItemID INT,
    IN p_Quantity INT
)
BEGIN
    DECLARE item_price DECIMAL(10,2);
    DECLARE line_total DECIMAL(10,2);
    DECLARE available_qty INT;
    
    -- Get item price
    SELECT Price INTO item_price FROM Tb_Item WHERE ItemID = p_ItemID;
    
    -- Check inventory
    SELECT QuantityAvailable INTO available_qty 
    FROM Tb_Inventory 
    WHERE ItemID = p_ItemID 
    LIMIT 1;
    
    IF available_qty < p_Quantity THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Insufficient inventory';
    END IF;
    
    -- Calculate line total
    SET line_total = item_price * p_Quantity;
    
    -- Add transaction item
    INSERT INTO Tb_TransactionItem (TransactionID, ItemID, Quantity, UnitPrice, LineTotal)
    VALUES (p_TransactionID, p_ItemID, p_Quantity, item_price, line_total);
    
    -- Update transaction total
    UPDATE Tb_Transaction
    SET TotalAmount = TotalAmount + line_total
    WHERE TransactionID = p_TransactionID;
    
    -- Update inventory
    UPDATE Tb_Inventory
    SET QuantityAvailable = QuantityAvailable - p_Quantity
    WHERE ItemID = p_ItemID;
    
    SELECT 'Item added to transaction successfully' AS Message;
END //
DELIMITER ;

-- Procedure 4: Generate sales report for a date range
DELIMITER //
CREATE PROCEDURE sp_SalesReport(
    IN p_StartYear INT,
    IN p_StartMonth INT,
    IN p_EndYear INT,
    IN p_EndMonth INT
)
BEGIN
    SELECT 
        t.TransactionID,
        CONCAT(c.FirstName, ' ', c.LastName) AS Customer,
        CONCAT(e.FirstName, ' ', e.LastName) AS Employee,
        CONCAT(t.DD, '-', t.MM, '-', t.YY) AS TransactionDate,
        t.TotalAmount,
        t.PaymentMode
    FROM Tb_Transaction t
    JOIN Tb_Customer c ON t.CustomerID = c.CustomerID
    JOIN Tb_Employee e ON t.EmployeeID = e.EmployeeID
    WHERE (t.YY > p_StartYear OR (t.YY = p_StartYear AND t.MM >= p_StartMonth))
      AND (t.YY < p_EndYear OR (t.YY = p_EndYear AND t.MM <= p_EndMonth))
    ORDER BY t.YY, t.MM, t.DD;
END //
DELIMITER ;

-- Procedure 5: Get low stock items
DELIMITER //
CREATE PROCEDURE sp_LowStockAlert(IN p_Threshold INT)
BEGIN
    SELECT 
        i.ItemID,
        i.Name,
        cat.CategoryName,
        inv.QuantityAvailable,
        inv.Location
    FROM Tb_Item i
    JOIN Tb_Category cat ON i.CategoryID = cat.CategoryID
    JOIN Tb_Inventory inv ON i.ItemID = inv.ItemID
    WHERE inv.QuantityAvailable <= p_Threshold
    ORDER BY inv.QuantityAvailable ASC;
END //
DELIMITER ;

-- Procedure 6: Add new donation
DELIMITER //
CREATE PROCEDURE sp_AddDonation(
    IN p_DonorID INT,
    IN p_EmployeeID INT,
    IN p_EstimatedValue DECIMAL(10,2),
    IN p_DD INT,
    IN p_MM INT,
    IN p_YY INT
)
BEGIN
    INSERT INTO Tb_Donation (DD, MM, YY, EstimatedValue, EmployeeID, DonorID)
    VALUES (p_DD, p_MM, p_YY, p_EstimatedValue, p_EmployeeID, p_DonorID);
    
    SELECT LAST_INSERT_ID() AS DonationID, 'Donation recorded successfully' AS Message;
END //
DELIMITER ;

-- Procedure 7: Update item price
DELIMITER //
CREATE PROCEDURE sp_UpdateItemPrice(
    IN p_ItemID INT,
    IN p_NewPrice DECIMAL(10,2)
)
BEGIN
    UPDATE Tb_Item
    SET Price = p_NewPrice
    WHERE ItemID = p_ItemID;
    
    SELECT 'Item price updated successfully' AS Message;
END //
DELIMITER ;

-- Procedure 8: Get customer purchase history
DELIMITER //
CREATE PROCEDURE sp_CustomerPurchaseHistory(IN p_CustomerID INT)
BEGIN
    SELECT 
        t.TransactionID,
        CONCAT(t.DD, '-', t.MM, '-', t.YY) AS TransactionDate,
        t.TotalAmount,
        t.PaymentMode,
        GROUP_CONCAT(CONCAT(i.Name, ' (', ti.Quantity, ')') SEPARATOR ', ') AS Items
    FROM Tb_Transaction t
    JOIN Tb_TransactionItem ti ON t.TransactionID = ti.TransactionID
    JOIN Tb_Item i ON ti.ItemID = i.ItemID
    WHERE t.CustomerID = p_CustomerID
    GROUP BY t.TransactionID
    ORDER BY t.YY DESC, t.MM DESC, t.DD DESC;
END //
DELIMITER ;

-- =====================================================
-- PART 3: TRIGGERS
-- =====================================================

-- Trigger 1: Validate transaction date before insert
DELIMITER //
CREATE TRIGGER tr_ValidateTransactionDate
BEFORE INSERT ON Tb_Transaction
FOR EACH ROW
BEGIN
    IF NEW.MM = 2 AND NEW.DD > 29 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid date for February';
    END IF;
    
    IF NEW.MM IN (4, 6, 9, 11) AND NEW.DD > 30 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid date for this month';
    END IF;
END //
DELIMITER ;

-- Trigger 2: Prevent deletion of category with items
DELIMITER //
CREATE TRIGGER tr_PreventCategoryDelete
BEFORE DELETE ON Tb_Category
FOR EACH ROW
BEGIN
    DECLARE item_count INT;
    SELECT COUNT(*) INTO item_count
    FROM Tb_Item
    WHERE CategoryID = OLD.CategoryID;
    
    IF item_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete category with existing items';
    END IF;
END //
DELIMITER ;

-- Trigger 3: Auto-update transaction total when item is added
DELIMITER //
CREATE TRIGGER tr_UpdateTransactionTotal
AFTER INSERT ON Tb_TransactionItem
FOR EACH ROW
BEGIN
    UPDATE Tb_Transaction
    SET TotalAmount = (
        SELECT SUM(LineTotal)
        FROM Tb_TransactionItem
        WHERE TransactionID = NEW.TransactionID
    )
    WHERE TransactionID = NEW.TransactionID;
END //
DELIMITER ;

-- Trigger 4: Log inventory changes
CREATE TABLE IF NOT EXISTS Tb_InventoryLog (
    LogID INT PRIMARY KEY AUTO_INCREMENT,
    ItemID INT,
    OldQuantity INT,
    NewQuantity INT,
    ChangeDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ChangeType VARCHAR(20)
);

DELIMITER //
CREATE TRIGGER tr_LogInventoryUpdate
AFTER UPDATE ON Tb_Inventory
FOR EACH ROW
BEGIN
    INSERT INTO Tb_InventoryLog (ItemID, OldQuantity, NewQuantity, ChangeType)
    VALUES (NEW.ItemID, OLD.QuantityAvailable, NEW.QuantityAvailable, 'UPDATE');
END //
DELIMITER ;

-- Trigger 5: Prevent negative inventory
DELIMITER //
CREATE TRIGGER tr_PreventNegativeInventory
BEFORE UPDATE ON Tb_Inventory
FOR EACH ROW
BEGIN
    IF NEW.QuantityAvailable < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Inventory cannot be negative';
    END IF;
END //
DELIMITER ;

-- Trigger 6: Validate donation date
DELIMITER //
CREATE TRIGGER tr_ValidateDonationDate
BEFORE INSERT ON Tb_Donation
FOR EACH ROW
BEGIN
    IF NEW.MM = 2 AND NEW.DD > 29 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid donation date for February';
    END IF;
    
    IF NEW.MM IN (4, 6, 9, 11) AND NEW.DD > 30 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid donation date for this month';
    END IF;
END //
DELIMITER ;

-- =====================================================
-- TESTING & DEMONSTRATION QUERIES
-- =====================================================

-- Test Functions
SELECT fn_CustomerTotalPurchases(1) AS 'Customer 1 Total Purchases';
SELECT fn_CategoryInventoryValue(1) AS 'Clothing Category Value';
SELECT fn_EmployeeSalesTotal(2) AS 'Employee 2 Sales Total';
SELECT fn_DonorTotalValue(1) AS 'Donor 1 Total Donations';
SELECT fn_CategoryAvgPrice(1) AS 'Clothing Avg Price';
SELECT fn_CountItemsByCondition('Good') AS 'Items in Good Condition';

-- Test Procedures
CALL sp_AddCustomer('Test', 'User', '9999999999', 'test@email.com');
CALL sp_LowStockAlert(5);
CALL sp_SalesReport(2024, 9, 2024, 10);
CALL sp_CustomerPurchaseHistory(1);

-- View trigger effects
SELECT * FROM Tb_InventoryLog;

-- =====================================================
-- DROP STATEMENTS (for cleanup/reset if needed)
-- =====================================================

/*
-- Drop Functions
DROP FUNCTION IF EXISTS fn_CustomerTotalPurchases;
DROP FUNCTION IF EXISTS fn_CategoryInventoryValue;
DROP FUNCTION IF EXISTS fn_EmployeeSalesTotal;
DROP FUNCTION IF EXISTS fn_DonorTotalValue;
DROP FUNCTION IF EXISTS fn_CategoryAvgPrice;
DROP FUNCTION IF EXISTS fn_CountItemsByCondition;

-- Drop Procedures
DROP PROCEDURE IF EXISTS sp_AddCustomer;
DROP PROCEDURE IF EXISTS sp_ProcessTransaction;
DROP PROCEDURE IF EXISTS sp_AddTransactionItem;
DROP PROCEDURE IF EXISTS sp_SalesReport;
DROP PROCEDURE IF EXISTS sp_LowStockAlert;
DROP PROCEDURE IF EXISTS sp_AddDonation;
DROP PROCEDURE IF EXISTS sp_UpdateItemPrice;
DROP PROCEDURE IF EXISTS sp_CustomerPurchaseHistory;

-- Drop Triggers
DROP TRIGGER IF EXISTS tr_ValidateTransactionDate;
DROP TRIGGER IF EXISTS tr_PreventCategoryDelete;
DROP TRIGGER IF EXISTS tr_UpdateTransactionTotal;
DROP TRIGGER IF EXISTS tr_LogInventoryUpdate;
DROP TRIGGER IF EXISTS tr_PreventNegativeInventory;
DROP TRIGGER IF EXISTS tr_ValidateDonationDate;

-- Drop Log Table
DROP TABLE IF EXISTS Tb_InventoryLog;
*/
