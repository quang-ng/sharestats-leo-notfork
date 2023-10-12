BEGIN;
CREATE TABLE openalex_works (
    id text NOT NULL,
    doi text,
    title text,
    display_name text,
    publication_year integer,
    publication_date text,
    type text,
    cited_by_count integer,
    is_retracted boolean,
    is_paratext boolean,
    cited_by_api_url text,
    abstract_inverted_index json
);

--
-- Name: works_primary_locations; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex_works_primary_locations (
    work_id text,
    source_id text,
    landing_page_url text,
    pdf_url text,
    is_oa boolean,
    version text,
    license text
);


--
-- Name: works_locations; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex_works_locations (
    work_id text,
    source_id text,
    landing_page_url text,
    pdf_url text,
    is_oa boolean,
    version text,
    license text
);


--
-- Name: works_best_oa_locations; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex_works_best_oa_locations (
    work_id text,
    source_id text,
    landing_page_url text,
    pdf_url text,
    is_oa boolean,
    version text,
    license text
);


--
-- Name: works_authorships; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex_works_authorships (
    work_id text,
    author_position text,
    author_id text,
    institution_id text,
    raw_affiliation_string text
);


--
-- Name: works_biblio; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex_works_biblio (
    work_id text NOT NULL,
    volume text,
    issue text,
    first_page text,
    last_page text
);


--
-- Name: works_concepts; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex_works_concepts (
    work_id text,
    concept_id text,
    score real
);


--
-- Name: works_ids; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex_works_ids (
    work_id text NOT NULL,
    openalex text,
    doi text,
    mag bigint,
    pmid text,
    pmcid text
);


--
-- Name: works_mesh; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex_works_mesh (
    work_id text,
    descriptor_ui text,
    descriptor_name text,
    qualifier_ui text,
    qualifier_name text,
    is_major_topic boolean
);


--
-- Name: works_open_access; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex_works_open_access (
    work_id text NOT NULL,
    is_oa boolean,
    oa_status text,
    oa_url text,
    any_repository_has_fulltext boolean
);


--
-- Name: works_referenced_works; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex_works_referenced_works (
    work_id text,
    referenced_work_id text
);


--
-- Name: works_related_works; Type: TABLE; Schema: openalex; Owner: -
--

CREATE TABLE openalex_works_related_works (
    work_id text,
    related_work_id text
);

CREATE INDEX works_primary_locations_work_id_idx ON openalex_works_primary_locations USING btree (work_id);

CREATE INDEX works_locations_work_id_idx ON openalex_works_locations USING btree (work_id);

CREATE INDEX works_best_oa_locations_work_id_idx ON openalex_works_best_oa_locations USING btree (work_id);

COMMIT;