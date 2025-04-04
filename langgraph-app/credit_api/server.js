const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const Database = require('better-sqlite3');
const path = require('path');

// Initialize the app
const api = express();
const PORT = process.env.PORT || 3000;

// Middleware
api.use(cors());
api.use(express.json());
api.use(morgan('dev'));

// Database connection
const dbPath = path.join(__dirname, 'credit_demo.sqlite');
const db = new Database(dbPath, { verbose: console.log });

// Create a middleware to inject the database connection
api.use((req, res, next) => {
  req.db = {
    query: (sql, ...params) => {
      try {
        const stmt = db.prepare(sql);
        if (sql.trim().toUpperCase().startsWith('SELECT')) {
          return stmt.all(...params);
        } else {
          return stmt.run(...params);
        }
      } catch (error) {
        console.error('Database error:', error);
        throw error;
      }
    }
  };
  next();
});

// Routes

// Customers APIs
api.get('/customers', (req, res) => {
  const customers = req.db.query('SELECT * FROM customers LIMIT 10');
  res.json(customers);
});

api.get('/customer', (req, res) => {
  const { id } = req.query;
  const customer = req.db.query('SELECT * FROM customers WHERE customer_id = ?', id)[0];

  if (customer) res.json(customer);
  else res.status(404).json({ message: 'Customer Not Found' });
});

// Credit Applications APIs
api.get('/applications', (req, res) => {
  const applications = req.db.query('SELECT * FROM credit_applications ORDER BY application_date DESC LIMIT 10');
  res.json(applications);
});

api.get('/application', (req, res) => {
  const { id } = req.query;
  const application = req.db.query('SELECT * FROM credit_applications WHERE application_id = ?', id)[0];

  if (application) res.json(application);
  else res.status(404).json({ message: 'Application Not Found' });
});

api.post('/applications', (req, res) => {
  const { customer_id, product_type, requested_amount } = req.body;
  const result = req.db.query('INSERT INTO credit_applications (customer_id, product_type, requested_amount) VALUES (?, ?, ?) RETURNING *', customer_id, product_type, requested_amount);
  res.json(result[0]);
});

// Credit Checks APIs
api.get('/credit-check', (req, res) => {
  const { customer_id } = req.query;
  const check = req.db.query('SELECT * FROM credit_checks WHERE customer_id = ?', customer_id)[0];

  if (check) res.json(check);
  else res.status(404).json({ message: 'Credit Check Not Found' });
});

api.post('/credit-check', (req, res) => {
  const { customer_id, credit_score } = req.body;
  const result = req.db.query('INSERT INTO credit_checks (customer_id, credit_score) VALUES (?, ?) RETURNING *', customer_id, credit_score);
  res.json(result[0]);
});

// KYC Checks APIs
api.get('/kyc-check', (req, res) => {
  const { customer_id } = req.query;
  const check = req.db.query('SELECT * FROM kyc_checks WHERE customer_id = ?', customer_id)[0];

  if (check) res.json(check);
  else res.status(404).json({ message: 'KYC Check Not Found' });
});

api.post('/kyc-check', (req, res) => {
  const { customer_id, kyc_passed, remarks } = req.body;
  const result = req.db.query('INSERT INTO kyc_checks (customer_id, kyc_passed, remarks) VALUES (?, ?, ?) RETURNING *', customer_id, kyc_passed, remarks);
  res.json(result[0]);
});

// Income Verification APIs
api.get('/income-verification', (req, res) => {
  const { customer_id } = req.query;
  const income = req.db.query('SELECT * FROM income_verifications WHERE customer_id = ?', customer_id)[0];

  if (income) res.json(income);
  else res.status(404).json({ message: 'Income Verification Not Found' });
});

api.post('/income-verification', (req, res) => {
  const { customer_id, declared_income, verified_income, remarks } = req.body;
  const status = declared_income === verified_income ? 'Completed' : 'Mismatch';
  const result = req.db.query('INSERT INTO income_verifications (customer_id, declared_income, verified_income, remarks, status) VALUES (?, ?, ?, ?, ?) RETURNING *', customer_id, declared_income, verified_income, remarks, status);
  res.json(result[0]);
});

// Background Checks APIs
api.get('/background-check', (req, res) => {
  const { customer_id } = req.query;
  const check = req.db.query('SELECT * FROM background_checks WHERE customer_id = ?', customer_id)[0];

  if (check) res.json(check);
  else res.status(404).json({ message: 'Background Check Not Found' });
});

api.post('/background-check', (req, res) => {
  const { customer_id, criminal_record, debt_collections, remarks } = req.body;
  const result = req.db.query('INSERT INTO background_checks (customer_id, criminal_record, debt_collections, remarks) VALUES (?, ?, ?, ?) RETURNING *', customer_id, criminal_record, debt_collections, remarks);
  res.json(result[0]);
});

// Manual Approval APIs
api.get('/manual-approval', (req, res) => {
  const { application_id } = req.query;
  const approval = req.db.query('SELECT * FROM manual_approvals WHERE application_id = ?', application_id)[0];

  if (approval) res.json(approval);
  else res.status(404).json({ message: 'Manual Approval Not Found' });
});

api.post('/manual-approval', (req, res) => {
  const { application_id, approver_name, approval_notes, approved } = req.body;
  const result = req.db.query('INSERT INTO manual_approvals (application_id, approver_name, approval_notes, approved) VALUES (?, ?, ?, ?) RETURNING *', application_id, approver_name, approval_notes, approved);
  const approval = req.db.query('SELECT * FROM manual_approvals WHERE application_id = ? order by approval_date desc limit 1', application_id)[0];

  if (approval) res.json(approval);
  else res.status(404).json({ message: 'Manual Approval Not Found' });
});

// Final Decision APIs
api.get('/final-decision', (req, res) => {
  const { application_id } = req.query;
  const decision = req.db.query('SELECT * FROM final_decisions WHERE application_id = ?', application_id)[0];

  if (decision) res.json(decision);
  else res.status(404).json({ message: 'Final Decision Not Found' });
});

api.post('/final-decision', (req, res) => {
  const { application_id, decision, reason } = req.body;
  const result = req.db.query('INSERT INTO final_decisions (application_id, decision, reason) VALUES (?, ?, ?) RETURNING *', application_id, decision, reason);

  req.db.query('UPDATE credit_applications SET status = ? WHERE application_id = ?', decision, application_id);
  updatedDecision = req.db.query('SELECT * FROM final_decisions WHERE application_id = ?', application_id)[0];
  if (updatedDecision) res.json(updatedDecision);
  else res.status(404).json({ message: 'Final Decision Not Found' });
});


// Health check endpoint
api.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'Credit Approval API is running' });
});

// Start the server
api.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('Closing database connection...');
  db.close();
  process.exit(0);
});

module.exports = api;
