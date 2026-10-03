# HealthCare Analysis — Technical Documentation

## Technical Scope

This document describes the technical implementation used to prepare, model, validate, and visualize the HealthCare Analysis project. Analytical findings and interpretations are documented separately in [`readme_analysis.md`](readme_analysis.md).

## Project Tools

- Python / Pandas
- Power BI
- DAX
- Data modeling
- Git / GitHub

## Data Workflow

The project workflow included:

1. Review the supplied hospital and patient-survey data.
2. Inspect fields, missing values, geographic information, and survey-related measures.
3. Prepare the data for analysis and Power BI.
4. Build relationships and analytical measures in the Power BI model.
5. Validate measure behavior in different filter contexts.
6. Build and verify the report pages.
7. Document analytical findings separately from technical implementation.

## Power BI Report Pages

The final report contains the following analytical pages:

- **Hospitals Performance**
- **Top 10 Hospitals**
- **Hospitals by City**
- **Hospital Survey Response Map**

## Survey Response Rate Measure

The hospital-level measure was defined using the maximum survey response rate in the current filter context:

```DAX
Survey Response Rate =
MAX(FACT_PATIENT_SURVEY[SURVEY_RESPONSE_RATE_PERCENT])
```

At an individual hospital row, the hospital filter context allows this measure to return the hospital's response-rate value. At the table total level, the context is broader and the measure returns the maximum response rate in that context rather than an overall average.

Because the total could be misinterpreted, the table total row was removed. A separate measure is used for the dashboard's overall average hospital response-rate KPI.

## Completed Surveys

Completed Surveys is used as supporting survey-participation context at the hospital and location levels. It is displayed alongside Survey Response Rate where appropriate.

## Geographic Implementation

The map uses the `LOCATION` field for geographic placement. Some source records contained explicit coordinates while others contained address information without latitude/longitude.

Power BI was able to geocode applicable address-only `LOCATION` records. The final map therefore uses location/address information rather than excluding all records that lack explicit coordinates.

The final map is titled:

**Hospital Survey Response Rate by Location**

The tooltip includes:

- Survey Response Rate
- Completed Surveys

Bubble size was intentionally left uniform so the visual does not imply an additional magnitude relationship beyond the values provided in the tooltip.

## Patient Survey Star Rating Validation

`PATIENT_SURVEY_STAR_RATING` was inspected at the row level before being used as a hospital-level metric.

The validation showed that:

- the source field contains discrete star values and blanks;
- multiple survey/measure rows can occur within the same hospital/location context;
- those records can contain different star-rating values;
- averaging them can create fractional derived values that do not exist as source star values.

For that reason, the field was not used as a definitive hospital-level rating on the final geographic visualization.

## Dashboard Validation

The report was reviewed page by page to confirm:

- measures behaved correctly in their intended filter context;
- misleading totals were removed;
- visual titles matched the metric actually displayed;
- geographic tooltips returned valid location-level information;
- the star-rating field was not presented with a stronger interpretation than the source data supports.

## Documentation Structure

The project documentation is intentionally separated:

- `README.md` — project introduction, objective, tools, portfolio context, and AI-assistance disclosure.
- `readme_analysis.md` — analytical questions, findings, visual evidence, interpretation, and data limitations.
- `readme_tech.md` — technical workflow, DAX logic, data-model decisions, geographic implementation, and Power BI configuration.

This separation keeps the analytical story distinct from the technical implementation.
