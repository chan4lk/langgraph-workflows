-- Script to TRUNCATE all EBIS Link schema tables and re-insert MORE COMPREHENSIVE sample data.
-- WARNING: DELETES ALL EXISTING DATA IN THESE TABLES. RUN WITH CAUTION.

BEGIN;

\echo 'Starting truncation process...'

-- Truncate tables in reverse order of dependency (children first)
-- Using RESTART IDENTITY to reset sequences, CASCADE for sequence restart propagation

\echo 'Truncating detail/linking tables...'
TRUNCATE TABLE special_roster_person RESTART IDENTITY CASCADE;
TRUNCATE TABLE r4_signing_bonus_pool_pick RESTART IDENTITY CASCADE;
TRUNCATE TABLE csp_payment_history RESTART IDENTITY CASCADE;
TRUNCATE TABLE cep_payment_history RESTART IDENTITY CASCADE;
TRUNCATE TABLE award_vote RESTART IDENTITY CASCADE;
TRUNCATE TABLE arbitration_assigned_arbitrator RESTART IDENTITY CASCADE;
TRUNCATE TABLE tx_bulletin_detail RESTART IDENTITY CASCADE;
TRUNCATE TABLE transaction_player_detail RESTART IDENTITY CASCADE;
-- Add TRUNCATE for specific tx_detail_* tables if they were created
TRUNCATE TABLE tx_detail_generic RESTART IDENTITY CASCADE; -- Example detail table
TRUNCATE TABLE tx_detail_mj_dl RESTART IDENTITY CASCADE;   -- Example detail table
TRUNCATE TABLE tx_detail_ptbnl RESTART IDENTITY CASCADE;   -- Example detail table
-- ... add TRUNCATE for ALL OTHER tx_detail_* tables you created ...
TRUNCATE TABLE add_c_salary RESTART IDENTITY CASCADE;
TRUNCATE TABLE mnc_addendum_b RESTART IDENTITY CASCADE; -- Base Addendum B table
-- Add TRUNCATE for specific addendum B detail tables if created (e.g., mnc_add_b_signing_bonus)
TRUNCATE TABLE mnc_addendum_a RESTART IDENTITY CASCADE;
TRUNCATE TABLE mjc_pay_schedule RESTART IDENTITY CASCADE;
TRUNCATE TABLE mjc_signing_bonus RESTART IDENTITY CASCADE;
TRUNCATE TABLE mjc_award_bonus RESTART IDENTITY CASCADE; -- Add other bonus types if created
TRUNCATE TABLE mjc_performance_bonus RESTART IDENTITY CASCADE;
TRUNCATE TABLE mjc_other_bonus RESTART IDENTITY CASCADE;
TRUNCATE TABLE mjc_salary_escalator RESTART IDENTITY CASCADE;
TRUNCATE TABLE mjc_option_clause RESTART IDENTITY CASCADE;
TRUNCATE TABLE mjc_covenant RESTART IDENTITY CASCADE; -- If created
TRUNCATE TABLE mjc_file_attachment_type_link RESTART IDENTITY CASCADE; -- If created
TRUNCATE TABLE mjc_file_attachment RESTART IDENTITY CASCADE; -- If created
TRUNCATE TABLE mjc_mn_compensation RESTART IDENTITY CASCADE;
TRUNCATE TABLE mjc_mj_compensation RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_yearly_service_days RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_mn_league_summary RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_mj_league_summary RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_intl_program_participation RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_dom_program_participation RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_dom_draft_history RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_dom_letter_of_intent RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_dom_positions RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_national_id RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_address RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_email_address RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_phone_number RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_agent RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_visa_info RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_baseball_info RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_bio_info RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_dom_info RESTART IDENTITY CASCADE;
TRUNCATE TABLE person_service_info RESTART IDENTITY CASCADE;

