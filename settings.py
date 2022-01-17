'''
Set paths for all python files at one place

'''

json_path = r"E:/Bachelorarbeit/JSONs"  # Path for CIK json files
# Path for raw 10K filings and 10K token files
tenk_path = r"E:/Bachelorarbeit/filings"
# Path for excel/csv output files (there will be one output file from every python file)
csv_path = r"E:/Bachelorarbeit/output"

#observation period

start_date = "2000-01-01"
end_date = "2021-10-01"

#short event window size for linear regression

event_start = -1
event_end = 4

#longer event window for CAR

event_start_extended = -5
event_end_extended = 31


