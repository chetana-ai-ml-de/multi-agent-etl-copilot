# 📘 Multi-Agent ETL Copilot — Full Documentation

This document summarizes the entire ETL Copilot pipeline including schema, mapping, generated ETL code, validation findings, and workflow steps.

---

# 1. 📊 Source Schema Summary

Example input dataset extracted by SchemaAgent:

```
PROVNUM: object
PROVNAME: object
CITY: object
STATE: object
COUNTY_NAME: object
CY_Qtr: object
WorkDate: int64
MDScensus: int64
Hrs_RN: float64
Hrs_LPN: float64
Hrs_CNA: float64
...
```

The SchemaAgent converts this into a compact, LLM-friendly format.

---

# 2. 🎯 Target Schema  
(Used for Capstone Demo)

```
facility_id
facility_name
state
county_name
quarter
work_date
resident_census
rn_hours_total
lpn_hours_total
cna_hours_total
total_nursing_hours
```

---

# 3. 🔄 Mapping Table (Auto-Generated)

Example produced by MappingAgent:

| Target Field          | Source Column     | Mapping Type   | Notes |
|----------------------|-------------------|----------------|-------|
| facility_id          | PROVNUM           | direct         | —     |
| facility_name        | PROVNAME          | direct         | —     |
| state                | STATE             | direct         | —     |
| county_name          | COUNTY_NAME       | direct         | —     |
| quarter              | CY_Qtr            | direct         | —     |
| work_date            | WorkDate          | direct         | —     |
| resident_census      | MDScensus         | direct         | —     |
| rn_hours_total       | Hrs_RN            | direct         | —     |
| lpn_hours_total      | Hrs_LPN           | direct         | —     |
| cna_hours_total      | Hrs_CNA           | direct         | —     |
| total_nursing_hours  | Derived           | formula        | Sum of RN + LPN + CNA |

Missing fields are labeled as “NO MATCH”.

---

# 4. 🧪 Generated ETL Code (TransformAgent)

```
df_out = df.rename(columns={
    'PROVNUM': 'facility_id',
    'PROVNAME': 'facility_name',
    'STATE': 'state',
    'COUNTY_NAME': 'county_name',
    'CY_Qtr': 'quarter',
    'WorkDate': 'work_date',
    'MDScensus': 'resident_census',
    'Hrs_RN': 'rn_hours_total',
    'Hrs_LPN': 'lpn_hours_total',
    'Hrs_CNA': 'cna_hours_total'
})

df_out['total_nursing_hours'] = (
    df_out['rn_hours_total'].fillna(0)
    + df_out['lpn_hours_total'].fillna(0)
    + df_out['cna_hours_total'].fillna(0)
)

df_out = df_out[
    [
        'facility_id', 'facility_name', 'state', 'county_name',
        'quarter', 'work_date', 'resident_census',
        'rn_hours_total', 'lpn_hours_total', 'cna_hours_total',
        'total_nursing_hours'
    ]
]
```

---

# 5. 🧹 Validation Report (ValidationAgent)

Example validation output:

```
{
  "validation_result": "PASS",
  "issues": []
}
```

Or for FAIL:

```
{
  "validation_result": "FAIL",
  "issues": [
    {"issue_type": "Missing Target Columns", "description": "..."},
    {"issue_type": "Suspicious Column Reference", "description": "..."}
  ]
}
```

---

# 6. 📄 Data Dictionary (Auto-Generated)

| Field Name            | Description                                   |
|-----------------------|-----------------------------------------------|
| facility_id           | Unique provider identifier                    |
| facility_name         | Nursing facility name                         |
| state                 | U.S. state code                               |
| county_name           | County where facility is located              |
| quarter               | Calendar quarter                              |
| work_date             | Date of staffing measurement                  |
| resident_census       | Number of residents at census                 |
| rn_hours_total        | Total RN hours                                 |
| lpn_hours_total       | Total LPN hours                                |
| cna_hours_total       | Total CNA hours                                |
| total_nursing_hours   | Sum of total nursing staff hours              |

---

# 7. 🔁 Pipeline Workflow Summary

1. SchemaAgent extracts schema  
2. MappingAgent creates mapping JSON  
3. TransformAgent generates Python code  
4. ValidationAgent checks correctness  
5. DocumentationAgent builds this file  

---

# 8. 🏁 Conclusion

This multi-agent pipeline automates the entire ETL journey:

**Schema → Mapping → Code → Validation → Documentation**

It reduces manual engineering time, increases accuracy, and standardizes transformation patterns.

Suitable for any industry: healthcare, finance, HR, retail, operations.