\echo 'Truncating core entity tables...'
TRUNCATE TABLE special_roster RESTART IDENTITY CASCADE;
TRUNCATE TABLE intl_signing_bonus_pool RESTART IDENTITY CASCADE;
TRUNCATE TABLE r4_signing_bonus_pool RESTART IDENTITY CASCADE;
TRUNCATE TABLE system_date_club RESTART IDENTITY CASCADE;
TRUNCATE TABLE r5_eligible_player RESTART IDENTITY CASCADE;
TRUNCATE TABLE pre_arb_bonus_payment RESTART IDENTITY CASCADE;
TRUNCATE TABLE minor_bonus_payment RESTART IDENTITY CASCADE;
TRUNCATE TABLE csp RESTART IDENTITY CASCADE;
TRUNCATE TABLE cep RESTART IDENTITY CASCADE;
TRUNCATE TABLE award RESTART IDENTITY CASCADE;
TRUNCATE TABLE arbitration RESTART IDENTITY CASCADE;
TRUNCATE TABLE tx_bulletin RESTART IDENTITY CASCADE;
TRUNCATE TABLE transaction RESTART IDENTITY CASCADE;
TRUNCATE TABLE add_d RESTART IDENTITY CASCADE;
TRUNCATE TABLE add_c RESTART IDENTITY CASCADE;
TRUNCATE TABLE mnc RESTART IDENTITY CASCADE;
TRUNCATE TABLE mjc RESTART IDENTITY CASCADE;
TRUNCATE TABLE roster_snapshot RESTART IDENTITY CASCADE;
TRUNCATE TABLE person RESTART IDENTITY CASCADE;

\echo 'Truncating system value/date tables...'
TRUNCATE TABLE system_value RESTART IDENTITY CASCADE;
TRUNCATE TABLE system_date RESTART IDENTITY CASCADE;

\echo 'Truncating lookup tables...'
-- Truncate lookups referencing other lookups first
TRUNCATE TABLE lk_club RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_league RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_city RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_sector RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_district RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_state RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_province RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_agent RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_school RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_school_division RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_employee_position RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_national_id_type RESTART IDENTITY CASCADE;
-- Add FK lookups if others exist

-- Truncate base lookup tables (Order might matter less here if no cross-lk dependencies remain)
TRUNCATE TABLE lk_person_type RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_country RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_baseball_position RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_stats_position RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_roster_status RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_level_of_play RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_org RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_agency RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_phone_number_type RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_address_type RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_email_address_type RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_immigration_status RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_spoken_language RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_equal_opportunity RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_tx_type RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_tx_name RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_tx_status RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_mjc_type RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_mjc_status RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_mnc_type RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_mnc_status RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_add_c_status RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_add_d_status RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_award RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_arbitration_status RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_school_type RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_school_class RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_r4_draft_status RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_amateur_program RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_intl_program RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_employee_type RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_body_part RESTART IDENTITY CASCADE; -- Add remaining lookup truncates
TRUNCATE TABLE lk_body_part_detail RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_body_side RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_diagnosis RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_injury_sustained RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_add_b_type RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_compounding_type RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_file_attachment_type RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_auth_signatory RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_mnc_parental_consent RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_mnc_life_insurance_status RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_bonus_payment_status RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_minor_bonus_type RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_cep_csp_status RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_cep_csp_invoice_status RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_csp_period RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_csp_period_type RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_arb_practitioner RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_arbitrator RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_arbitrator_decision RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_r5_phase RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_roster_type RESTART IDENTITY CASCADE;
TRUNCATE TABLE lk_pro_roster_snapshot_type RESTART IDENTITY CASCADE; -- Or similar name
TRUNCATE TABLE lk_tx_il_reason RESTART IDENTITY CASCADE;
-- Add any other lk_ tables...

\echo 'Truncation complete.'
\echo 'Starting sample data insertion (more comprehensive)...'

-- =============== SAMPLE DATA INSERTION ===============

