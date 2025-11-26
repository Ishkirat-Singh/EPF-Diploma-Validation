# EPF Diploma Validation System - Design & Layout

## 🏗️ High-Level Architecture

This diagram illustrates the overall structure of the system, from data ingestion to visualization.

```mermaid
graph TD
    subgraph "Data Sources"
        DS_Dip[Diploma Services]
        DS_BDE[BDE / DSI]
        DS_Lang[Language Services]
        DS_Int[International Dev]
        DS_Stud[Director of Studies]
        DS_Intern[Internship Services]
    end

    subgraph "Data Processing (Python/Pandas)"
        Ingest[Data Ingestion Script]
        Clean[Data Cleaning & Normalization]
        Valid[Validation Rules Engine]
    end

    subgraph "Storage"
        DB[(Central SQL Database)]
        DD[Data Dictionary]
    end

    subgraph "Presentation"
        Dash[Dashboard (Power BI / Web)]
        Rep[Reports]
    end

    DS_Dip -->|Excel / Phenix| Ingest
    DS_BDE -->|TBD| Ingest
    DS_Lang -->|Scores| Ingest
    DS_Int -->|VEIO / TFI| Ingest
    DS_Stud -->|Voltaire| Ingest
    DS_Intern -->|PFE Dates| Ingest

    Ingest --> Clean
    Clean --> Valid
    Valid --> DB
    DD -.->|Defines| DB
    DB --> Dash
    DB --> Rep
```

## 🔄 Data Flow Diagram

This diagram details how data moves through the system and how it is transformed.

```mermaid
flowchart LR
    RawData[Raw Data Files] -->|Load| DataFrame[Pandas DataFrames]
    DataFrame -->|Standardize| StdData[Standardized Data]
    
    subgraph "Transformation Steps"
        StdData -->|Map Columns| Mapped
        Mapped -->|Handle Missing| Cleaned
        Cleaned -->|Deduplicate| Unique
        Unique -->|Merge| MasterTable
    end
    
    MasterTable -->|Export| SQL[SQL Database]
    MasterTable -->|Export| CSV[Cleaned CSV]
```

## 🗃️ Entity Relationship Diagram (Draft)

A tentative schema for the central database based on the data sources.

```mermaid
erDiagram
    STUDENT {
        string Student_ID PK
        string Name
        string Email
        string Program
    }
    
    ACADEMIC_CREDITS {
        int ID PK
        string Student_ID FK
        string Year_Level "1A, 2A, 3A, etc."
        float Credits_Value
        string Source "EPF, External"
        string Status "Validated, Pending"
    }
    
    LANGUAGE_SCORES {
        int ID PK
        string Student_ID FK
        string Test_Type "TOEIC, Voltaire, TFI"
        int Score
        date Date_Taken
    }
    
    COMPETENCIES {
        int ID PK
        string Student_ID FK
        string Competency_Name
        string Status "Acquired, Objective"
    }
    
    INTERNSHIP {
        int ID PK
        string Student_ID FK
        date Start_Date
        date End_Date
        boolean Validated
    }

    STUDENT ||--o{ ACADEMIC_CREDITS : has
    STUDENT ||--o{ LANGUAGE_SCORES : has
    STUDENT ||--o{ COMPETENCIES : has
    STUDENT ||--o{ INTERNSHIP : completes
```

## 📝 Data Dictionary Structure

| Field Name | Data Type | Description | Source | Validation Rule |
|------------|-----------|-------------|--------|-----------------|
| `Student_ID` | String | Unique identifier (e.g., EPF2024-123) | All | Must be unique |
| `Credits_Total` | Float | Sum of validated credits | Phenix/Excel | >= 180 for diploma |
| `English_Score` | Integer | TOEIC or equivalent score | Langues | >= 785 |
| `PFE_Validated` | Boolean | Internship validation status | Stages | True if valid |
