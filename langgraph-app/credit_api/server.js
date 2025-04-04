const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const Database = require('better-sqlite3');
const path = require('path');

// Initialize the app
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

// Database connection
const dbPath = path.join(__dirname, 'credit_demo.sqlite');
const db = new Database(dbPath, { verbose: console.log });

// Create a middleware to inject the database connection
app.use((req, res, next) => {
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
app.get('/customers', (req, res) => {
  try {
    const customers = req.db.query('SELECT * FROM customers LIMIT 10');
    res.json(customers);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/customer', (req, res) => {
  try {
    const { id } = req.query;
    const customer = req.db.query('SELECT * FROM customers WHERE customer_id = ?', id);
    
    if (customer && customer.length > 0) {
      res.json(customer[0]);
    } else {
      res.status(404).json({ message: 'Customer Not Found' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Credit Applications APIs
app.get('/applications', (req, res) => {
  try {
    const applications = req.db.query('SELECT * FROM credit_applications ORDER BY application_date DESC LIMIT 10');
    res.json(applications);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/application', (req, res) => {
  try {
    const { id } = req.query;
    const application = req.db.query('SELECT * FROM credit_applications WHERE application_id = ?', id);
    
    if (application && application.length > 0) {
      res.json(application[0]);
    } else {
      res.status(404).json({ message: 'Application Not Found' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/applications', (req, res) => {
  try {
    const { customer_id, product_type, requested_amount } = req.body;
    
    // Insert the application
    const result = req.db.query(
      'INSERT INTO credit_applications (customer_id, product_type, requested_amount) VALUES (?, ?, ?) RETURNING *', 
      customer_id, product_type, requested_amount
    );
    
    // Get the inserted application
    const application = req.db.query('SELECT * FROM credit_applications WHERE rowid = last_insert_rowid()');
    
    if (application && application.length > 0) {
      res.json(application[0]);
    } else {
      res.status(500).json({ message: 'Failed to create application' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Credit Checks APIs
app.get('/credit-check', (req, res) => {
  try {
    const { application_id } = req.query;
    const check = req.db.query('SELECT * FROM credit_checks WHERE application_id = ?', application_id);
    
    if (check && check.length > 0) {
      res.json(check[0]);
    } else {
      res.status(404).json({ message: 'Credit Check Not Found' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/credit-check', (req, res) => {
  try {
    const { application_id, credit_score } = req.body;
    
    // Insert the credit check
    req.db.query(
      'INSERT INTO credit_checks (application_id, credit_score) VALUES (?, ?)', 
      application_id, credit_score
    );
    
    // Get the inserted credit check
    const check = req.db.query('SELECT * FROM credit_checks WHERE rowid = last_insert_rowid()');
    
    if (check && check.length > 0) {
      res.json(check[0]);
    } else {
      res.status(500).json({ message: 'Failed to create credit check' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// KYC Checks APIs
app.get('/kyc-check', (req, res) => {
  try {
    const { application_id } = req.query;
    const check = req.db.query('SELECT * FROM kyc_checks WHERE application_id = ?', application_id);
    
    if (check && check.length > 0) {
      res.json(check[0]);
    } else {
      res.status(404).json({ message: 'KYC Check Not Found' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/kyc-check', (req, res) => {
  try {
    const { application_id, kyc_passed, remarks } = req.body;
    
    // Insert the KYC check
    req.db.query(
      'INSERT INTO kyc_checks (application_id, kyc_passed, remarks) VALUES (?, ?, ?)', 
      application_id, kyc_passed, remarks
    );
    
    // Get the inserted KYC check
    const check = req.db.query('SELECT * FROM kyc_checks WHERE rowid = last_insert_rowid()');
    
    if (check && check.length > 0) {
      res.json(check[0]);
    } else {
      res.status(500).json({ message: 'Failed to create KYC check' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Income Verification APIs
app.get('/income-verification', (req, res) => {
  try {
    const { application_id } = req.query;
    const income = req.db.query('SELECT * FROM income_verifications WHERE application_id = ?', application_id);
    
    if (income && income.length > 0) {
      res.json(income[0]);
    } else {
      res.status(404).json({ message: 'Income Verification Not Found' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/income-verification', (req, res) => {
  try {
    const { application_id, declared_income, verified_income, remarks } = req.body;
    const status = declared_income === verified_income ? 'Completed' : 'Mismatch';
    
    // Insert the income verification
    req.db.query(
      'INSERT INTO income_verifications (application_id, declared_income, verified_income, remarks, status) VALUES (?, ?, ?, ?, ?)', 
      application_id, declared_income, verified_income, remarks, status
    );
    
    // Get the inserted income verification
    const income = req.db.query('SELECT * FROM income_verifications WHERE rowid = last_insert_rowid()');
    
    if (income && income.length > 0) {
      res.json(income[0]);
    } else {
      res.status(500).json({ message: 'Failed to create income verification' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Background Checks APIs
app.get('/background-check', (req, res) => {
  try {
    const { application_id } = req.query;
    const check = req.db.query('SELECT * FROM background_checks WHERE application_id = ?', application_id);
    
    if (check && check.length > 0) {
      res.json(check[0]);
    } else {
      res.status(404).json({ message: 'Background Check Not Found' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/background-check', (req, res) => {
  try {
    const { application_id, criminal_record, debt_collections, remarks } = req.body;
    
    // Insert the background check
    req.db.query(
      'INSERT INTO background_checks (application_id, criminal_record, debt_collections, remarks) VALUES (?, ?, ?, ?)', 
      application_id, criminal_record, debt_collections, remarks
    );
    
    // Get the inserted background check
    const check = req.db.query('SELECT * FROM background_checks WHERE rowid = last_insert_rowid()');
    
    if (check && check.length > 0) {
      res.json(check[0]);
    } else {
      res.status(500).json({ message: 'Failed to create background check' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Manual Approval APIs
app.get('/manual-approval', (req, res) => {
  try {
    const { application_id } = req.query;
    const approval = req.db.query('SELECT * FROM manual_approvals WHERE application_id = ?', application_id);
    
    if (approval && approval.length > 0) {
      res.json(approval[0]);
    } else {
      res.status(404).json({ message: 'Manual Approval Not Found' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/manual-approval', (req, res) => {
  try {
    const { application_id, approver_name, approval_notes, approved } = req.body;
    
    // Insert the manual approval
    req.db.query(
      'INSERT INTO manual_approvals (application_id, approver_name, approval_notes, approved) VALUES (?, ?, ?, ?)', 
      application_id, approver_name, approval_notes, approved
    );
    
    // Get the inserted manual approval
    const approval = req.db.query('SELECT * FROM manual_approvals WHERE rowid = last_insert_rowid()');
    
    if (approval && approval.length > 0) {
      res.json(approval[0]);
    } else {
      res.status(500).json({ message: 'Failed to create manual approval' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Final Decision APIs
app.get('/final-decision', (req, res) => {
  try {
    const { application_id } = req.query;
    const decision = req.db.query('SELECT * FROM final_decisions WHERE application_id = ?', application_id);
    
    if (decision && decision.length > 0) {
      res.json(decision[0]);
    } else {
      res.status(404).json({ message: 'Final Decision Not Found' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/final-decision', (req, res) => {
  try {
    const { application_id, decision, reason } = req.body;
    
    // Insert the final decision
    req.db.query(
      'INSERT INTO final_decisions (application_id, decision, reason) VALUES (?, ?, ?)', 
      application_id, decision, reason
    );
    
    // Update the application status
    req.db.query(
      'UPDATE credit_applications SET status = ? WHERE application_id = ?', 
      decision, application_id
    );
    
    // Get the inserted final decision
    const finalDecision = req.db.query('SELECT * FROM final_decisions WHERE rowid = last_insert_rowid()');
    
    if (finalDecision && finalDecision.length > 0) {
      res.json(finalDecision[0]);
    } else {
      res.status(500).json({ message: 'Failed to create final decision' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'Credit Approval API is running' });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('Closing database connection...');
  db.close();
  process.exit(0);
});

module.exports = app;