-- Lookup Data (Ensure enough variety)
INSERT INTO lk_person_type (id, code, description) SELECT i, 'TYPE'||i, 'Person Type '||i FROM generate_series(1, 5) AS i ON CONFLICT DO NOTHING;
INSERT INTO lk_country (id, code, short_name, name) SELECT i, 'C'||i, 'Ct'||i, 'Country '||i FROM generate_series(1, 10) AS i ON CONFLICT DO NOTHING;
INSERT INTO lk_state (id, code, name) SELECT i, 'S'||i, 'State '||i FROM generate_series(1, 10) AS i ON CONFLICT DO NOTHING;
INSERT INTO lk_baseball_position (id, code, description, grouping) SELECT i, 'POS'||i, 'Position '||i, CASE WHEN i <= 2 THEN 'Pitcher' WHEN i<=6 THEN 'Infielder' ELSE 'Outfielder' END FROM generate_series(1, 10) AS i ON CONFLICT DO NOTHING;
INSERT INTO lk_roster_status (id, code, description, short_description, is_major, is_minor, is_40_man, is_il_status, is_dl_status) VALUES
    (1, 'ACTIVE', 'Active', 'ACT', TRUE, TRUE, TRUE, FALSE, FALSE), (2, 'IL10', '10-Day IL', 'IL10', TRUE, FALSE, TRUE, TRUE, TRUE), (3, 'IL60', '60-Day IL', 'IL60', TRUE, FALSE, FALSE, TRUE, TRUE), (4, 'DFA', 'Designated for Assignment', 'DFA', TRUE, TRUE, TRUE, FALSE, FALSE), (5, 'OPT', 'Optioned', 'OPT', FALSE, TRUE, TRUE, FALSE, FALSE), (6, 'AAA', 'Active Triple-A', 'AAA', FALSE, TRUE, TRUE, FALSE, FALSE), (7, 'AA', 'Active Double-A', 'AA', FALSE, TRUE, FALSE, FALSE, FALSE), (8, 'VOL', 'Voluntarily Retired', 'VOL', FALSE, FALSE, FALSE, TRUE, FALSE), (9, 'SUSP', 'Suspended List', 'SUSP', TRUE, TRUE, FALSE, TRUE, FALSE), (10, 'PAT', 'Paternity List', 'PAT', TRUE, FALSE, TRUE, TRUE, FALSE)
ON CONFLICT (id) DO NOTHING;
INSERT INTO lk_level_of_play (id, code, description) VALUES (1, 'MLB', 'Major League'), (2, 'AAA', 'Triple-A'), (3, 'AA', 'Double-A'), (4, 'A+', 'High-A'), (5, 'A', 'Single-A'), (6, 'Rk', 'Rookie Complex'), (7, 'DSL', 'Dominican Summer League'), (8, 'VSL', 'Venezuelan Summer League') ON CONFLICT DO NOTHING;
INSERT INTO lk_org (id, code, name) SELECT i, 'ORG'||i, 'Organization '||i FROM generate_series(1, 10) AS i ON CONFLICT DO NOTHING;
INSERT INTO lk_league (id, code, name, level_of_play_id) SELECT i, 'LG'||i, 'League '||i, (i%8)+1 FROM generate_series(1, 10) AS i ON CONFLICT DO NOTHING;
INSERT INTO lk_club (id, org_id, league_id, bam_club_id, short_name, name) SELECT i, (i%10)+1, (i%10)+1, 1000+i, 'CL'||i, 'Club '||i FROM generate_series(1, 10) AS i ON CONFLICT DO NOTHING;
INSERT INTO lk_agency (id, name) SELECT i, 'Agency '||i FROM generate_series(1, 5) AS i ON CONFLICT DO NOTHING;
INSERT INTO lk_agent (id, agency_id, first_name, last_name) SELECT i, (i%5)+1, 'AgentF'||i, 'AgentL'||i FROM generate_series(1, 10) AS i ON CONFLICT DO NOTHING;
INSERT INTO lk_phone_number_type (id, code, description) VALUES (1, 'MOBILE', 'Mobile'), (2, 'HOME', 'Home'), (3, 'WORK', 'Work') ON CONFLICT DO NOTHING;
INSERT INTO lk_address_type (id, code, description) VALUES (1, 'HOME', 'Home'), (2, 'MAIL', 'Mailing') ON CONFLICT DO NOTHING;
INSERT INTO lk_email_address_type (id, code, description) VALUES (1, 'PERS', 'Personal'), (2, 'WORK', 'Work') ON CONFLICT DO NOTHING;
INSERT INTO lk_tx_type (id, code, description) SELECT i, 'TXTYPE'||i, 'Tx Type Desc '||i FROM generate_series(1, 10) AS i ON CONFLICT DO NOTHING; -- Use more realistic codes from prev answer if needed
INSERT INTO lk_tx_name (id, name) SELECT i, 'Tx Name Desc '||i FROM generate_series(1, 10) AS i ON CONFLICT DO NOTHING; -- Use more realistic names from prev answer if needed
INSERT INTO lk_tx_status (id, code, description) VALUES (1,'PEND','Pending'),(2,'APPR','Approved'),(3,'VOID','Voided'),(4,'REJ','Rejected') ON CONFLICT DO NOTHING;
INSERT INTO lk_mjc_type (id, code, description) SELECT i, 'MJCT'||i, 'MJC Type '||i FROM generate_series(1, 3) AS i ON CONFLICT DO NOTHING;
INSERT INTO lk_mjc_status (id, code, description) SELECT i, 'MJCS'||i, 'MJC Status '||i FROM generate_series(1, 4) AS i ON CONFLICT DO NOTHING;
INSERT INTO lk_mnc_type (id, code, description) SELECT i, 'MNCT'||i, 'MNC Type '||i FROM generate_series(1, 3) AS i ON CONFLICT DO NOTHING;
INSERT INTO lk_mnc_status (id, code, description) SELECT i, 'MNCS'||i, 'MNC Status '||i FROM generate_series(1, 4) AS i ON CONFLICT DO NOTHING;
INSERT INTO lk_add_c_status (id, code, description) SELECT i, 'ADDCSTAT'||i, 'Add C Status '||i FROM generate_series(1, 3) AS i ON CONFLICT DO NOTHING;
INSERT INTO lk_add_d_status (id, code, description) SELECT i, 'ADDDSTAT'||i, 'Add D Status '||i FROM generate_series(1, 2) AS i ON CONFLICT DO NOTHING;
INSERT INTO lk_add_b_type (id, code, description) SELECT i, 'ADDBTYPE'||i, 'Add B Type '||i FROM generate_series(1, 10) AS i ON CONFLICT DO NOTHING; -- Placeholder for various Add B clauses

