# Data View Schema: `Student_Validation_View`

**Purpose:** This view aggregates data from Diploma Services, International Relations, Languages, and Internship databases into a single read-only table for the Validation Dashboard.

**Refresh Rate:** Daily (at 04:00 AM)

## Schema Definition

| Column Name | Data Type | Source System | Description |
| :--- | :--- | :--- | :--- |
| `Student_ID` | VARCHAR(20) | ERP (Phenix) | **Primary Key**. Format: EPF20XX-XXXX |
| `Full_Name` | VARCHAR(100) | ERP | Student's full legal name |
| `Major` | VARCHAR(50) | ERP | e.g., "Généraliste", "Numérique" |
| `Year_Level` | VARCHAR(10) | ERP | e.g., "5A" |
| `Credits_1A` | FLOAT | Phenix | Validated credits for Year 1 |
| `Credits_2A` | FLOAT | Phenix | Validated credits for Year 2 |
| `Credits_3A` | FLOAT | Phenix | Validated credits for Year 3 |
| `Credits_4A` | FLOAT | Phenix | Validated credits for Year 4 |
| `Credits_5A` | FLOAT | Phenix | Validated credits for Year 5 |
| `Credits_S7` | FLOAT | Phenix | Semester 7 Total |
| `Credits_S8` | FLOAT | Phenix | Semester 8 Total |
| `Credits_S9` | FLOAT | Phenix | Semester 9 Total |
| `Credits_S10` | FLOAT | Phenix | Semester 10 Total |
| `English_Score` | INT | Langues | Most recent validation score (TOEIC/Equivalent) |
| `Voltaire_Status` | VARCHAR(20) | Pedagogy | "Valid", "Invalid", "Exempt" |
| `Internship_Status` | VARCHAR(20) | Stages | "Valid", "Ongoing", "Pending" |
| `Internship_End_Date`| DATE | Stages | End date of final internship |
| `Competencies_Status`| VARCHAR(20) | BDE | "Acquired", "In Progress" |
| `Last_Updated` | TIMESTAMP | System | Time of last data fetch |

## SQL Pseudo-Code (for IT Reference)

```sql
CREATE VIEW Student_Validation_View AS
SELECT
    s.id as Student_ID,
    s.name as Full_Name,
    -- ... (joins with other tables)
FROM
    Students s
    LEFT JOIN Credits c ON s.id = c.student_id
    LEFT JOIN Languages l ON s.id = l.student_id
    LEFT JOIN Internships i ON s.id = i.student_id;
```
