const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

// Database path
const dbPath = path.join(__dirname, 'credit_demo.sqlite');

// Check if database file exists
const dbExists = fs.existsSync(dbPath);

// Create or open the database
const db = new Database(dbPath, { verbose: console.log });

// Initialize tables if they don't exist
function initializeDatabase() {
  console.log('Initializing database...');

  // Create customers table
  db.exec(`
    CREATE TABLE IF NOT EXISTS customers (
      customer_id TEXT PRIMARY KEY,
      first_name TEXT NOT NULL,
      last_name TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL,
      phone TEXT,
      address TEXT,
      date_of_birth TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Create credit_applications table
  db.exec(`
    CREATE TABLE IF NOT EXISTS credit_applications (
      application_id TEXT PRIMARY KEY,
      customer_id TEXT NOT NULL,
      product_type TEXT NOT NULL,
      requested_amount REAL NOT NULL,
      status TEXT DEFAULT 'Pending',
      application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    )
  `);

  // Create credit_checks table
  db.exec(`
    CREATE TABLE IF NOT EXISTS credit_checks (
      check_id INTEGER PRIMARY KEY AUTOINCREMENT,
      application_id TEXT NOT NULL,
      credit_score INTEGER NOT NULL,
      check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (application_id) REFERENCES credit_applications (application_id)
    )
  `);

  // Create kyc_checks table
  db.exec(`
    CREATE TABLE IF NOT EXISTS kyc_checks (
      check_id INTEGER PRIMARY KEY AUTOINCREMENT,
      application_id TEXT NOT NULL,
      kyc_passed BOOLEAN NOT NULL,
      remarks TEXT,
      check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (application_id) REFERENCES credit_applications (application_id)
    )
  `);

  // Create income_verifications table
  db.exec(`
    CREATE TABLE IF NOT EXISTS income_verifications (
      verification_id INTEGER PRIMARY KEY AUTOINCREMENT,
      application_id TEXT NOT NULL,
      declared_income REAL NOT NULL,
      verified_income REAL NOT NULL,
      remarks TEXT,
      status TEXT NOT NULL,
      verification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (application_id) REFERENCES credit_applications (application_id)
    )
  `);

  // Create background_checks table
  db.exec(`
    CREATE TABLE IF NOT EXISTS background_checks (
      check_id INTEGER PRIMARY KEY AUTOINCREMENT,
      application_id TEXT NOT NULL,
      criminal_record BOOLEAN NOT NULL,
      debt_collections BOOLEAN NOT NULL,
      remarks TEXT,
      check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (application_id) REFERENCES credit_applications (application_id)
    )
  `);

  // Create manual_approvals table
  db.exec(`
    CREATE TABLE IF NOT EXISTS manual_approvals (
      approval_id INTEGER PRIMARY KEY AUTOINCREMENT,
      application_id TEXT NOT NULL,
      approver_name TEXT NOT NULL,
      approval_notes TEXT,
      approved BOOLEAN NOT NULL,
      approval_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (application_id) REFERENCES credit_applications (application_id)
    )
  `);

  // Create final_decisions table
  db.exec(`
    CREATE TABLE IF NOT EXISTS final_decisions (
      decision_id INTEGER PRIMARY KEY AUTOINCREMENT,
      application_id TEXT NOT NULL,
      decision TEXT NOT NULL,
      reason TEXT,
      decision_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (application_id) REFERENCES credit_applications (application_id)
    )
  `);

  console.log('Database initialization complete!');
}

// Insert sample data if the database was just created
function insertSampleData() {
  if (dbExists) {
    console.log('Database already exists, skipping sample data insertion.');
    return;
  }

  console.log('Inserting sample data...');

  // Insert sample customers
  const customers = [
    { id: 'CUST001', firstName: 'John', lastName: 'Doe', email: 'john.doe@example.com', phone: '555-123-4567', address: '123 Main St, Anytown, USA', dob: '1985-06-15' },
    { id: 'CUST002', firstName: 'Jane', lastName: 'Smith', email: 'jane.smith@example.com', phone: '555-987-6543', address: '456 Oak Ave, Somewhere, USA', dob: '1990-03-22' },
    { id: 'CUST003', firstName: 'Robert', lastName: 'Johnson', email: 'robert.j@example.com', phone: '555-456-7890', address: '789 Pine Rd, Nowhere, USA', dob: '1978-11-30' }
  ];

  const insertCustomer = db.prepare('INSERT INTO customers (customer_id, first_name, last_name, email, phone, address, date_of_birth) VALUES (?, ?, ?, ?, ?, ?, ?)');
  
  customers.forEach(customer => {
    insertCustomer.run(
      customer.id,
      customer.firstName,
      customer.lastName,
      customer.email,
      customer.phone,
      customer.address,
      customer.dob
    );
  });

  // Insert sample applications
  const applications = [
    { id: 'APP001', customerId: 'CUST001', productType: 'credit_card', amount: 5000 },
    { id: 'APP002', customerId: 'CUST002', productType: 'personal_loan', amount: 15000 },
    { id: 'APP003', customerId: 'CUST003', productType: 'mortgage', amount: 250000 }
  ];

  const insertApplication = db.prepare('INSERT INTO credit_applications (application_id, customer_id, product_type, requested_amount) VALUES (?, ?, ?, ?)');
  
  applications.forEach(app => {
    insertApplication.run(
      app.id,
      app.customerId,
      app.productType,
      app.amount
    );
  });

  console.log('Sample data insertion complete!');
}

// Run initialization
initializeDatabase();
insertSampleData();

// Close the database connection
db.close();

console.log('Database setup complete!');