-- Core Entities
INSERT INTO person (person_id, person_type_id, current_org_id, current_club_id, mj_roster_status_id, mn_roster_status_id)
SELECT 100 + i, (i%5)+1, (i%10)+1, (i%10)+1, (i%10)+1, (i%10)+1
FROM generate_series(1, 10) AS i;

INSERT INTO person_bio_info (person_id, last_name, first_name, birthdate, birth_country_id)
SELECT 100+i, 'LastName'||i, 'FirstName'||i, make_date(1990+(i%12), (i%12)+1, (i%28)+1), (i%10)+1
FROM generate_series(1, 10) AS i;

INSERT INTO person_baseball_info (person_id, player_position_id, height_inches, weight_lbs, batting_side, throwing_side, is_on_40_man_roster)
SELECT 100+i, (i%10)+1, 68+(i%8), 170+(i*5), CASE WHEN i%3=0 THEN 'L' WHEN i%3=1 THEN 'R' ELSE 'S' END, CASE WHEN i%2=0 THEN 'L' ELSE 'R' END, (i%2=0)
FROM generate_series(1, 10) AS i;

INSERT INTO person_agent (person_id, agent_id, agency_id)
SELECT 100+i, (i%10)+1, (SELECT agency_id FROM lk_agent WHERE id = (i%10)+1)
FROM generate_series(1, 10) AS i;

INSERT INTO person_phone_number (person_id, phone_number_type_id, country_id, phone_number)
SELECT 100+i, (i%3)+1, (i%10)+1, '555-02'||LPAD(i::text, 2, '0')
FROM generate_series(1, 10) AS i;

INSERT INTO person_email_address (person_id, email_address_type_id, email_address)
SELECT 100+i, (i%2)+1, 'player'||i||'@email.com'
FROM generate_series(1, 10) AS i;

INSERT INTO person_address (person_id, address_type_id, address1, city, state_id, zip, country_id)
SELECT 100+i, 1, i||' Main St', 'Anytown'||i, (i%10)+1, LPAD(((i*1234)%90000+10000)::text, 5, '0'), (i%10)+1
FROM generate_series(1, 10) AS i;

