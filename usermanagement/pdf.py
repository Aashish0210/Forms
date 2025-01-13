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
    daily_reports = intern_profile.dailyreport_set.all()

    # Create an HTTP response with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="daily_reports.pdf"'

    # Create the PDF canvas
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Add title
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, height - 50, "Intern Form")

    # Add intern details
    p.setFont("Helvetica", 10)
    user = intern_profile.user  # Access related user
    p.drawString(50, height - 100, f"Name: {user.first_name} {user.last_name}")
    p.drawString(50, height - 120, f"Email: {user.email}")
    p.drawString(50, height - 140, f"Phone Number: {intern_profile.phone_no or 'Not Provided'}")
    if intern_profile.department:
        p.drawString(50, height - 160, f"Department: {intern_profile.department.name}")
        p.drawString(50, height - 180, f"Department Location: {intern_profile.department.location}")
    else:
        p.drawString(50, height - 160, "Department: Not Assigned")

    # Add supervisor details if available
    if intern_profile.supervisor:
        supervisor_user = intern_profile.supervisor  # Access supervisor's User instance
        supervisor_profile = getattr(supervisor_user, 'supervisorprofile', None)  # Access SupervisorProfile
        supervisor_name = f"{supervisor_user.first_name} {supervisor_user.last_name}" if supervisor_user else "Not Provided"
        supervisor_email = supervisor_profile.email if supervisor_profile else "Not Provided"
        supervisor_phone = supervisor_profile.phone_no if supervisor_profile else "Not Provided"

        p.drawString(50, height - 200, f"Supervisor Name: {supervisor_name}")
        p.drawString(50, height - 220, f"Supervisor Email: {supervisor_email}")
        p.drawString(50, height - 240, f"Supervisor Phone: {supervisor_phone}")
    else:
        p.drawString(50, height - 200, "Supervisor: Not Assigned")

    # Prepare table for daily reports
    table_start_y = height - 260
    table_data = [["S.N.", "Time In", "Time Out", "Task Done", "Problem Faced"]]
    for idx, report in enumerate(daily_reports, start=1):
        table_data.append([idx, report.time_in, report.time_out, report.task_done, report.problem_faced])

    # Create table
    table = Table(table_data, colWidths=[40, 100, 100, 150, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))

    # Adjust for table height
    table_height = len(table_data) * 20
    available_space = height - table_start_y - 40

    if table_height > available_space:
        p.showPage()
        p.setFont("Helvetica-Bold", 14)
        p.drawString(200, height - 50, "Intern Form")
        table_start_y = height - 100

    table.wrapOn(p, width, height)
    table.drawOn(p, 50, table_start_y - table_height)

    # Finalize PDF
    p.save()

    return response
