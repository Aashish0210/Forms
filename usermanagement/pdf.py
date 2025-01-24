from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

def generate_pdf(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    # Get the intern's profile and daily reports
    intern_profile = request.user.internprofile
    daily_reports = intern_profile.dailyreport_set.all().order_by('date')  # Sort reports by date ascending

    # Create an HTTP response with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="daily_reports.pdf"'

    # Create the PDF canvas
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Add title
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, height - 50, "Intern Evaluation Forms")
    p.drawString(220, height - 70, "Citizen College")

    # Prepare tables for intern profile and supervisor details
    table_data_intern = [
        [f"Program: BCA"],
        [f"Name of Student: {intern_profile.user.first_name} {intern_profile.user.last_name}"],
        [f"Email of Student: {intern_profile.user.email}"],
        [f"Phone Number: {intern_profile.phone_no or 'Not Provided'}"],
        [f"Department assign: {intern_profile.department.name if intern_profile.department else 'Not Assigned'}"],
        [f"Organization detail: {intern_profile.department.name_and_location if intern_profile.department else 'Not Assigned'}"]
    ]

    # Prepare supervisor details
    supervisor_name = "Not Provided"
    supervisor_email = "Not Provided"
    supervisor_phone = "Not Provided"
    if intern_profile.supervisor:
        supervisor_user = intern_profile.supervisor
        supervisor_profile = getattr(supervisor_user, 'supervisorprofile', None)
        supervisor_name = f"{supervisor_user.first_name} {supervisor_user.last_name}" if supervisor_user else "Not Provided"
        supervisor_email = supervisor_profile.email if supervisor_profile else "Not Provided"
        supervisor_phone = supervisor_profile.phone_no if supervisor_profile else "Not Provided"

    table_data_supervisor = [
        [f"Page No:"],
        [f"PU Registration NO: {intern_profile.user.pu_reg_no if intern_profile.user.pu_reg_no else 'Not Assigned'}"],
        [f"Internship start Date: "],
        [f"Supervisor Name: {supervisor_name}"],
        [f"Supervisor Email: {supervisor_email}"],
        [f"Supervisor Phone: {supervisor_phone}"]
    ]

    # Create tables for intern profile and supervisor side by side
    table_intern = Table(table_data_intern, colWidths=[250, 270])  # First table width is 150 for 'Field' and 250 for 'Details'
    table_supervisor = Table(table_data_supervisor, colWidths=[290, 250])  # Same width for supervisor details

    # Set table styles
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ])
    
    # Apply styles to both tables
    table_intern.setStyle(table_style)
    table_supervisor.setStyle(table_style)

    # Adjust the position for the tables (side by side)
    table_start_y = height - 200
    table_intern.wrapOn(p, width, height)
    table_supervisor.wrapOn(p, width, height)
    table_intern.drawOn(p, 50, table_start_y)
    table_supervisor.drawOn(p, 300, table_start_y)  # Adjust position to place the second table side by side

    # Add a separator before the daily reports table
    p.setLineWidth(1)
    p.line(50, table_start_y - 10, width - 20, table_start_y - 10)

    # Prepare table for daily reports
    table_data_reports = [["S.N.", "Date", "Time In", "Time Out", "Major Activities Performed", "Any concerns or problem faced", "Total Hours"]]
    for idx, report in enumerate(daily_reports, start=1):
        report_date = report.date.strftime('%Y-%m-%d') if report.date else 'No Date'
        table_data_reports.append([idx, report_date, report.start_time, report.end_time, report.task_done, report.problem_faced, report.total_hours])

    # Adjust column widths for daily reports table (include "Total Hours" column)
    table_reports = Table(table_data_reports, colWidths=[40, 50, 60, 50, 140, 155, 50])

    # Style the daily reports table
    table_reports.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))

    # Adjust the start Y position to make sure there's enough space for the daily reports
    report_start_y = table_start_y - 30 # Reduce the space to fit the daily reports below the supervisor table

    # Check if the reports will fit on the page
    table_height = len(table_data_reports) * 20
    available_space = report_start_y - 40

    if table_height > available_space:
        p.showPage()  # Start a new page if the table doesn't fit
        p.setFont("Helvetica-Bold", 14)
        p.drawString(200, height - 50, "Intern Form")
        report_start_y = height - 100

    # Wrap and draw the daily reports table on the canvas
    table_reports.wrapOn(p, width, height)
    table_reports.drawOn(p, 50, report_start_y - table_height)

    # Finalize the PDF
    p.save()

    return response