INSERT INTO person_service_info (person_id, total_mls_years, total_mls_days, mn_service_years, mn_contract_years)
SELECT 100+i, i%6, (random()*171)::int, i%8, i%8
FROM generate_series(1, 10) AS i;

-- Contracts
INSERT INTO mjc (mjc_id, person_id, mjc_type_id, current_contract_status_id, start_year, non_option_years, signed_date, signing_org_id, current_org_id)
SELECT 200+i, 100+i, (i%3)+1, (i%4)+1, 2020+(i%4), i%6+1, current_date - (i*interval '3 month'), (i%10)+1, (i%10)+1
FROM generate_series(1, 10) AS i;

INSERT INTO mnc (mnc_id, person_id, mnc_type_id, mnc_status_id, name_on_contract)
SELECT 300+i, 100+i, (i%3)+1, (i%4)+1, 'MNC Player Name '||i
FROM generate_series(1, 10) AS i;

-- Contract Details
INSERT INTO mjc_mj_compensation (mjc_id, year, guaranteed_salary, base_salary)
SELECT 200+i, 2023+(i%3), (random()*10+1)*1000000, (random()*1+0.7)*1000000 -- Year, guaranteed, base
FROM generate_series(1, 10) AS i
UNION ALL -- Add a second year for some contracts
SELECT 200+i, 2024+(i%3), (random()*12+1.5)*1000000, (random()*1.2+0.8)*1000000
FROM generate_series(1, 5) AS i; -- Only for first 5 MJCs

INSERT INTO mjc_signing_bonus (mjc_id, bonus_amount)
SELECT 200+i, (random()*5+0.5)*100000 -- Signing bonus for all MJCs
FROM generate_series(1, 10) AS i;

INSERT INTO mjc_pay_schedule (mjc_id, related_signing_bonus_id, payment_date, payment_amount)
SELECT mjc.mjc_id, sb.mjc_signing_bonus_id, mjc.signed_date + interval '30 days', sb.bonus_amount / 2
FROM mjc JOIN mjc_signing_bonus sb ON mjc.mjc_id = sb.mjc_id
UNION ALL
SELECT mjc.mjc_id, sb.mjc_signing_bonus_id, mjc.signed_date + interval '1 year', sb.bonus_amount / 2
FROM mjc JOIN mjc_signing_bonus sb ON mjc.mjc_id = sb.mjc_id;

INSERT INTO mnc_addendum_a (mnc_id, beginning_in_year, num_seasons, org_id, club_id)
SELECT 300+i, 2023+(i%2), i%5+1, (i%10)+1, (i%10)+1
FROM generate_series(1, 10) AS i;

INSERT INTO mnc_addendum_b (mnc_id, add_b_type_id, language_data)
SELECT 300+i, (i%10)+1, 'Generic Addendum B Clause Text for Type '||(i%10)+1
FROM generate_series(1, 10) AS i; -- One generic Add B per MNC

-- Add C & D
INSERT INTO add_c (add_c_id, person_id, mnc_id, add_c_year, add_c_status_id, signed_date, org_id)
SELECT 400+i, 100+i, CASE WHEN i%2=0 THEN 300+i ELSE NULL END, 2022+(i%3), (i%3)+1, current_date-(i*interval '1 month'), (i%10)+1
FROM generate_series(1, 10) AS i;

INSERT INTO add_c_salary (add_c_id, level_of_play_id, monthly_salary)
SELECT 400+i, (i%8)+1, (random()*1000+2000)
FROM generate_series(1, 10) AS i;

INSERT INTO add_d (add_d_id, person_id, mnc_id, year, current_status_id, signed_date, org_id)
SELECT 500+i, 100+i, CASE WHEN i%2=1 THEN 300+i ELSE NULL END, 2023+(i%2), (i%2)+1, current_date-(i*interval '2 month'), (i%10)+1
FROM generate_series(1, 10) AS i;

