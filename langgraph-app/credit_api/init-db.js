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
      customer_id TEXT NOT NULL,
      credit_score INTEGER NOT NULL,
      check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    )
  `);

  // Create kyc_checks table
  db.exec(`
    CREATE TABLE IF NOT EXISTS kyc_checks (
      check_id INTEGER PRIMARY KEY AUTOINCREMENT,
      customer_id TEXT NOT NULL,
      kyc_passed BOOLEAN NOT NULL,
      remarks TEXT,
      check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    )
  `);

  // Create income_verifications table
  db.exec(`
    CREATE TABLE IF NOT EXISTS income_verifications (
      verification_id INTEGER PRIMARY KEY AUTOINCREMENT,
      customer_id TEXT NOT NULL,
      declared_income REAL NOT NULL,
      verified_income REAL NOT NULL,
      remarks TEXT,
      status TEXT NOT NULL,
      verification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    )
  `);

  // Create background_checks table
  db.exec(`
    CREATE TABLE IF NOT EXISTS background_checks (
      check_id INTEGER PRIMARY KEY AUTOINCREMENT,
      customer_id TEXT NOT NULL,
      criminal_record BOOLEAN NOT NULL,
      debt_collections BOOLEAN NOT NULL,
      remarks TEXT,
      check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
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
    { id: 'CUST003', firstName: 'Robert', lastName: 'Johnson', email: 'robert.j@example.com', phone: '555-456-7890', address: '789 Pine Rd, Nowhere, USA', dob: '1978-11-30' },
    { id: 'CUST004', firstName: 'Emily', lastName: 'Wilson', email: 'emily.w@example.com', phone: '555-222-3333', address: '101 Elm St, Anytown, USA', dob: '1992-05-18' },
    { id: 'CUST005', firstName: 'Michael', lastName: 'Brown', email: 'michael.b@example.com', phone: '555-444-5555', address: '202 Maple Ave, Somewhere, USA', dob: '1980-09-27' }
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
    // High credit score scenario (credit_score > 700)
    { id: 'APP001', customerId: 'CUST001', productType: 'credit_card', amount: 5000 },
    // Low credit score scenario (credit_score < 600)
    { id: 'APP002', customerId: 'CUST002', productType: 'personal_loan', amount: 15000 },
    // Medium credit score + KYC failed scenario
    { id: 'APP003', customerId: 'CUST003', productType: 'mortgage', amount: 250000 },
    // Income mismatch scenario
    { id: 'APP004', customerId: 'CUST004', productType: 'personal_loan', amount: 20000 },
    // Additional application for testing
    { id: 'APP005', customerId: 'CUST005', productType: 'auto_loan', amount: 35000 }
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

  // Insert credit checks for each scenario
  const creditChecks = [
    // High credit score (> 700)
    { customerId: 'CUST001', creditScore: 780 },
    // Low credit score (< 600)
    { customerId: 'CUST002', creditScore: 520 },
    // Medium credit score (600-700)
    { customerId: 'CUST003', creditScore: 650 },
    // Income mismatch scenario
    { customerId: 'CUST004', creditScore: 680 },
    // Additional application
    { customerId: 'CUST005', creditScore: 710 }
  ];

  const insertCreditCheck = db.prepare('INSERT INTO credit_checks (customer_id, credit_score) VALUES (?, ?)');
  
  creditChecks.forEach(check => {
    insertCreditCheck.run(
      check.customerId,
      check.creditScore
    );
  });

  // Insert KYC checks
  const kycChecks = [
    // High credit score - KYC passed
    { customerId: 'CUST001', kycPassed: 1, remarks: 'All documents verified successfully.' },
    // Low credit score - KYC passed
    { customerId: 'CUST002', kycPassed: 1, remarks: 'Identity verified.' },
    // Medium credit score - KYC failed
    { customerId: 'CUST003', kycPassed: 0, remarks: 'Missing identification documents.' },
    // Income mismatch - KYC passed
    { customerId: 'CUST004', kycPassed: 1, remarks: 'All documents verified.' },
    // Additional application - KYC passed
    { customerId: 'CUST005', kycPassed: 1, remarks: 'Identity verified successfully.' }
  ];

  const insertKycCheck = db.prepare('INSERT INTO kyc_checks (customer_id, kyc_passed, remarks) VALUES (?, ?, ?)');
  
  kycChecks.forEach(check => {
    insertKycCheck.run(
      check.customerId,
      check.kycPassed,
      check.remarks
    );
  });

  // Insert income verifications
  const incomeVerifications = [
    // High credit score - Income matches
    { customerId: 'CUST001', declaredIncome: 85000, verifiedIncome: 85000, remarks: 'Income verified with pay stubs.', status: 'Completed' },
    // Low credit score - Income matches
    { customerId: 'CUST002', declaredIncome: 45000, verifiedIncome: 45000, remarks: 'Income verified with tax returns.', status: 'Completed' },
    // Medium credit score - Income matches
    { customerId: 'CUST003', declaredIncome: 120000, verifiedIncome: 120000, remarks: 'Income verified with employer.', status: 'Completed' },
    // Income mismatch scenario
    { customerId: 'CUST004', declaredIncome: 90000, verifiedIncome: 65000, remarks: 'Discrepancy found in declared income.', status: 'Mismatch' },
    // Additional application - Income matches
    { customerId: 'CUST005', declaredIncome: 75000, verifiedIncome: 75000, remarks: 'Income verified with bank statements.', status: 'Completed' }
  ];

  const insertIncomeVerification = db.prepare('INSERT INTO income_verifications (customer_id, declared_income, verified_income, remarks, status) VALUES (?, ?, ?, ?, ?)');
  
  incomeVerifications.forEach(verification => {
    insertIncomeVerification.run(
      verification.customerId,
      verification.declaredIncome,
      verification.verifiedIncome,
      verification.remarks,
      verification.status
    );
  });

  // Insert background checks for applicable scenarios
  const backgroundChecks = [
    // Low credit score - Background check
    { customerId: 'CUST002', criminalRecord: 0, debtCollections: 1, remarks: 'Has outstanding collections.' },
    // Medium credit score - Background check
    { customerId: 'CUST003', criminalRecord: 0, debtCollections: 0, remarks: 'No issues found.' },
    // Income mismatch - Background check
    { customerId: 'CUST004', criminalRecord: 0, debtCollections: 0, remarks: 'No issues found.' }
  ];

  const insertBackgroundCheck = db.prepare('INSERT INTO background_checks (customer_id, criminal_record, debt_collections, remarks) VALUES (?, ?, ?, ?)');
  
  backgroundChecks.forEach(check => {
    insertBackgroundCheck.run(
      check.customerId,
      check.criminalRecord,
      check.debtCollections,
      check.remarks
    );
  });

  // Insert manual approvals for applicable scenarios
  const manualApprovals = [
    // Medium credit score + KYC failed - Manual approval needed
    { applicationId: 'APP003', approverName: 'Jane Supervisor', approvalNotes: 'Approved with condition to provide missing documents within 30 days.', approved: 1 },
    // Income mismatch - Manual approval needed
    { applicationId: 'APP004', approverName: 'John Manager', approvalNotes: 'Approved for lower amount based on verified income.', approved: 1 }
  ];

  const insertManualApproval = db.prepare('INSERT INTO manual_approvals (application_id, approver_name, approval_notes, approved) VALUES (?, ?, ?, ?)');
  
  manualApprovals.forEach(approval => {
    insertManualApproval.run(
      approval.applicationId,
      approval.approverName,
      approval.approvalNotes,
      approval.approved
    );
  });

  // Insert final decisions
  const finalDecisions = [
    // High credit score - Approved
    { applicationId: 'APP001', decision: 'Approved', reason: 'Excellent credit score and all verifications passed.' },
    // Low credit score - Rejected
    { applicationId: 'APP002', decision: 'Rejected', reason: 'Low credit score and outstanding collections.' },
    // Medium credit score + KYC failed - Conditionally Approved
    { applicationId: 'APP003', decision: 'Conditionally Approved', reason: 'Approved pending submission of missing KYC documents.' },
    // Income mismatch - Approved with modifications
    { applicationId: 'APP004', decision: 'Approved', reason: 'Approved for reduced amount based on verified income.' },
    // Additional application - Approved
    { applicationId: 'APP005', decision: 'Approved', reason: 'Approved for good credit score and all verifications passed.' }
  ];

  const insertFinalDecision = db.prepare('INSERT INTO final_decisions (application_id, decision, reason) VALUES (?, ?, ?)');
  
  finalDecisions.forEach(decision => {
    insertFinalDecision.run(
      decision.applicationId,
      decision.decision,
      decision.reason
    );
  });

  // Update application statuses based on final decisions
  const updateApplicationStatus = db.prepare('UPDATE credit_applications SET status = ? WHERE application_id = ?');
  
  finalDecisions.forEach(decision => {
    updateApplicationStatus.run(
      decision.decision,
      decision.applicationId
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
