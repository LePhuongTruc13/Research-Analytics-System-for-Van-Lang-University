-- ============================================
-- Drop tables (optional)
-- ============================================

DROP TABLE IF EXISTS author_metrics CASCADE;
DROP TABLE IF EXISTS paper_topic CASCADE;
DROP TABLE IF EXISTS topics CASCADE;
DROP TABLE IF EXISTS author_institution CASCADE;
DROP TABLE IF EXISTS paper_author CASCADE;
DROP TABLE IF EXISTS institutions CASCADE;
DROP TABLE IF EXISTS authors CASCADE;
DROP TABLE IF EXISTS papers CASCADE;

-- ============================================
-- Papers
-- ============================================

CREATE TABLE papers (

    paper_id VARCHAR(50) PRIMARY KEY,

    doi VARCHAR(255),

    title TEXT NOT NULL,

    abstract TEXT,

    publication_year INTEGER,

    cited_by_count INTEGER,

    is_open_access BOOLEAN

);

-- ============================================
-- Authors
-- ============================================

CREATE TABLE authors (

    author_id VARCHAR(50) PRIMARY KEY,

    author_name TEXT NOT NULL

);

-- ============================================
-- Institutions
-- ============================================

CREATE TABLE institutions (

    institution_id VARCHAR(50) PRIMARY KEY,

    institution_name TEXT,

    country_code VARCHAR(50)

);

-- ============================================
-- Paper - Author
-- ============================================

CREATE TABLE paper_author (

    paper_id VARCHAR(50),

    author_id VARCHAR(50),

    PRIMARY KEY (paper_id, author_id),

    FOREIGN KEY (paper_id)
        REFERENCES papers(paper_id)
        ON DELETE CASCADE,

    FOREIGN KEY (author_id)
        REFERENCES authors(author_id)
        ON DELETE CASCADE

);

-- ============================================
-- Author - Institution
-- ============================================

CREATE TABLE author_institution (

    author_id VARCHAR(50),

    institution_id VARCHAR(50),

    PRIMARY KEY (author_id, institution_id),

    FOREIGN KEY (author_id)
        REFERENCES authors(author_id)
        ON DELETE CASCADE,

    FOREIGN KEY (institution_id)
        REFERENCES institutions(institution_id)
        ON DELETE CASCADE

);

-- ============================================
-- Topics (BERTopic)
-- ============================================

CREATE TABLE topics (

    topic_id INTEGER PRIMARY KEY,

    topic_name TEXT,

    keywords TEXT,

    paper_count INTEGER

);

-- ============================================
-- Paper - Topic
-- ============================================

CREATE TABLE paper_topic (

    paper_id VARCHAR(50),

    topic_id INTEGER,

    probability FLOAT,

    PRIMARY KEY (paper_id, topic_id),

    FOREIGN KEY (paper_id)
        REFERENCES papers(paper_id)
        ON DELETE CASCADE,

    FOREIGN KEY (topic_id)
        REFERENCES topics(topic_id)
        ON DELETE CASCADE

);

-- ============================================
-- Author Metrics (Network Analysis)
-- ============================================

CREATE TABLE author_metrics (

    author_id VARCHAR(50) PRIMARY KEY,

    degree FLOAT,

    betweenness FLOAT,

    closeness FLOAT,

    pagerank FLOAT,

    FOREIGN KEY (author_id)
        REFERENCES authors(author_id)
        ON DELETE CASCADE

);