-- Transactions
INSERT INTO transaction (tx_id, tx_type_id, tx_name_id, tx_date, current_status_id, approved_timestamp, event_id)
SELECT 600+i, (i%10)+1, (i%10)+1, current_date-(i*interval '10 days'), 2, NOW()-(i*interval '9 days'), 10000+i
FROM generate_series(1, 10) AS i;

INSERT INTO transaction_player_detail (tx_id, person_id, prior_org_id, post_org_id, prior_club_id, post_club_id, prior_mj_roster_status_id, post_mj_roster_status_id, prior_mn_roster_status_id, post_mn_roster_status_id)
SELECT 600+i, 100+i, CASE WHEN i%2=0 THEN (i%10)+1 ELSE NULL END, (i%10)+1, CASE WHEN i%2=0 THEN (i%10)+1 ELSE NULL END, (i%10)+1, (i%10)+1, ((i+1)%10)+1, (i%10)+1, ((i+1)%10)+1
FROM generate_series(1, 10) AS i;

-- Transaction Details (Example for Generic and MJ DL)
INSERT INTO tx_detail_generic (tx_id)
SELECT 600+i FROM generate_series(1, 10, 2) AS i; -- Odd tx_id

INSERT INTO tx_detail_mj_dl (tx_id, injury_date, earliest_reinstatement_date, body_part_id, diagnosis_id)
SELECT 600+i, current_date-(i*interval '10 days'), current_date-(i*interval '10 days')+interval '10 days', (i%5)+1, (i%5)+1 -- Needs lk_body_part, lk_diagnosis populated
FROM generate_series(2, 10, 2) AS i; -- Even tx_id (assuming lookup tables have IDs 1-5)

-- Bulletin
INSERT INTO tx_bulletin (bulletin_id, bulletin_date)
SELECT 700+i, current_date-(i*interval '1 day')
FROM generate_series(1, 10) AS i;

INSERT INTO tx_bulletin_detail (bulletin_id, tx_id, person_id, org_code, player_name, description, tx_date, approved_date)
SELECT 700+i, 600+i, 100+i, 'ORG'||((i%10)+1), 'LName'||i||', FName'||i, 'Bulletin Desc '||i, current_date-(i*interval '10 days'), current_date-(i*interval '9 days')
FROM generate_series(1, 10) AS i;

-- Other Core Entities
INSERT INTO arbitration (arbitration_id, person_id, arbitration_org_id, arbitration_year, arbitration_status_id, club_offer, player_offer)
SELECT 800+i, 100+i, (i%10)+1, 2023+(i%2), (i%5)+1, (random()*5M+0.5M), (random()*6M+0.6M)
FROM generate_series(1, 10) AS i;

INSERT INTO award (award_id, award_code, league, year)
SELECT 900+i, ((i-1)%4)+101, CASE WHEN i%2=0 THEN 'AL' ELSE 'NL' END, 2022+(i%3) -- Award codes 101-104
FROM generate_series(1, 10) AS i;

INSERT INTO award_vote (award_id, person_id, votes, place)
SELECT 900+i, 100+i, (random()*100)::int, (i%5)+1
FROM generate_series(1, 10) AS i;

INSERT INTO cep (person_id, mnc_id, status_id, responsible_org_id, tuition_allowance_commitment, living_allowance_commitment)
SELECT 100+i, CASE WHEN i%3=0 THEN 300+i ELSE NULL END, 1, (i%10)+1, random()*50000+10000, random()*10000+2000
FROM generate_series(1, 10) AS i;

INSERT INTO csp (person_id, mnc_id, status_id, responsible_org_id, tuition_allowance_commitment_total, living_allowance_commitment_total)
SELECT 100+i, CASE WHEN i%4=0 THEN 300+i ELSE NULL END, 1, (i%10)+1, random()*60000+15000, random()*12000+3000
FROM generate_series(1, 10) AS i;

INSERT INTO minor_bonus_payment (mnc_bonus_payment_tracking_id, person_id, mnc_id, status_id, bonus_type_id, responsible_org_id, amount, due_date, date_paid)
SELECT 1000+i, 100+i, CASE WHEN i%2=0 THEN 300+i ELSE NULL END, 1, (i%5)+1, (i%10)+1, random()*10000+1000, current_date-(i*interval '20 days'), current_date-(i*interval '15 days')
FROM generate_series(1, 10) AS i;

