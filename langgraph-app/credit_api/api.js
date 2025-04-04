// Customers APIs
api.get('/customers', (req, res, { db }) => {
  const customers = db.query('SELECT * FROM customers LIMIT 10');
  res.json(customers);
});

api.get('/customer', (req, res, { db }) => {
  const { id } = req.query;
  const customer = db.query('SELECT * FROM customers WHERE customer_id = ?', id)[0];

  if (customer) res.json(customer);
  else res.status(404).json({ message: 'Customer Not Found' });
});

// Credit Applications APIs
api.get('/applications', (req, res, { db }) => {
  const applications = db.query('SELECT * FROM credit_applications ORDER BY application_date DESC LIMIT 10');
  res.json(applications);
});

api.get('/application', (req, res, { db }) => {
  const { id } = req.query;
  const application = db.query('SELECT * FROM credit_applications WHERE application_id = ?', id)[0];

  if (application) res.json(application);
  else res.status(404).json({ message: 'Application Not Found' });
});

api.post('/applications', (req, res, { db }) => {
  const { customer_id, product_type, requested_amount } = req.body;
  const result = db.query('INSERT INTO credit_applications (customer_id, product_type, requested_amount) VALUES (?, ?, ?) RETURNING *', customer_id, product_type, requested_amount);
  res.json(result[0]);
});

// Credit Checks APIs
api.get('/credit-check', (req, res, { db }) => {
  const { application_id } = req.query;
  const check = db.query('SELECT * FROM credit_checks WHERE application_id = ?', application_id)[0];

  if (check) res.json(check);
  else res.status(404).json({ message: 'Credit Check Not Found' });
});

api.post('/credit-check', (req, res, { db }) => {
  const { application_id, credit_score } = req.body;
  const result = db.query('INSERT INTO credit_checks (application_id, credit_score) VALUES (?, ?) RETURNING *', application_id, credit_score);
  res.json(result[0]);
});

// KYC Checks APIs
api.get('/kyc-check', (req, res, { db }) => {
  const { application_id } = req.query;
  const check = db.query('SELECT * FROM kyc_checks WHERE application_id = ?', application_id)[0];

  if (check) res.json(check);
  else res.status(404).json({ message: 'KYC Check Not Found' });
});

api.post('/kyc-check', (req, res, { db }) => {
  const { application_id, kyc_passed, remarks } = req.body;
  const result = db.query('INSERT INTO kyc_checks (application_id, kyc_passed, remarks) VALUES (?, ?, ?) RETURNING *', application_id, kyc_passed, remarks);
  res.json(result[0]);
});

// Income Verification APIs
api.get('/income-verification', (req, res, { db }) => {
  const { application_id } = req.query;
  const income = db.query('SELECT * FROM income_verifications WHERE application_id = ?', application_id)[0];

  if (income) res.json(income);
  else res.status(404).json({ message: 'Income Verification Not Found' });
});

api.post('/income-verification', (req, res, { db }) => {
  const { application_id, declared_income, verified_income, remarks } = req.body;
  const status = declared_income === verified_income ? 'Completed' : 'Mismatch';
  const result = db.query('INSERT INTO income_verifications (application_id, declared_income, verified_income, remarks, status) VALUES (?, ?, ?, ?, ?) RETURNING *', application_id, declared_income, verified_income, remarks, status);
  res.json(result[0]);
});

// Background Checks APIs
api.get('/background-check', (req, res, { db }) => {
  const { application_id } = req.query;
  const check = db.query('SELECT * FROM background_checks WHERE application_id = ?', application_id)[0];

  if (check) res.json(check);
  else res.status(404).json({ message: 'Background Check Not Found' });
});

api.post('/background-check', (req, res, { db }) => {
  const { application_id, criminal_record, debt_collections, remarks } = req.body;
  const result = db.query('INSERT INTO background_checks (application_id, criminal_record, debt_collections, remarks) VALUES (?, ?, ?, ?) RETURNING *', application_id, criminal_record, debt_collections, remarks);
  res.json(result[0]);
});

// Manual Approval APIs
api.get('/manual-approval', (req, res, { db }) => {
  const { application_id } = req.query;
  const approval = db.query('SELECT * FROM manual_approvals WHERE application_id = ?', application_id)[0];

  if (approval) res.json(approval);
  else res.status(404).json({ message: 'Manual Approval Not Found' });
});

api.post('/manual-approval', (req, res, { db }) => {
  const { application_id, approver_name, approval_notes, approved } = req.body;
  const result = db.query('INSERT INTO manual_approvals (application_id, approver_name, approval_notes, approved) VALUES (?, ?, ?, ?) RETURNING *', application_id, approver_name, approval_notes, approved);
  res.json(result[0]);
});

// Final Decision APIs
api.get('/final-decision', (req, res, { db }) => {
  const { application_id } = req.query;
  const decision = db.query('SELECT * FROM final_decisions WHERE application_id = ?', application_id)[0];

  if (decision) res.json(decision);
  else res.status(404).json({ message: 'Final Decision Not Found' });
});

api.post('/final-decision', (req, res, { db }) => {
  const { application_id, decision, reason } = req.body;
  const result = db.query('INSERT INTO final_decisions (application_id, decision, reason) VALUES (?, ?, ?) RETURNING *', application_id, decision, reason);

  db.query('UPDATE credit_applications SET status = ? WHERE application_id = ?', decision, application_id);
  res.json(result[0]);
});
