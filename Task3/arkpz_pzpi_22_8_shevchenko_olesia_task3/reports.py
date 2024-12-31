import csv
from models import AccessEvent

# Генерує звіт про події доступу в форматі CSV
def generate_access_report():
    file_path = "reports/access_report.csv"
    try:
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["ID", "User ID", "Lab ID", "Timestamp", "Status", "Reason"])
            for event in AccessEvent.query.all():
                writer.writerow([event.id, event.user_id, event.lab_id, event.timestamp, event.status, event.reason])
        return file_path
    except Exception as e:
        return f"Error generating report: {e}"
