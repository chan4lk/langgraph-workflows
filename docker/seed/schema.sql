-- PostgreSQL Schema based on eBis Link API Swagger

-- =============== LOOKUP TABLES ===============
-- (Inferred from definitions like CountryApi - Lookup, StateApi - Lookup, etc. and /lkup paths)

CREATE TABLE lk_person_type (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_country (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    short_name TEXT,
    name TEXT,
    dial_code INTEGER,
    use_dropdown_flag BOOLEAN, -- From CountryApiSystemValuesV1
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_state (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    name TEXT,
    -- Assuming state belongs to a country, though not explicitly in StateApi - Lookup definition
    -- country_id INTEGER REFERENCES lk_country(id),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_province (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    -- country_id INTEGER REFERENCES lk_country(id), -- Likely relationship
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_district (
    id INTEGER PRIMARY KEY,
    description TEXT,
    country_id INTEGER REFERENCES lk_country(id), -- From DistrictApi - Lookup
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_city (
    id INTEGER PRIMARY KEY,
    description TEXT,
    district_id INTEGER REFERENCES lk_district(id), -- From CityApi - Lookup
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_sector (
    id INTEGER PRIMARY KEY,
    description TEXT,
    city_id INTEGER REFERENCES lk_city(id), -- From SectorApi - Lookup
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);


CREATE TABLE lk_baseball_position (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    grouping TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_stats_position (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    grouping TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_roster_status (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    short_description TEXT,
    is_major BOOLEAN,
    is_minor BOOLEAN,
    is_40_man BOOLEAN,
    is_active_roster BOOLEAN, -- counts against active limit
    is_employee BOOLEAN,
    is_il_status BOOLEAN, -- Inactive List
    is_rehab_status BOOLEAN,
    is_inactive_status BOOLEAN,
    is_injured_status BOOLEAN,
    is_mn_active BOOLEAN,
    is_mn_under_control BOOLEAN,
    is_dl_status BOOLEAN, -- Disabled List
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_level_of_play (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_league (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    name TEXT,
    level_of_play_id INTEGER REFERENCES lk_level_of_play(id),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Org table is fundamental, often referenced
CREATE TABLE lk_org (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    name TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Club table also fundamental
CREATE TABLE lk_club (
    id INTEGER PRIMARY KEY,
    org_id INTEGER REFERENCES lk_org(id),
    league_id INTEGER REFERENCES lk_league(id),
    bam_club_id INTEGER UNIQUE,
    short_name TEXT,
    name TEXT,
    legal_name TEXT,
    city TEXT,
    is_active BOOLEAN,
    ebis1_lkup TEXT,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
COMMENT ON COLUMN lk_club.is_active IS 'Reflects active status as per ClubApi - Lookup `active` field for a specific effective date range.';

CREATE TABLE lk_agency (
    id INTEGER PRIMARY KEY,
    name TEXT,
    phone_number TEXT,
    is_active BOOLEAN,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_agent (
    id INTEGER PRIMARY KEY,
    agency_id INTEGER REFERENCES lk_agency(id),
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    fax_number TEXT,
    is_active BOOLEAN,
    is_certification BOOLEAN,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_phone_number_type (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_address_type (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_email_address_type ( -- Assuming this exists based on pattern
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);


CREATE TABLE lk_national_id_type (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    country_id INTEGER REFERENCES lk_country(id),
    format_pattern TEXT, -- From NationalIdTypeApiSystemValuesV1
    validation_pattern TEXT, -- From NationalIdTypeApiSystemValuesV1
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_immigration_status (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_spoken_language (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_equal_opportunity (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_tx_type (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_tx_name (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    -- details_class_name TEXT, -- Metadata, likely not needed in DB
    -- player_details_class_name TEXT, -- Metadata, likely not needed in DB
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_tx_status (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_mjc_type (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_mjc_status (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_mnc_type (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_mnc_status (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_add_c_status (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_add_d_status (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_award (
    id INTEGER PRIMARY KEY,
    code INTEGER UNIQUE, -- Seems to be numeric in AwardApi - Lookup
    name TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_arbitration_status (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_school (
    id INTEGER PRIMARY KEY,
    name TEXT,
    address1 TEXT,
    address2 TEXT,
    address3 TEXT,
    city TEXT,
    state_id INTEGER REFERENCES lk_state(id),
    zip TEXT,
    country_id INTEGER REFERENCES lk_country(id),
    phone TEXT,
    comments TEXT,
    school_division_id INTEGER, -- Refers to lk_school_division
    school_type_id INTEGER, -- Refers to lk_school_type
    is_active BOOLEAN,
    -- province, district, sector could be added if needed based on address fields
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
-- Need supporting school lookup tables
CREATE TABLE lk_school_type ( id INTEGER PRIMARY KEY, code TEXT UNIQUE, name TEXT );
CREATE TABLE lk_school_division ( id INTEGER PRIMARY KEY, code TEXT UNIQUE, name TEXT, school_type_id INTEGER REFERENCES lk_school_type(id) );
ALTER TABLE lk_school ADD CONSTRAINT fk_school_division FOREIGN KEY (school_division_id) REFERENCES lk_school_division(id);
ALTER TABLE lk_school ADD CONSTRAINT fk_school_type FOREIGN KEY (school_type_id) REFERENCES lk_school_type(id);

CREATE TABLE lk_school_class (
    id INTEGER PRIMARY KEY,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_r4_draft_status ( -- Inferred from DomPlayerDraftHistoryApi
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_amateur_program (
    id INTEGER PRIMARY KEY,
    description TEXT UNIQUE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_intl_program (
    id INTEGER PRIMARY KEY,
    description TEXT UNIQUE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lk_employee_position (
    id INTEGER PRIMARY KEY,
    description TEXT,
    employee_type_id INTEGER, -- Refers to lk_employee_type
    is_mj_roster_position BOOLEAN,
    is_active BOOLEAN,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE lk_employee_type ( id INTEGER PRIMARY KEY, description TEXT UNIQUE );
ALTER TABLE lk_employee_position ADD CONSTRAINT fk_employee_type FOREIGN KEY (employee_type_id) REFERENCES lk_employee_type(id);


-- ... other lookup tables as needed (e.g., body parts, visa types, transaction reasons, bonus types, etc.)


-- =============== CORE TABLES ===============

CREATE TABLE person (
    person_id BIGINT PRIMARY KEY, -- From API path {ebisId}
    person_type_id INTEGER REFERENCES lk_person_type(id),
    -- bio_info_id BIGINT UNIQUE, -- If using separate bio table
    -- baseball_info_id BIGINT UNIQUE, -- If using separate baseball table
    -- etc. for other 1-to-1 info tables
    merged_player_id BIGINT REFERENCES person(person_id), -- Self reference for merged players
    past_pro_player BOOLEAN,
    past_ama BOOLEAN,
    past_player BOOLEAN,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    ebis_updated_timestamp_ms BIGINT, -- Map updatedTimestamp
    ebis_cache_updated_timestamp_ms BIGINT, -- Map cacheUpdatedTimestamp
    ebis_service_updated_timestamp_ms BIGINT -- Map updatedServiceTimestamp
);
COMMENT ON COLUMN person.person_id IS 'Corresponds to ebisId in the API paths.';

-- Example of breaking out complex nested objects (optional, alternative is embedding)
CREATE TABLE person_bio_info (
    person_id BIGINT PRIMARY KEY REFERENCES person(person_id) ON DELETE CASCADE,
    last_name TEXT,
    first_name TEXT,
    middle_name TEXT,
    extended_last_name TEXT,
    roster_first_name TEXT,
    birthdate DATE,
    birth_city_id INTEGER REFERENCES lk_city(id),
    birth_state_id INTEGER REFERENCES lk_state(id),
    birth_province_id INTEGER REFERENCES lk_province(id),
    birth_district_id INTEGER REFERENCES lk_district(id),
    birth_sector_id INTEGER REFERENCES lk_sector(id),
    birth_country_id INTEGER REFERENCES lk_country(id),
    spoken_lang_id INTEGER REFERENCES lk_spoken_language(id),
    gender TEXT, -- Could be ENUM('M', 'F', 'O') or similar
    former_identity TEXT,
    equal_opportunity_id INTEGER REFERENCES lk_equal_opportunity(id),
    reason_for_name_birth_change TEXT,
    sounds_like TEXT,
    mother_name TEXT,
    father_name TEXT,
    is_twin BOOLEAN
    -- No separate updated timestamps here, assume tied to parent person record
);

CREATE TABLE person_baseball_info (
    person_id BIGINT PRIMARY KEY REFERENCES person(person_id) ON DELETE CASCADE,
    player_position_id INTEGER REFERENCES lk_baseball_position(id),
    stats_position_id INTEGER REFERENCES lk_stats_position(id),
    secondary_position_id INTEGER REFERENCES lk_baseball_position(id),
    height_inches INTEGER, -- Assuming height is stored in inches
    weight_lbs INTEGER, -- Assuming weight is stored in lbs
    uniform_number TEXT,
    batting_side TEXT, -- Could be ENUM('R', 'L', 'S')
    throwing_side TEXT, -- Could be ENUM('R', 'L')
    is_on_40_man_roster BOOLEAN,
    is_on_roster BOOLEAN, -- General flag if on *any* roster
    is_on_major_league_roster BOOLEAN,
    is_on_minor_league_roster BOOLEAN,
    first_pro_contract_date DATE,
    first_pro_contract_club_id INTEGER REFERENCES lk_club(id),
    first_ml_acquisition_org_id INTEGER REFERENCES lk_org(id),
    first_ml_acquisition_date DATE,
    first_ml_acquisition_from_club_id INTEGER REFERENCES lk_club(id), -- Might be outside MLB/affiliated system
    first_ml_report_org_id INTEGER REFERENCES lk_org(id),
    first_ml_club_report_date DATE,
    current_ml_acquisition_org_id INTEGER REFERENCES lk_org(id),
    current_ml_acquisition_date DATE,
    current_ml_acquired_from_club_id INTEGER REFERENCES lk_club(id), -- Might be outside MLB/affiliated system
    current_ml_report_org_id INTEGER REFERENCES lk_org(id),
    current_ml_club_report_date DATE,
    is_disqualified BOOLEAN,
    is_two_way_player BOOLEAN,
    is_club_player_pool BOOLEAN,
    is_non_roster_invitee BOOLEAN
);

-- One-to-many tables related to Person
CREATE TABLE person_agent (
    person_agent_id BIGSERIAL PRIMARY KEY,
    person_id BIGINT NOT NULL REFERENCES person(person_id) ON DELETE CASCADE,
    agent_id INTEGER REFERENCES lk_agent(id),
    agency_id INTEGER REFERENCES lk_agency(id),
    sequence_number INTEGER -- If order matters
);

CREATE TABLE person_phone_number (
    person_phone_number_id BIGSERIAL PRIMARY KEY,
    person_id BIGINT NOT NULL REFERENCES person(person_id) ON DELETE CASCADE,
    phone_number_type_id INTEGER REFERENCES lk_phone_number_type(id),
    country_id INTEGER REFERENCES lk_country(id),
    phone_number TEXT,
    sequence_number INTEGER
);

CREATE TABLE person_email_address (
    person_email_address_id BIGSERIAL PRIMARY KEY,
    person_id BIGINT NOT NULL REFERENCES person(person_id) ON DELETE CASCADE,
    email_address_type_id INTEGER REFERENCES lk_email_address_type(id),
    email_address TEXT,
    sequence_number INTEGER
);

CREATE TABLE person_address (
    person_address_id BIGSERIAL PRIMARY KEY,
    person_id BIGINT NOT NULL REFERENCES person(person_id) ON DELETE CASCADE,
    address_type_id INTEGER REFERENCES lk_address_type(id),
    address1 TEXT,
    address2 TEXT,
    address3 TEXT,
    city TEXT, -- Store text value as provided
    city_id INTEGER REFERENCES lk_city(id),
    state_id INTEGER REFERENCES lk_state(id),
    state_code TEXT, -- Store text value as provided
    zip TEXT,
    country_id INTEGER REFERENCES lk_country(id),
    country_name TEXT, -- Store text value as provided
    province_id INTEGER REFERENCES lk_province(id),
    province_name TEXT,
    district_id INTEGER REFERENCES lk_district(id),
    district_name TEXT,
    sector_id INTEGER REFERENCES lk_sector(id),
    sector_name TEXT,
    sequence_number INTEGER
);

CREATE TABLE person_national_id (
    person_national_id BIGSERIAL PRIMARY KEY,
    person_id BIGINT NOT NULL REFERENCES person(person_id) ON DELETE CASCADE,
    national_id_type_id INTEGER REFERENCES lk_national_id_type(id),
    national_id_country_id INTEGER REFERENCES lk_country(id),
    id_number TEXT
);

CREATE TABLE person_visa_info ( -- From InternationalInformationApi
    person_id BIGINT PRIMARY KEY REFERENCES person(person_id) ON DELETE CASCADE,
    has_visa BOOLEAN,
    is_renewal_pending BOOLEAN,
    granted_date DATE,
    expiration_date DATE,
    visa_type TEXT,
    immigration_status_id INTEGER REFERENCES lk_immigration_status(id),
    needed_waiver BOOLEAN,
    general_comments TEXT
);

-- Embed simpler status info directly into person or related tables
ALTER TABLE person ADD COLUMN current_org_id INTEGER REFERENCES lk_org(id);
ALTER TABLE person ADD COLUMN current_club_id INTEGER REFERENCES lk_club(id);
ALTER TABLE person ADD COLUMN rehab_club_id INTEGER REFERENCES lk_club(id);
ALTER TABLE person ADD COLUMN mj_roster_status_id INTEGER REFERENCES lk_roster_status(id);
ALTER TABLE person ADD COLUMN mn_roster_status_id INTEGER REFERENCES lk_roster_status(id);
-- ... add other PlayerProfileHeader fields
ALTER TABLE person ADD COLUMN outright_waiver_good_until_date DATE;
ALTER TABLE person ADD COLUMN is_outright_waiver_in_effect BOOLEAN;
-- ... add other waiver, IL, option, outright fields

-- Domestic Amateur Info (Linked to Person)
CREATE TABLE person_dom_info (
    person_id BIGINT PRIMARY KEY REFERENCES person(person_id) ON DELETE CASCADE,
    draft_prospect_link INTEGER,
    eligibility_comments TEXT,
    is_top_player BOOLEAN,
    is_over_21_eligible BOOLEAN,
    is_not_subject_to_deadline BOOLEAN,
    draft_agent_id INTEGER REFERENCES lk_agent(id),
    draft_agency_id INTEGER REFERENCES lk_agency(id)
);

CREATE TABLE person_dom_positions ( -- From DomPlayerInfoApi.positions
    person_dom_position_id BIGSERIAL PRIMARY KEY,
    person_id BIGINT NOT NULL REFERENCES person_dom_info(person_id) ON DELETE CASCADE,
    player_position_id INTEGER REFERENCES lk_baseball_position(id),
    sequence INTEGER
);

CREATE TABLE person_dom_letter_of_intent ( -- From DomPlayerInfoApi.letterOfIntent
    person_id BIGINT PRIMARY KEY REFERENCES person_dom_info(person_id) ON DELETE CASCADE,
    school_id INTEGER REFERENCES lk_school(id),
    school_display_name TEXT,
    school_state TEXT,
    school_city TEXT,
    school_type TEXT -- Could link to lk_school_type if consistent
);

CREATE TABLE person_dom_draft_history ( -- From DomPlayerInfoApi.draftHistory
    dom_draft_history_id BIGSERIAL PRIMARY KEY, -- amaDraftEligibleId is likely internal
    person_id BIGINT NOT NULL REFERENCES person_dom_info(person_id) ON DELETE CASCADE,
    draft_year INTEGER,
    draft_number INTEGER,
    is_redraft BOOLEAN,
    school_id INTEGER REFERENCES lk_school(id),
    school_display_name TEXT,
    school_state TEXT,
    draft_position_id INTEGER REFERENCES lk_baseball_position(id),
    school_class_id INTEGER REFERENCES lk_school_class(id),
    school_type_id INTEGER REFERENCES lk_school_type(id),
    r4_draft_status_id INTEGER REFERENCES lk_r4_draft_status(id),
    r4_origin TEXT,
    drafting_org_id INTEGER REFERENCES lk_org(id),
    draft_round TEXT,
    pick_in_round INTEGER,
    overall_pick INTEGER,
    has_consent BOOLEAN,
    consent_status TEXT
    -- Ignoring schoolInfo and submissions for brevity, structure similar to above if needed
);

CREATE TABLE person_dom_program_participation (
    person_dom_program_participation_id BIGSERIAL PRIMARY KEY,
    person_id BIGINT NOT NULL REFERENCES person_dom_info(person_id) ON DELETE CASCADE,
    amateur_program_id INTEGER REFERENCES lk_amateur_program(id),
    participation_years INTEGER[] -- Array of years
);

CREATE TABLE person_intl_program_participation (
    person_intl_program_participation_id BIGSERIAL PRIMARY KEY,
    person_id BIGINT NOT NULL REFERENCES person(person_id) ON DELETE CASCADE, -- Link directly to person if not nested under dom_info
    intl_program_id INTEGER REFERENCES lk_intl_program(id),
    participation_years INTEGER[]
);

-- Service Info (Complex - requires multiple tables or careful embedding)
CREATE TABLE person_service_info (
    person_id BIGINT PRIMARY KEY REFERENCES person(person_id) ON DELETE CASCADE,
    total_mls_years INTEGER,
    total_mls_days INTEGER,
    opening_day_mls_years INTEGER,
    opening_day_mls_days INTEGER,
    prior_season_service_years INTEGER,
    prior_season_service_days INTEGER,
    current_club_mls_years INTEGER,
    current_club_mls_days INTEGER,
    current_season_service_years INTEGER,
    current_season_service_days INTEGER,
    super_two_year INTEGER,
    rookie_milestone_date DATE,
    is_rookie BOOLEAN,
    three_year_date DATE,
    is_three_year BOOLEAN,
    five_year_date DATE,
    is_five_year BOOLEAN,
    six_year_date DATE,
    is_six_year BOOLEAN,
    ten_five_player_date DATE,
    is_ten_five_player BOOLEAN,
    mn_contract_years INTEGER,
    mn_service_years INTEGER,
    is_potential_mn_lg_fa BOOLEAN,
    potential_mn_lg_fa_year INTEGER,
    dsl_vsl_service_years INTEGER,
    domestic_service_years INTEGER,
    highest_level_of_play_id INTEGER REFERENCES lk_level_of_play(id),
    mlb_comment TEXT
);

CREATE TABLE person_mj_league_summary (
    person_mj_league_summary_id BIGSERIAL PRIMARY KEY,
    person_id BIGINT NOT NULL REFERENCES person_service_info(person_id) ON DELETE CASCADE,
    service_year INTEGER,
    effective_date DATE,
    club_code TEXT, -- Assuming this maps to org code or club code
    days_with_club INTEGER,
    adjustments INTEGER,
    days_towards_172 INTEGER,
    total_season_service INTEGER,
    total_mls_per_year_years INTEGER,
    total_mls_per_year_days INTEGER,
    sequence_number INTEGER,
    comments TEXT,
    days_with_club_actual INTEGER,
    days_towards_172_actual INTEGER,
    dues_days INTEGER
);

CREATE TABLE person_mn_league_summary (
    person_mn_league_summary_id BIGSERIAL PRIMARY KEY,
    person_id BIGINT NOT NULL REFERENCES person_service_info(person_id) ON DELETE CASCADE,
    roster_year INTEGER,
    effective_date DATE,
    service_days INTEGER,
    days_aaa INTEGER,
    days_aa INTEGER,
    days_a1 INTEGER,
    days_f1 INTEGER, -- Short A?
    days_sa INTEGER, -- Rookie Advanced?
    days_ra INTEGER, -- Rookie?
    days_rr INTEGER, -- Complex League Rookie?
    days_dsl INTEGER,
    days_vsl INTEGER,
    days_asl INTEGER,
    org_code TEXT -- Org code for the summary line
);

CREATE TABLE person_yearly_service_days (
    person_yearly_service_days_id BIGSERIAL PRIMARY KEY,
    person_id BIGINT NOT NULL REFERENCES person_service_info(person_id) ON DELETE CASCADE,
    service_year INTEGER,
    org_id INTEGER REFERENCES lk_org(id),
    sequence_number INTEGER,
    il_days INTEGER,
    option_days INTEGER,
    outright_days INTEGER
);

-- Major Contract (MJC)
CREATE TABLE mjc (
    mjc_id BIGINT PRIMARY KEY, -- From API path {mjcId}
    person_id BIGINT NOT NULL REFERENCES person(person_id),
    mjc_type_id INTEGER REFERENCES lk_mjc_type(id),
    current_contract_status_id INTEGER REFERENCES lk_mjc_status(id),
    is_settlement BOOLEAN,
    start_year INTEGER,
    option_years INTEGER,
    non_option_years INTEGER,
    signed_date DATE,
    approved_timestamp TIMESTAMPTZ,
    terminated_timestamp TIMESTAMPTZ,
    expiration_timestamp TIMESTAMPTZ,
    void_timestamp TIMESTAMPTZ,
    superceded_timestamp TIMESTAMPTZ,
    confirmed_date DATE,
    status_timestamp TIMESTAMPTZ,
    signing_org_id INTEGER REFERENCES lk_org(id),
    current_org_id INTEGER REFERENCES lk_org(id),
    agent_id INTEGER REFERENCES lk_agent(id),
    agency_id INTEGER REFERENCES lk_agency(id),
    auth_signatory_id INTEGER, -- Needs lookup table lk_auth_signatory
    life_insurance_signed_date DATE,
    comments TEXT,
    mlb_comment TEXT,
    confirmed_event_id INTEGER, -- Link to transaction table?
    terminated_event_id INTEGER,
    expired_event_id INTEGER,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    ebis_updated_timestamp_ms BIGINT,
    ebis_cache_updated_timestamp_ms BIGINT
);

-- Tables for MJC nested structures (Compensation, Bonuses, Options, etc.)
CREATE TABLE mjc_mj_compensation (
    mjc_mj_compensation_id BIGSERIAL PRIMARY KEY,
    mjc_id BIGINT NOT NULL REFERENCES mjc(mjc_id) ON DELETE CASCADE,
    year INTEGER NOT NULL,
    base_salary NUMERIC,
    guaranteed_salary NUMERIC,
    other_salary NUMERIC,
    lrd_salary NUMERIC,
    lrd_salary_no_bonus NUMERIC,
    non_guaranteed_salary NUMERIC,
    earned_bonus_amount NUMERIC, -- Sum of earned bonuses for the year
    offered_award_bonus_amount NUMERIC,
    offered_perf_bonus_amount NUMERIC,
    offered_other_bonus_amount NUMERIC,
    offered_escalator_amount NUMERIC,
    earned_award_bonus_amount NUMERIC,
    earned_perf_bonus_amount NUMERIC,
    earned_other_bonus_amount NUMERIC,
    earned_escalator_amount NUMERIC,
    base_salary_adjusted NUMERIC, -- Adjusted values if applicable
    guaranteed_salary_adjusted NUMERIC,
    lrd_salary_adjusted NUMERIC,
    lrd_salary_no_bonus_adjusted NUMERIC,
    earned_bonus_amount_adjusted NUMERIC,
    prorate_signing_bonus_flag BOOLEAN,
    UNIQUE (mjc_id, year)
);
-- Further breakdown for pay schedules per year might be needed if MjcPaySchedulesApi varies by year

CREATE TABLE mjc_mn_compensation (
    mjc_mn_compensation_id BIGSERIAL PRIMARY KEY,
    mjc_id BIGINT NOT NULL REFERENCES mjc(mjc_id) ON DELETE CASCADE,
    year INTEGER NOT NULL,
    level_of_play_id INTEGER NOT NULL REFERENCES lk_level_of_play(id),
    salary NUMERIC,
    UNIQUE (mjc_id, year, level_of_play_id)
);

-- Need tables for Bonuses (Award, Performance, Other, Signing, Escalators) and Options
-- Structure will be complex, involving terms, thresholds, pay schedules. Example for Signing Bonus:
CREATE TABLE mjc_signing_bonus (
    mjc_signing_bonus_id BIGSERIAL PRIMARY KEY,
    mjc_id BIGINT NOT NULL REFERENCES mjc(mjc_id) ON DELETE CASCADE,
    bonus_amount NUMERIC, -- Total nominal amount
    days_from_approval INTEGER,
    language_id INTEGER, -- Needs lk_contract_language table
    comments TEXT
);

CREATE TABLE mjc_pay_schedule (
    mjc_pay_schedule_id BIGSERIAL PRIMARY KEY,
    mjc_id BIGINT NOT NULL REFERENCES mjc(mjc_id) ON DELETE CASCADE,
    related_bonus_id INTEGER, -- FK to specific bonus table (e.g., mjc_signing_bonus) - Polymorphic or separate tables?
    related_option_id INTEGER, -- FK to option table
    related_buyout_option_id INTEGER, -- FK to option table (for buyout)
    related_compensation_year INTEGER, -- Link to mjc_mj_compensation (mjc_id, year)
    payment_date DATE,
    within_days_of_earning INTEGER,
    accrual_date DATE,
    earned_date DATE,
    principal_amount NUMERIC,
    payment_amount NUMERIC,
    lrd_present_value NUMERIC,
    principal_amount_adjusted NUMERIC,
    payment_amount_adjusted NUMERIC,
    lrd_present_value_adjusted NUMERIC,
    cbt_present_value NUMERIC,
    interest_rate NUMERIC,
    compounding_type_id INTEGER -- Needs lk_compounding_type
);
-- Need bonus tables (mjc_award_bonus, mjc_performance_bonus, mjc_other_bonus, mjc_salary_escalator)
-- Need option tables (mjc_option_clause)
-- Need covenant tables (mjc_covenant - potentially complex structure)
-- Need file attachment tables (mjc_file_attachment, mjc_file_attachment_type_link, lk_file_attachment_type)


-- Minor Contract (MNC)
CREATE TABLE mnc (
    mnc_id BIGINT PRIMARY KEY, -- From API path {mncId}
    person_id BIGINT NOT NULL REFERENCES person(person_id),
    mnc_type_id INTEGER REFERENCES lk_mnc_type(id),
    mnc_status_id INTEGER REFERENCES lk_mnc_status(id),
    agent_id INTEGER REFERENCES lk_agent(id),
    agency_id INTEGER REFERENCES lk_agency(id),
    name_on_contract TEXT,
    signed_as_id INTEGER, -- Needs lookup table?
    street_address TEXT, -- Should be normalized into address table? API shows flat string.
    city_state_country_zip TEXT, -- Should be normalized? API shows flat string.
    execution_negotiator_primary_id INTEGER,
    execution_negotiator_secondary_id INTEGER,
    execution_auth_signatory_id INTEGER,
    execution_parental_consent_id INTEGER, -- Needs lk_mnc_parental_consent
    execution_consent_country_id INTEGER REFERENCES lk_country(id),
    execution_consent_city TEXT,
    execution_signed_country_id INTEGER REFERENCES lk_country(id),
    execution_signed_city TEXT,
    execution_signed_state_id INTEGER REFERENCES lk_state(id),
    comments TEXT,
    status_last_changed_timestamp TIMESTAMPTZ,
    approved_timestamp TIMESTAMPTZ,
    submitted_timestamp TIMESTAMPTZ,
    state_reason_id INTEGER, -- Needs lookup (e.g., lk_mnc_state_reason)
    body_part_id INTEGER, -- Needs lk_body_part
    body_part_detail_id INTEGER, -- Needs lk_body_part_detail
    diagnosis_id INTEGER, -- Needs lk_diagnosis
    life_insurance_status_id INTEGER, -- Needs lk_mnc_life_insurance_status
    life_insurance_signed_date DATE,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    ebis_updated_timestamp_ms BIGINT,
    ebis_cache_updated_timestamp_ms BIGINT
);

-- Tables for MNC nested structures (Addendums A, B, C, E, F, G, H, MexAssign)
CREATE TABLE mnc_addendum_a (
    mnc_id BIGINT PRIMARY KEY REFERENCES mnc(mnc_id) ON DELETE CASCADE,
    beginning_in_year INTEGER,
    num_seasons INTEGER,
    terms_agreed_upon_date DATE,
    signed_date DATE,
    is_successor_contract BOOLEAN,
    org_id INTEGER REFERENCES lk_org(id),
    club_id INTEGER REFERENCES lk_club(id)
    -- Roster limit fields seem informational, not stored unless needed for history
);

CREATE TABLE mnc_addendum_b ( -- Represents various clauses linked by type
    add_b_id BIGSERIAL PRIMARY KEY,
    mnc_id BIGINT NOT NULL REFERENCES mnc(mnc_id) ON DELETE CASCADE,
    add_b_type_id INTEGER NOT NULL, -- Needs lk_add_b_type
    language_id INTEGER, -- Needs lk_contract_language
    language_label TEXT,
    language_data TEXT, -- Stores the specific clause text/data
    -- Clause-specific fields would ideally be in separate tables inheriting/linking from this
    -- E.g., mnc_add_b_signing_bonus, mnc_add_b_college_scholarship, etc.
    -- Storing everything in language_data might be simpler initially if parsing isn't required.
    UNIQUE (mnc_id, add_b_type_id) -- Assuming one clause of each type per MNC
);

-- Addendum C (Separate top-level entity in API)
CREATE TABLE add_c (
    add_c_id BIGINT PRIMARY KEY, -- From API path {addCId}
    person_id BIGINT NOT NULL REFERENCES person(person_id),
    mnc_id BIGINT REFERENCES mnc(mnc_id), -- Can AddC exist without MNC? API suggests yes by path. Nullable FK.
    add_c_year INTEGER,
    minor_league_club_id INTEGER REFERENCES lk_club(id),
    contract_years_remaining INTEGER,
    auth_signatory_id INTEGER, -- Needs lk_auth_signatory
    add_c_status_id INTEGER REFERENCES lk_add_c_status(id),
    tendered_timestamp TIMESTAMPTZ,
    pending_timestamp TIMESTAMPTZ,
    approved_timestamp TIMESTAMPTZ,
    signed_date DATE,
    is_valid_for_service BOOLEAN,
    additional_text TEXT,
    contract_flag BOOLEAN, -- Meaning?
    org_id INTEGER REFERENCES lk_org(id), -- Which org? Signing? Current?
    signed_country_id INTEGER REFERENCES lk_country(id),
    signed_state_id INTEGER REFERENCES lk_state(id),
    signed_city TEXT,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    ebis_updated_timestamp_ms BIGINT,
    ebis_cache_updated_timestamp_ms BIGINT
);

CREATE TABLE add_c_salary (
    add_c_salary_id BIGSERIAL PRIMARY KEY,
    add_c_id BIGINT NOT NULL REFERENCES add_c(add_c_id) ON DELETE CASCADE,
    level_of_play_id INTEGER NOT NULL REFERENCES lk_level_of_play(id),
    previous_salary NUMERIC,
    monthly_salary NUMERIC,
    sequence_number INTEGER -- Order/priority?
    -- AddCClubApi seems informational about the club for that level, not stored here directly
);


-- Addendum D (Separate top-level entity)
CREATE TABLE add_d (
    add_d_id BIGINT PRIMARY KEY, -- From API path {addDId}
    mnc_id BIGINT REFERENCES mnc(mnc_id), -- Can AddD exist without MNC? API suggests yes.
    person_id BIGINT NOT NULL REFERENCES person(person_id),
    year INTEGER,
    league_id INTEGER REFERENCES lk_league(id),
    club_id INTEGER REFERENCES lk_club(id),
    signed_date DATE,
    monthly_salary NUMERIC,
    current_status_id INTEGER REFERENCES lk_add_d_status(id),
    auth_sig_id INTEGER, -- Needs lk_auth_signatory
    submitted_timestamp TIMESTAMPTZ,
    approved_timestamp TIMESTAMPTZ,
    org_id INTEGER REFERENCES lk_org(id),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    ebis_updated_timestamp_ms BIGINT,
    ebis_cache_updated_timestamp_ms BIGINT
);


-- Transaction (TX)
CREATE TABLE transaction (
    tx_id BIGINT PRIMARY KEY, -- From API path {txId}
    tx_type_id INTEGER REFERENCES lk_tx_type(id),
    tx_name_id INTEGER REFERENCES lk_tx_name(id),
    tx_date DATE,
    current_status_id INTEGER REFERENCES lk_tx_status(id),
    submitted_timestamp TIMESTAMPTZ,
    approved_timestamp TIMESTAMPTZ,
    status_changed_timestamp TIMESTAMPTZ,
    is_safe_harbor BOOLEAN,
    comments TEXT,
    is_major_transaction BOOLEAN,
    event_id INTEGER, -- Optional: link to event system if exists
    -- Detail fields need separate tables based on TxDetailApi discriminator (@class)
    -- e.g., tx_detail_generic, tx_detail_trade, tx_detail_dl_placement, tx_detail_rehab, etc.
    -- Each detail table would have tx_id as FK.
    auth_signatory_id INTEGER, -- Common detail field, could be here or in detail tables
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    ebis_updated_timestamp_ms BIGINT,
    ebis_cache_updated_timestamp_ms BIGINT
);

CREATE TABLE transaction_player_detail (
    tx_player_detail_id BIGSERIAL PRIMARY KEY,
    tx_id BIGINT NOT NULL REFERENCES transaction(tx_id) ON DELETE CASCADE,
    person_id BIGINT NOT NULL REFERENCES person(person_id),
    prior_org_id INTEGER REFERENCES lk_org(id),
    post_org_id INTEGER REFERENCES lk_org(id),
    prior_club_id INTEGER REFERENCES lk_club(id),
    post_club_id INTEGER REFERENCES lk_club(id),
    prior_mj_roster_status_id INTEGER REFERENCES lk_roster_status(id),
    post_mj_roster_status_id INTEGER REFERENCES lk_roster_status(id),
    prior_mn_roster_status_id INTEGER REFERENCES lk_roster_status(id),
    post_mn_roster_status_id INTEGER REFERENCES lk_roster_status(id),
    transaction_date_mls_years INTEGER, -- From MlsDetailsV1
    transaction_date_mls_days INTEGER, -- From MlsDetailsV1
    opening_day_mls_years INTEGER,
    opening_day_mls_days INTEGER,
    opening_day_mls_year INTEGER,
    mlb_comment TEXT
);

-- Example Detail Table (Generic - others follow pattern)
CREATE TABLE tx_detail_generic (
    tx_id BIGINT PRIMARY KEY REFERENCES transaction(tx_id) ON DELETE CASCADE
    -- No specific fields in TxGenericDetailApi beyond common auth signatory
);

CREATE TABLE tx_detail_mj_dl ( -- For TxMjDlDetailApi
    tx_id BIGINT PRIMARY KEY REFERENCES transaction(tx_id) ON DELETE CASCADE,
    ailment_id INTEGER, -- Needs lookup
    body_part_id INTEGER, -- Needs lookup
    body_part_detail_id INTEGER, -- Needs lookup
    body_side_id INTEGER, -- Needs lookup
    diagnosis_id INTEGER, -- Needs lookup
    injury_sustained_id INTEGER, -- Needs lookup
    country_id INTEGER REFERENCES lk_country(id),
    state_id INTEGER REFERENCES lk_state(id),
    is_ailment BOOLEAN,
    is_double_header_exception BOOLEAN,
    received_sfd BOOLEAN,
    earliest_reinstatement_date DATE,
    exam_date DATE,
    injury_date DATE,
    last_game_date DATE,
    roster_affected_date DATE
);
-- Similar tables for TxMjIlDetailApi, TxMnDlDetailApi, TxMnIlDetailApi, TxConcDlDetailApi, TxConcIlDetailApi, TxRestrDetailApi, etc.

CREATE TABLE tx_detail_trade ( -- Example for a more complex one like trade (structure not fully defined in snippet)
    tx_id BIGINT PRIMARY KEY REFERENCES transaction(tx_id) ON DELETE CASCADE,
    -- Fields related to trade specifics, potentially including considerations
    cash_consideration NUMERIC
    -- May need links back to transaction_player_detail for players involved in specific ways (e.g., PTBNL)
);

CREATE TABLE tx_detail_ptbnl ( -- For TxPtbnlDetailApi
    tx_id BIGINT PRIMARY KEY REFERENCES transaction(tx_id) ON DELETE CASCADE,
    -- Note: PTBNL usually involves *which* player is PTBNL, linking back might be complex
    ptbnl_person_id BIGINT REFERENCES person(person_id), -- The player to be named?
    ptbnl_player_name TEXT, -- If ID unknown initially
    ptbnl_position_id INTEGER REFERENCES lk_baseball_position(id),
    on_before_date DATE,
    alternate_cash_consideration NUMERIC,
    competitive_balance_amount NUMERIC
    -- receivedInsForm seems misplaced here, maybe status related?
);

-- Transaction Bulletin
CREATE TABLE tx_bulletin (
    bulletin_id BIGINT PRIMARY KEY, -- From API path
    bulletin_date DATE,
    comments TEXT,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    ebis_updated_timestamp_ms BIGINT,
    ebis_cache_updated_timestamp_ms BIGINT
);

CREATE TABLE tx_bulletin_detail (
    bulletin_detail_id BIGSERIAL PRIMARY KEY, -- API uses bulletinDetailId, assuming it's unique within bulletin
    bulletin_id BIGINT NOT NULL REFERENCES tx_bulletin(bulletin_id) ON DELETE CASCADE,
    tx_id BIGINT REFERENCES transaction(tx_id), -- Link to the specific transaction
    person_id BIGINT REFERENCES person(person_id), -- Player involved
    org_code TEXT, -- Denormalized org code
    player_name TEXT, -- Denormalized name
    position_code TEXT, -- Denormalized position
    mls_display TEXT, -- Denormalized MLS (e.g., "1.034")
    description TEXT, -- Bulletin line description
    tx_date DATE, -- Denormalized tx date
    approved_date DATE, -- Denormalized approved date
    mlb_comment TEXT
);

-- Arbitration
CREATE TABLE arbitration (
    arbitration_id BIGINT PRIMARY KEY, -- From API path
    person_id BIGINT NOT NULL REFERENCES person(person_id),
    arbitration_org_id INTEGER REFERENCES lk_org(id),
    arbitration_year INTEGER NOT NULL,
    arbitration_status_id INTEGER REFERENCES lk_arbitration_status(id),
    exchange_date DATE,
    end_of_season_mls TEXT, -- Store as text "Y.DDD"
    eligibility_count INTEGER,
    is_tender BOOLEAN,
    club_offer NUMERIC,
    player_offer NUMERIC,
    club_practitioner_id1 INTEGER, -- Needs lk_arb_practitioner table
    club_practitioner_id2 INTEGER,
    player_practitioner_id1 INTEGER,
    player_practitioner_id2 INTEGER,
    hearing_location TEXT,
    position_id INTEGER REFERENCES lk_baseball_position(id),
    hearing_timestamp TIMESTAMPTZ,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    ebis_updated_timestamp_ms BIGINT,
    ebis_cache_updated_timestamp_ms BIGINT
);

CREATE TABLE arbitration_assigned_arbitrator (
    arbitration_assigned_arbitrator_id BIGSERIAL PRIMARY KEY,
    arbitration_id BIGINT NOT NULL REFERENCES arbitration(arbitration_id) ON DELETE CASCADE,
    arbitrator_id INTEGER NOT NULL, -- Needs lk_arbitrator table
    is_chair BOOLEAN,
    arbitrator_decision_id INTEGER -- Needs lk_arbitrator_decision table
);

-- Award
CREATE TABLE award (
    award_id BIGINT PRIMARY KEY, -- From API path
    award_code INTEGER REFERENCES lk_award(code), -- Link to lookup table via code
    league TEXT, -- AL/NL? Could be normalized.
    position TEXT, -- Specific position for award? Could link to lk_baseball_position
    year INTEGER NOT NULL,
    total_votes_cast INTEGER,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(), -- API has createdTimestamp
    updated_at TIMESTAMPTZ DEFAULT now(),
    ebis_updated_timestamp_ms BIGINT,
    ebis_cache_updated_timestamp_ms BIGINT
);

CREATE TABLE award_vote (
    award_vote_id BIGSERIAL PRIMARY KEY,
    award_id BIGINT NOT NULL REFERENCES award(award_id) ON DELETE CASCADE,
    person_id BIGINT NOT NULL REFERENCES person(person_id),
    votes INTEGER,
    place INTEGER -- Finishing place (1st, 2nd, etc.)
);

-- CEP / CSP (Continuing Education Program / College Scholarship Plan)
-- Structure seems very similar, maybe combine or use inheritance if supported well.
-- Using separate tables for clarity based on API structure.

CREATE TABLE cep (
    cep_id BIGSERIAL PRIMARY KEY,
    person_id BIGINT NOT NULL REFERENCES person(person_id),
    mnc_id BIGINT REFERENCES mnc(mnc_id), -- Optional link to originating contract
    status_id INTEGER, -- Needs lk_cep_csp_status
    responsible_org_id INTEGER REFERENCES lk_org(id),
    tuition_allowance_commitment NUMERIC,
    living_allowance_commitment NUMERIC,
    living_allowance_expiration_date DATE,
    tuition_allowance_used NUMERIC,
    living_allowance_used NUMERIC,
    comments TEXT,
    signed_date DATE,
    tuition_allowance_completed_date DATE,
    living_allowance_completed_date DATE,
    lapsed_date DATE,
    last_ind_foreign_roster_date DATE, -- For CEP only
    is_deleted BOOLEAN DEFAULT FALSE, -- Assumed based on other patterns
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    ebis_updated_timestamp_ms BIGINT,
    ebis_cache_updated_timestamp_ms BIGINT
);

CREATE TABLE cep_payment_history (
    cep_payment_history_id BIGSERIAL PRIMARY KEY,
    cep_id BIGINT NOT NULL REFERENCES cep(cep_id) ON DELETE CASCADE,
    paid_to TEXT,
    status_id INTEGER, -- Needs lk_cep_csp_invoice_status
    gross_amount NUMERIC,
    net_amount NUMERIC,
    check_number TEXT,
    tuition_amount NUMERIC,
    fees_amount NUMERIC,
    books_amount NUMERIC,
    living_amount NUMERIC,
    start_date DATE,
    end_date DATE,
    check_date DATE,
    payment_mailed_date DATE
);

CREATE TABLE csp (
    csp_id BIGSERIAL PRIMARY KEY,
    person_id BIGINT NOT NULL REFERENCES person(person_id),
    mnc_id BIGINT REFERENCES mnc(mnc_id),
    status_id INTEGER, -- Needs lk_cep_csp_status
    responsible_org_id INTEGER REFERENCES lk_org(id),
    tuition_allowance_commitment_semesters NUMERIC, -- From CSP Tuition Allowance
    tuition_allowance_commitment_per_semester NUMERIC,
    tuition_allowance_commitment_quarters NUMERIC,
    tuition_allowance_commitment_per_quarter NUMERIC,
    tuition_allowance_commitment_total NUMERIC,
    tuition_allowance_ibp_offset NUMERIC,
    living_allowance_commitment_semesters NUMERIC, -- From CSP Living Commitment
    living_allowance_commitment_per_semester NUMERIC,
    living_allowance_commitment_quarters NUMERIC,
    living_allowance_commitment_per_quarter NUMERIC,
    living_allowance_commitment_total NUMERIC,
    living_allowance_expiration_date DATE,
    tuition_allowance_used_semesters NUMERIC, -- From CSP Allowance Used
    tuition_allowance_used_per_semester NUMERIC,
    tuition_allowance_used_quarters NUMERIC,
    tuition_allowance_used_per_quarter NUMERIC,
    tuition_allowance_used_total NUMERIC,
    living_allowance_used_semesters NUMERIC,
    living_allowance_used_per_semester NUMERIC,
    living_allowance_used_quarters NUMERIC,
    living_allowance_used_per_quarter NUMERIC,
    living_allowance_used_total NUMERIC,
    comments TEXT,
    signed_date DATE,
    tuition_allowance_completed_date DATE,
    living_allowance_completed_date DATE,
    lapsed_date DATE,
    is_deleted BOOLEAN DEFAULT FALSE, -- Assumed
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    ebis_updated_timestamp_ms BIGINT,
    ebis_cache_updated_timestamp_ms BIGINT
);

CREATE TABLE csp_payment_history (
    csp_payment_history_id BIGSERIAL PRIMARY KEY,
    csp_id BIGINT NOT NULL REFERENCES csp(csp_id) ON DELETE CASCADE,
    year INTEGER,
    period_id INTEGER, -- Needs lk_csp_period
    period_type_id INTEGER, -- Needs lk_csp_period_type
    paid_to TEXT,
    status_id INTEGER, -- Needs lk_cep_csp_invoice_status
    gross_amount NUMERIC,
    net_amount NUMERIC,
    check_number TEXT,
    credits NUMERIC,
    tuition_amount NUMERIC,
    fees_amount NUMERIC,
    books_amount NUMERIC,
    living_amount NUMERIC,
    check_date DATE,
    payment_mailed_date DATE
);

-- Minor Bonus Payment Tracking (separate from MNC Addendum B bonuses)
CREATE TABLE minor_bonus_payment (
    mnc_bonus_payment_tracking_id BIGINT PRIMARY KEY, -- From API path? Or just ID? Let's assume it's the ID.
    mnc_id BIGINT REFERENCES mnc(mnc_id), -- Optional link to contract
    person_id BIGINT NOT NULL REFERENCES person(person_id),
    status_id INTEGER, -- Needs lookup (e.g., lk_bonus_payment_status)
    bonus_type_id INTEGER, -- Needs lookup (e.g., lk_minor_bonus_type)
    responsible_org_id INTEGER REFERENCES lk_org(id),
    paid_by_org_id INTEGER REFERENCES lk_org(id),
    amount NUMERIC,
    due_date DATE,
    date_paid DATE,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    ebis_updated_timestamp_ms BIGINT,
    ebis_cache_updated_timestamp_ms BIGINT
);

-- Pre-Arbitration Bonus Payment
CREATE TABLE pre_arb_bonus_payment (
    pre_arb_bonus_id BIGINT PRIMARY KEY, -- From definition
    year INTEGER NOT NULL,
    org_id INTEGER NOT NULL REFERENCES lk_org(id),
    person_id BIGINT NOT NULL REFERENCES person(person_id),
    war NUMERIC, -- Assuming war is numeric
    payment_amount NUMERIC,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    ebis_updated_timestamp_ms BIGINT,
    ebis_cache_updated_timestamp_ms BIGINT
);

-- Rule 5 Eligible Players
CREATE TABLE r5_eligible_player (
    r5_eligible_player_id BIGSERIAL PRIMARY KEY, -- No unique ID in definition, composite key likely year+playerId
    year INTEGER NOT NULL,
    person_id BIGINT NOT NULL REFERENCES person(person_id),
    position_id INTEGER REFERENCES lk_baseball_position(id),
    org_id INTEGER REFERENCES lk_org(id),
    club_id INTEGER REFERENCES lk_club(id),
    level_of_play_id INTEGER REFERENCES lk_level_of_play(id),
    roster_status_id INTEGER REFERENCES lk_roster_status(id),
    birthdate DATE,
    il_days INTEGER,
    has_ibp BOOLEAN,
    is_under_control BOOLEAN,
    -- History specific fields (if storing selected players from R5History endpoint)
    r5_draft_phase_id INTEGER, -- Needs lk_r5_phase
    r5_draft_selecting_org_id INTEGER REFERENCES lk_org(id),
    r5_draft_selection_round INTEGER,
    r5_draft_selection_pick INTEGER,
    created_at TIMESTAMPTZ DEFAULT now(), -- Assuming we track when record was added/updated
    updated_at TIMESTAMPTZ DEFAULT now(),
    ebis_updated_timestamp_ms BIGINT,
    UNIQUE (year, person_id) -- Assuming a player is eligible once per year
);

-- System Dates / Values
CREATE TABLE system_date (
    system_date_year INTEGER PRIMARY KEY,
    first_day_of_major_league_season DATE,
    last_day_of_major_league_season DATE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    ebis_updated_timestamp_ms BIGINT,
    ebis_cache_updated_timestamp_ms BIGINT
);

CREATE TABLE system_date_club (
    system_date_club_id BIGSERIAL PRIMARY KEY,
    system_date_year INTEGER NOT NULL REFERENCES system_date(system_date_year),
    org_id INTEGER REFERENCES lk_org(id),
    club_id INTEGER NOT NULL REFERENCES lk_club(id),
    league_id INTEGER REFERENCES lk_league(id), -- Denormalized for easier access?
    first_game_of_season DATE,
    last_game_of_season DATE,
    last_playoff_date DATE,
    UNIQUE(system_date_year, club_id)
);

CREATE TABLE system_value (
    system_value_year INTEGER PRIMARY KEY,
    originally_scheduled_days_in_season INTEGER,
    actual_days_in_season INTEGER,
    originally_scheduled_games_in_season INTEGER,
    actual_games_in_season INTEGER,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    ebis_updated_timestamp_ms BIGINT,
    ebis_cache_updated_timestamp_ms BIGINT
);

-- Signing Bonus Pools (R4 / Intl)
CREATE TABLE r4_signing_bonus_pool (
    r4_signing_bonus_pool_id BIGSERIAL PRIMARY KEY,
    org_id INTEGER NOT NULL REFERENCES lk_org(id),
    year INTEGER NOT NULL,
    -- Calculated Amounts - Need to decide how to store 'asOf' variations if needed. Storing latest calculation:
    total_signing_bonus_amount NUMERIC,
    club_signing_bonus_pool_amount NUMERIC,
    overage_amount NUMERIC,
    overage_percentage NUMERIC,
    penalty_tax NUMERIC,
    penalty_draft_selections TEXT,
    -- Pool Info (Individual Picks)
    -- created_at, updated_at, ebis_updated_timestamp_ms etc.
    UNIQUE (org_id, year)
);

CREATE TABLE r4_signing_bonus_pool_pick (
    r4_signing_bonus_pool_pick_id BIGSERIAL PRIMARY KEY,
    r4_signing_bonus_pool_id BIGINT NOT NULL REFERENCES r4_signing_bonus_pool(r4_signing_bonus_pool_id) ON DELETE CASCADE,
    draft_round TEXT,
    overall_pick TEXT, -- Stored as text as could be "CBA", etc.
    person_id BIGINT REFERENCES person(person_id), -- The player drafted/signed
    school_class TEXT, -- Could link to lk_school_class
    is_nsd BOOLEAN, -- Not Subject to Deadline?
    bonus_value_amount NUMERIC,
    signed_date DATE,
    actual_bonus_amount NUMERIC,
    amount_towards_threshold NUMERIC,
    over_under NUMERIC
);

CREATE TABLE intl_signing_bonus_pool (
    intl_signing_bonus_pool_id BIGSERIAL PRIMARY KEY,
    org_id INTEGER NOT NULL REFERENCES lk_org(id),
    signing_period_start_year INTEGER NOT NULL,
    signing_period_end_year INTEGER NOT NULL,
    total_actual_signing_bonus_amount NUMERIC,
    total_exceptions_amount NUMERIC,
    total_actual_signing_bonus_minus_total_exceptions_amount NUMERIC,
    club_signing_bonus_pool_amount NUMERIC,
    overage_amount NUMERIC,
    overage_percentage NUMERIC,
    penalty_tax NUMERIC,
    penalty_msg TEXT,
    remaining_club_signing_bonus_pool_amount NUMERIC,
    original_club_signing_bonus_pool_amount NUMERIC,
    maximum_allowable_pool_amount NUMERIC,
    -- created_at, updated_at, ebis_updated_timestamp_ms etc.
    UNIQUE (org_id, signing_period_start_year)
);

-- Roster Snapshot Data (complex, potentially large)
-- Represents historical state, could be a separate schema or use partitioning heavily.
CREATE TABLE roster_snapshot (
    roster_snapshot_id BIGSERIAL PRIMARY KEY,
    roster_date DATE NOT NULL,
    person_id BIGINT NOT NULL REFERENCES person(person_id),
    org_id INTEGER REFERENCES lk_org(id),
    club_id INTEGER REFERENCES lk_club(id),
    uniform_number TEXT,
    player_position_id INTEGER REFERENCES lk_baseball_position(id),
    bats TEXT,
    throws TEXT,
    mj_roster_status_id INTEGER REFERENCES lk_roster_status(id),
    mn_roster_status_id INTEGER REFERENCES lk_roster_status(id),
    major_league_service_years INTEGER, -- Snapshot of service at that date
    major_league_service_days INTEGER,
    is_employee BOOLEAN,
    employee_position_id INTEGER REFERENCES lk_employee_position(id),
    rehab_club_id INTEGER REFERENCES lk_club(id),
    option_club_id INTEGER REFERENCES lk_club(id), -- Club player was optioned *to*?
    ebis_updated_timestamp_ms BIGINT -- When this specific snapshot record was last updated in EBIS source
);
-- Indexing is crucial here
CREATE INDEX idx_roster_snapshot_date_person ON roster_snapshot (roster_date, person_id);
CREATE INDEX idx_roster_snapshot_date_org_club ON roster_snapshot (roster_date, org_id, club_id);
-- Partitioning by roster_date (e.g., monthly or yearly) would be highly recommended.

-- Special Rosters
CREATE TABLE special_roster (
    special_roster_id BIGSERIAL PRIMARY KEY,
    org_id INTEGER NOT NULL REFERENCES lk_org(id),
    club_id INTEGER REFERENCES lk_club(id), -- Nullable if org-level roster?
    year INTEGER NOT NULL,
    roster_type_id INTEGER NOT NULL, -- Needs lk_roster_type or lk_pro_roster_snapshot_type
    ebis_updated_timestamp_ms BIGINT,
    UNIQUE (org_id, club_id, year, roster_type_id) -- Assuming club_id CAN be null for org-level
);

CREATE TABLE special_roster_person (
    special_roster_person_id BIGSERIAL PRIMARY KEY,
    special_roster_id BIGINT NOT NULL REFERENCES special_roster(special_roster_id) ON DELETE CASCADE,
    person_id BIGINT NOT NULL REFERENCES person(person_id)
    -- Denormalized fields from Person - Special Rosters if needed for performance
    -- uniform_number, player_position_id, bats, throws, mj_status_id, mn_status_id, mls_years, mls_days, is_employee, emp_pos_id
);


-- Add Indexes (Examples - Many more needed for performance)
CREATE INDEX idx_person_type ON person (person_type_id);
CREATE INDEX idx_mjc_person_id ON mjc (person_id);
CREATE INDEX idx_mnc_person_id ON mnc (person_id);
CREATE INDEX idx_transaction_type ON transaction (tx_type_id);
CREATE INDEX idx_transaction_name ON transaction (tx_name_id);
CREATE INDEX idx_transaction_date ON transaction (tx_date);
CREATE INDEX idx_tx_player_detail_person ON transaction_player_detail (person_id);
CREATE INDEX idx_tx_player_detail_tx ON transaction_player_detail (tx_id);
CREATE INDEX idx_add_c_person_id ON add_c (person_id);
CREATE INDEX idx_add_c_mnc_id ON add_c (mnc_id);
CREATE INDEX idx_add_d_person_id ON add_d (person_id);
CREATE INDEX idx_add_d_mnc_id ON add_d (mnc_id);
CREATE INDEX idx_arbitration_person_year ON arbitration (person_id, arbitration_year);
CREATE INDEX idx_award_year_code ON award (year, award_code);
CREATE INDEX idx_award_vote_person ON award_vote (person_id);
CREATE INDEX idx_cep_person ON cep (person_id);
CREATE INDEX idx_csp_person ON csp (person_id);
-- ... indexes on FKs and frequently queried columns (timestamps, org_id, club_id, year)