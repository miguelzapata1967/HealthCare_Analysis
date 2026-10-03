# HealthCare Analysis — Analytical Findings

## Analysis Scope

This document records the analytical findings and supporting visual evidence from the hospital patient-survey dataset provided for the project. The analysis reports what was observed in the available data while explicitly disclosing limitations in coverage and completeness.

## Hospital Performance and Survey Participation

Hospital-level survey participation was evaluated using completed surveys and survey response rate. Response rates vary among the hospitals represented in the dataset.

![Hospital Performance](images/analysis_result_09.png)

### Validation of the Response-Rate Measure

The hospital-level `Survey Response Rate` measure uses `MAX(FACT_PATIENT_SURVEY[SURVEY_RESPONSE_RATE_PERCENT])`. In an individual hospital row, the filter context returns that hospital's value. In the table total context, however, the same measure returned the maximum value across the broader context rather than an overall response rate. For this reason, the misleading total row was removed and the dashboard retains a separate overall average-response-rate KPI.

![Hospital Performance Measure Validation](images/analysis_result_10.png)

## Top Hospitals by Survey Response Rate

The analysis identifies hospitals with the highest survey response rates within the provided dataset. These results describe the project data only and should not be interpreted as a comprehensive national ranking of U.S. hospitals.

![Top 10 Hospitals](images/analysis_result_11.png)

## Hospitals by City

The geographic analysis shows that some cities represented in the dataset contain multiple hospitals. This finding describes the hospital records supplied for the project and does not establish complete hospital coverage for those cities.

![Hospitals by City](images/analysis_result_12.png)

## Hospital Survey Response by Location

The final geographic visualization maps hospital/location records and presents Survey Response Rate and Completed Surveys as supporting information.

![Hospital Survey Response Rate by Location](images/analysis_result_16.png)

## Patient Survey Star Rating — Data Quality Finding

The investigation of `PATIENT_SURVEY_STAR_RATING` showed that the source field contains discrete star values and blanks. Multiple survey and measure records can occur within the same hospital/location context, and different records can contain different star ratings.

![Patient Survey Star Rating Source Values](images/analysis_result_05.png)

![Patient Survey Star Rating Record Investigation](images/analysis_result_06.png)

![Patient Survey Star Rating Context Validation](images/analysis_result_07.png)

Averaging those records by hospital/location can therefore create a fractional derived value that is not itself a source-reported star value. The star-rating evidence is retained as a finding, but it is not used as a definitive overall hospital rating or comprehensive national hospital ranking.

## Additional Analysis Evidence

The following screenshots preserve the intermediate result checks used to validate the analytical workflow.

![Analysis Evidence 1](images/analysis_result_01.png)

![Analysis Evidence 2](images/analysis_result_02.png)

![Analysis Evidence 3](images/analysis_result_03.png)

![Analysis Evidence 4](images/analysis_result_04.png)

![Analysis Evidence 8](images/analysis_result_08.png)

![Analysis Evidence 13](images/analysis_result_13.png)

![Analysis Evidence 14](images/analysis_result_14.png)

![Analysis Evidence 15](images/analysis_result_15.png)

## Data Limitations

The analysis reflects only the hospital and patient-survey records supplied for this project. The dataset does not contain every hospital in the United States, and some hospital, geographic, and patient-survey information is incomplete.

The geographic work also identified records without explicit latitude/longitude coordinates. Address information contained in `LOCATION` was used for Power BI geocoding where applicable.

These limitations do not require discarding findings observed in the supplied data. They limit how broadly those findings can be generalized. Results should therefore be interpreted as evidence from the available dataset rather than as a comprehensive assessment of the entire U.S. hospital population.

## Analytical Conclusion

The project preserves findings supported by the available evidence, validates questionable aggregations before interpreting them, and separates observed results from claims that the data cannot support.
