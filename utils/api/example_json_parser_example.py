from json_parser import query_json

sample_json = {
  "clientNumber": "525278745",
  "upskillingID": "1537927835421777920",
  "expectedStartDate": "2025-11-27",
  "expectedEndDate": "2025-11-30",
  "actualStartDate": "2025-11-27",
  "actualEndDate": "None",
  "outcomeResultCode": "None",
  "outcomeCode": "None",
  "transactionID": "A1234",
  "sourceSystem": "MyMSD",
  "courseDetails": [
    {
      "courseID": "9176032803442139136",
      "courseName": "Test Course",
      "participation": [
        {
          "weekCode": {
            "tableName": "MSDWeek",
            "value": "WK1",
            "description": "Week 1"
          },
          "hoursCompleted": 0,
          "minutesCompleted": 0
        },
        {
          "weekCode": {
            "tableName": "MSDWeek",
            "value": "WK2",
            "description": "Week 2"
          },
          "hoursCompleted": 0,
          "minutesCompleted": 0
        },
        {
          "weekCode": {
            "tableName": "MSDWeek",
            "value": "WK3",
            "description": "Week 3"
          },
          "hoursCompleted": 0,
          "minutesCompleted": 0
        },
        {
          "weekCode": {
            "tableName": "MSDWeek",
            "value": "WK4",
            "description": "Week 4"
          },
          "hoursCompleted": 0,
          "minutesCompleted": 0
        }
      ]
    }
  ],
  "weekDetails": [
    {
      "weekStartDate": "2025-11-27",
      "weekEndDate": "2025-11-27",
      "weekCode": {
        "tableName": "MSDWeek",
        "value": "WK1",
        "description": "Week 1"
      }
    },
    {
      "weekStartDate": "2025-11-28",
      "weekEndDate": "2025-11-28",
      "weekCode": {
        "tableName": "MSDWeek",
        "value": "WK2",
        "description": "Week 2"
      }
    },
    {
      "weekStartDate": "2025-11-29",
      "weekEndDate": "2025-11-29",
      "weekCode": {
        "tableName": "MSDWeek",
        "value": "WK3",
        "description": "Week 3"
      }
    },
    {
      "weekStartDate": "2025-11-30",
      "weekEndDate": "2025-11-30",
      "weekCode": {
        "tableName": "MSDWeek",
        "value": "WK4",
        "description": "Week 4"
      }
    }
  ]
}


#print(parse_and_resolve_json(sample_json, input_from_feature_file))
input_from_feature_file = "weekDetails..value=WK3"

print(query_json(sample_json, input_from_feature_file))

# --- Define all test inputs in a list ---
test_inputs = [
    # 1️ JMESPath query (returns the value field)
    # Result = WK2
    "courseDetails[0].participation[1].weekCode.value",

    # 2️ JMESPath query (returns entire object)
    # Result = {'tableName': 'MSDWeek', 'value': 'WK2', 'description': 'Week 2'}
    "courseDetails[0].participation[1].weekCode",

    "courseDetails[0]..value",

    # 3️ Direct key lookup
    # Result = 525683311
    "clientNumber",

    # 4 Find dict where value == WK3
    # Result = {'tableName': 'MSDWeek', 'value': 'WK3', 'description': 'Week 3'}
    "courseDetails[]..value=WK3",

    # 5️ Parent of the dict (offset -1)
    # Result = {'weekCode': {'tableName': 'MSDWeek', 'value': 'WK3', 'description': 'Week 3'}}
    "courseDetails..value=WK3:-1",

    # 6️ Parent, then extract weekEndDate
    # Result = 2025-10-17
    "weekDetails..value=WK3:-1.weekEndDate",


    # 7️ Match by value only (WK1)
    # Result = {'tableName': 'MSDWeek', 'value': 'WK1', 'description': 'Week 1'}
    "value=WK1"
]


# --- Loop through and call the wrapper method ---
for idx, pattern in enumerate(test_inputs, start=1):
    result = query_json(sample_json, pattern)
    print(f"{idx}: Pattern = {pattern}\nResult = {result}\n")