INSERT INTO pre_arb_bonus_payment (pre_arb_bonus_id, year, org_id, person_id, war, payment_amount)
SELECT 1100+i, 2022+(i%3), (i%10)+1, 100+i, round((random()*5)::numeric, 1), random()*1000000+50000
FROM generate_series(1, 10) AS i;

INSERT INTO r5_eligible_player (year, person_id, position_id, org_id, club_id, level_of_play_id, roster_status_id, birthdate)
SELECT 2023+(i%2), 100+i, (i%10)+1, (i%10)+1, (i%10)+1, (i%8)+1, (i%10)+1, (SELECT birthdate FROM person_bio_info WHERE person_id = 100+i)
FROM generate_series(1, 10) AS i;

INSERT INTO system_date (system_date_year, first_day_of_major_league_season, last_day_of_major_league_season)
SELECT 2020+i, make_date(2020+i, 3, 25+(i%5)), make_date(2020+i, 9, 28+(i%3))
FROM generate_series(0, 4) AS i ON CONFLICT DO NOTHING;

INSERT INTO system_date_club (system_date_year, club_id, league_id, first_game_of_season, last_game_of_season)
SELECT 2020+(i%5), (i%10)+1, (SELECT league_id FROM lk_club WHERE id = (i%10)+1), make_date(2020+(i%5), 4, 1+(i%7)), make_date(2020+(i%5), 9, 15+(i%10))
FROM generate_series(1, 10) AS i ON CONFLICT DO NOTHING;

INSERT INTO system_value (system_value_year, originally_scheduled_days_in_season, actual_days_in_season, originally_scheduled_games_in_season, actual_games_in_season)
SELECT 2020+i, 183+(i%5), 180+(i%5), 162, 162-(i%3)
FROM generate_series(0, 4) AS i ON CONFLICT DO NOTHING;

INSERT INTO r4_signing_bonus_pool (org_id, year, club_signing_bonus_pool_amount, total_signing_bonus_amount)
SELECT (i%10)+1, 2022+(i%3), random()*5M+5M, random()*4M+4.5M
FROM generate_series(1, 10) AS i ON CONFLICT DO NOTHING;

INSERT INTO intl_signing_bonus_pool (org_id, signing_period_start_year, signing_period_end_year, club_signing_bonus_pool_amount, total_actual_signing_bonus_amount)
SELECT (i%10)+1, 2022+(i%3), 2023+(i%3), random()*4M+3M, random()*3.5M+2.8M
FROM generate_series(1, 10) AS i ON CONFLICT DO NOTHING;

INSERT INTO roster_snapshot (roster_date, person_id, org_id, club_id, mj_roster_status_id, mn_roster_status_id)
SELECT current_date-(i*interval '1 day'), 100+i, (SELECT current_org_id FROM person WHERE person_id = 100+i), (SELECT current_club_id FROM person WHERE person_id = 100+i), (SELECT mj_roster_status_id FROM person WHERE person_id = 100+i), (SELECT mn_roster_status_id FROM person WHERE person_id = 100+i)
FROM generate_series(1, 10) AS i;

INSERT INTO special_roster (org_id, club_id, year, roster_type_id)
SELECT (i%10)+1, CASE WHEN i%2=0 THEN (i%10)+1 ELSE NULL END, 2023+(i%2), (i%5)+1
FROM generate_series(1, 10) AS i ON CONFLICT DO NOTHING;

INSERT INTO special_roster_person (special_roster_id, person_id)
SELECT sr.special_roster_id, 100+i -- Use actual generated special_roster_id if sequence used
FROM special_roster sr JOIN generate_series(1, 10) i ON sr.org_id = (i % 10) + 1 AND sr.year = 2023 + (i % 2) AND sr.roster_type_id = (i % 5) + 1 LIMIT 10; -- Need a better way to join if IDs aren't sequential 1-10


\echo 'Sample data insertion complete.'

COMMIT;

\echo 'Truncate and data insertion script finished.'