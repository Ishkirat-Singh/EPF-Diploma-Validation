# Visualization Mapping & Justification

This document maps each column from the "Excel Validation Criteria" to a specific visualization on the dashboard, explaining **Why** we chose it and **How** we handle the data frequency.

## 1. Academic Performance (Credits)

| Data Point | Visualization | Justification | Update Freq |
| :--- | :--- | :--- | :--- |
| **Yearly Credits** (1A-5A) | **Stacked Bar Chart** | Allows quick comparison of progress across years. Gaps (e.g., missing 2A credits) are immediately visible as "dips" in the bar. | Semesterly |
| **Total Credits** (Target: 300) | **Radial Progress Bar** | Shows percentage completion towards the absolute goal (300 ECTS). A full circle = Graduation Ready. | Semesterly |
| **Semester Breakdown** (S7-S10) | **Heatmap Table** | Color-coded (Green > 30, Red < 30). Efficiently shows which specific semester is blocking graduation without cluttering the UI. | Semesterly |

## 2. Language Proficiency

| Data Point | Visualization | Justification | Update Freq |
| :--- | :--- | :--- | :--- |
| **TOEIC Score** | **Gauge Chart** | **Threshold: 785**. The needle clearly shows if the student is in the "Green Zone" or "Red Zone". Much faster to read than a raw number. | Monthly |
| **Voltaire** | **Status Badge** | Binary status (Valid/Invalid). Does not need a chart, just a clear "Badge" indicator. | Yearly |

## 3. Professional Experience (Internships)

| Data Point | Visualization | Justification | Update Freq |
| :--- | :--- | :--- | :--- |
| **Internship Validity** | **Timeline (Gantt)** | Visualizes the *duration* and *dates*. Helps verify if the minimum 14 weeks were met and if the visible dates overlap with academic periods. | Weekly |
| **PFE Decision** | **Traffic Light Icon** | Critical Go/No-Go decision. Traffic light (Green/Red) mimics the final jury decision process. | Weekly |

## 4. Competencies & Soft Skills

| Data Point | Visualization | Justification | Update Freq |
| :--- | :--- | :--- | :--- |
| **Competency Status** | **Spider / Radar Chart** | Plots different competency dimensions. If the shape is fully filled, the student is complete. If one corner is "dented", that specific competency is missing. | Yearly |

---

## 🕒 Data Latency Strategy

Since data comes from different sources (Stages, Langues, Pedagogy) with different update frequencies, the dashboard will include a **"Freshness Indicator"** tooltip for each section.

*   **Example:** Hovering over the Internship timeline will show: *"Source: CSM Tool. Last Updated: 2 days ago."*
*   **Justification:** This prevents the jury from making decisions based on stale data. If the data is > 1 month old for a "Weekly" source, the indicator turns Orange to warn the user.
