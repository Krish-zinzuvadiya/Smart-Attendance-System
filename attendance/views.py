from django.shortcuts import render, redirect, get_object_or_404
import re
import pdfplumber
from django.contrib import messages
from .models import Student, ClassSchedule
from .forms import UploadPDFForm, ClassScheduleForm, StudentEditForm
from django.db.models import F
from textblob import TextBlob
import base64
from PIL import Image
import pytesseract
from django.core.files.base import ContentFile
import io

# Path to Tesseract (Windows) - Adjust this path if Tesseract is installed elsewhere
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def upload_pdf(request):
    if request.method == "POST":
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES["file"]

            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    lines = page.extract_text().split("\n")
                    for line in lines:
                        parts = line.split()

                        if len(parts) > 8 and parts[1].isdigit():
                            try:
                                roll_no = int(parts[0])
                                enrollment_no = parts[1]
                                # join words until we reach attended numbers
                                name_parts = []
                                i = 2
                                while i < len(parts) and not parts[i].isdigit():
                                    name_parts.append(parts[i])
                                    i += 1
                                name = " ".join(name_parts)

                                # Adjust indices based on your PDF structure
                                # This part is highly dependent on the exact PDF layout.
                                # You might need to inspect 'parts' carefully for your specific PDF.
                                # For example, if 'attended' is always 3 words after name, and 'conducted' 4 words after name.
                                # The original code had i+15, i+16, i+17, i+18 which seems very large.
                                # Let's assume a more typical structure or you'll need to debug this.
                                # For now, I'll use placeholder logic.
                                # You need to find the correct indices for attended, conducted, percentage, mentor.
                                # Example: if attended is parts[idx_attended], conducted is parts[idx_conducted]
                                # For demonstration, I'll use dummy values or try to infer from common patterns.

                                # Re-evaluating the original logic for parsing:
                                # The original code had:
                                # attended = int(parts[i+15])
                                # conducted = int(parts[i+16])
                                # percentage = float(parts[i+17])
                                # mentor = parts[i+18]
                                # This implies a very specific and long line structure.
                                # If the percentage field is removed from the model, it should not be parsed here.
                                # Let's assume 'attended', 'conducted', 'mentor' are at predictable positions after the name.
                                # This is a common point of failure for PDF parsing.
                                # You might need to print 'parts' and 'i' to find correct indices.

                                # Placeholder for correct index finding:
                                # Assuming 'attended' and 'conducted' are the first two numbers after the name,
                                # and mentor is the next string.
                                # This is a guess, you MUST verify with your actual PDF content.
                                num_fields_found = 0
                                current_idx = i
                                temp_attended = 0
                                temp_conducted = 0
                                temp_mentor = ""

                                while current_idx < len(parts):
                                    if parts[current_idx].isdigit():
                                        if num_fields_found == 0:
                                            temp_attended = int(parts[current_idx])
                                            num_fields_found += 1
                                        elif num_fields_found == 1:
                                            temp_conducted = int(parts[current_idx])
                                            num_fields_found += 1
                                        else:
                                            break # Found two numbers, assume attended and conducted
                                    elif num_fields_found == 2: # After finding attended/conducted, next string is mentor
                                        temp_mentor = parts[current_idx]
                                        break
                                    current_idx += 1

                                attended = temp_attended
                                conducted = temp_conducted
                                mentor = temp_mentor


                                Student.objects.update_or_create(
                                    enrollment_no=enrollment_no,
                                    defaults={
                                        "roll_no": roll_no,
                                        "name": name,
                                        "attended": attended,
                                        "conducted": conducted,
                                        "mentor": mentor,
                                        "s_score": 0.0, # Default value
                                        "batch": 2025, # Default value
                                    }
                                )
                            except Exception as e:
                                print(f"Skipping line: {line}. Error: {e}")
                                messages.warning(request, f"Could not parse line: {line[:50]}... Error: {e}")

            messages.success(request, "PDF data uploaded and students updated successfully!")
            return redirect("student_list")
    else:
        form = UploadPDFForm()
    return render(request, "upload_pdf.html", {"form": form})


def student_list(request):
    students = list(Student.objects.all())

    sort_by = request.GET.get("sort_by", "percentage_desc")

    if sort_by == "roll_asc":
        students.sort(key=lambda x: x.roll_no)
    elif sort_by == "roll_desc":
        students.sort(key=lambda x: x.roll_no, reverse=True)
    elif sort_by == "percentage_asc":
        students.sort(key=lambda x: x.percentage)
    else:  # "percentage_desc"
        students.sort(key=lambda x: x.percentage, reverse=True)

    return render(request, "student_list.html", {"students": students, "sort_by": sort_by})


def home(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == "POST":
        usertype = request.POST.get("usertype")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if usertype == "admin":
            if username == "ljku" and password == "123":
                request.session["admin"] = True
                messages.success(request, "Admin login successful!")
                return redirect("student_list")
            else:
                messages.error(request, "Invalid Admin Credentials!")
                return redirect("home")

        if usertype == "student":
            try:
                student = Student.objects.get(enrollment_no=username)
                if str(student.roll_no) == password:
                    request.session["student_id"] = student.id
                    messages.success(request, f"Welcome, {student.name}!")
                    return redirect("student_dashboard")
                else:
                    messages.error(request, "Invalid Password!")
                    return redirect("home")
            except Student.DoesNotExist:
                messages.error(request, "Student not found!")
                return redirect("home")

    return redirect("home")


from django.db.models import Q

def student_dashboard(request):
    student_id = request.session.get("student_id")
    if not student_id:
        messages.error(request, "Please login to access the dashboard.")
        return redirect("home")

    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        reason = request.POST.get("reason")
        if reason:
            analysis = TextBlob(reason).sentiment
            student.s_score = analysis.polarity
            student.reason_for_low_attendance = reason
            student.save()
            messages.success(
                request,
                f"Reason submitted. Your sentiment score: {student.s_score:.2f}"
            )
            return redirect("student_dashboard")

    # ✅ filter classes based on roll range
    scheduled_classes = ClassSchedule.objects.filter(
        Q(roll_from__isnull=True, roll_to__isnull=True) |
        Q(roll_from__lte=student.roll_no, roll_to__gte=student.roll_no)
    )

    return render(
        request,
        "student_dashboard.html",
        {
            "student": student,
            "scheduled_classes": scheduled_classes,
        }
    )


def schedule_class(request):
    if not request.session.get("admin"):
        messages.error(request, "Access denied. Admin login required.")
        return redirect("home")

    if request.method == "POST":
        form = ClassScheduleForm(request.POST)
        if form.is_valid():
            class_schedule = form.save()

            roll_from = form.cleaned_data.get('roll_from')
            roll_to = form.cleaned_data.get('roll_to')

            if roll_from is not None and roll_to is not None:
                # Increment conducted count only for students within the specified roll range
                Student.objects.filter(roll_no__gte=roll_from, roll_no__lte=roll_to).update(conducted=F("conducted") + 1)
                messages.success(request, f"Class '{class_schedule.title}' scheduled for Roll No. {roll_from}-{roll_to}. Conducted count updated.")
            else:
                # Increment conducted count for all students if no range is specified
                Student.objects.update(conducted=F("conducted") + 1)
                messages.success(request, f"Class '{class_schedule.title}' scheduled for all students. Conducted count updated.")

            return redirect("schedule_class")
        else:
            messages.error(request, "Error scheduling class. Please check the form.")
    else:
        form = ClassScheduleForm()

    scheduled_classes = ClassSchedule.objects.all().order_by('-date', '-start_time')
    return render(request, "schedule_class.html", {"form": form, "scheduled_classes": scheduled_classes})


def delete_class(request, pk):
    if not request.session.get("admin"):
        messages.error(request, "Access denied. Admin login required.")
        return redirect("home")

    class_to_delete = get_object_or_404(ClassSchedule, pk=pk)
    if request.method == "POST":
        class_to_delete.delete()
        messages.success(request, f"Class '{class_to_delete.title}' deleted successfully.")
    return redirect("schedule_class")


def mark_attendance(request):
    class_id = request.GET.get("class_id")  # Get class id from query params
    scheduled_class = None
    if class_id:
        scheduled_class = ScheduledClass.objects.filter(id=class_id).first()

    if request.method == "POST":
        img_base64 = request.POST.get("captured_image")
        if img_base64:
            try:
                # Decode and OCR
                format, imgstr = img_base64.split(';base64,')
                image_data = io.BytesIO(base64.b64decode(imgstr))
                img = Image.open(image_data).convert('L')
                text = pytesseract.image_to_string(img)

                # Extract enrollment no.
                match = re.search(r"\b\d{14}\b", text) or re.search(r"\b\d{10,14}\b", text)
                if match:
                    extracted_enrollment = match.group().strip()

                    try:
                        student = Student.objects.get(enrollment_no=extracted_enrollment)

                        # ✅ Check roll range
                        if scheduled_class and scheduled_class.roll_from and scheduled_class.roll_to:
                            if not (scheduled_class.roll_from <= student.roll_no <= scheduled_class.roll_to):
                                messages.error(request, f"⚠ You are not eligible for this class (Roll: {student.roll_no}).")
                                return render(request, "mark_attendance.html", {"class": scheduled_class})

                        # Mark attendance
                        student.attended = int(student.attended or 0) + 1
                        student.save()
                        messages.success(request, f"✅ Attendance marked for {student.name} ({student.enrollment_no}).")

                    except Student.DoesNotExist:
                        messages.error(request, f"❌ Student not found with enrollment number: {extracted_enrollment}")
                else:
                    messages.error(request, "⚠ No valid enrollment number found in the ID card.")
            except Exception as e:
                messages.error(request, f"⚠ Error processing ID card image: {str(e)}")
    return render(request, "mark_attendance.html", {"class": scheduled_class})

def student_edit(request, pk):
    if not request.session.get("admin"):
        messages.error(request, "Access denied. Admin login required.")
        return redirect("home")

    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f"Student {student.name} updated successfully.")
            return redirect("student_list")
        else:
            messages.error(request, "Error updating student. Please check the form.")
    else:
        form = StudentEditForm(instance=student)
    return render(request, "student_edit.html", {"form": form, "student": student})


def student_delete(request, pk):
    if not request.session.get("admin"):
        messages.error(request, "Access denied. Admin login required.")
        return redirect("home")

    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, f"Student {student.name} deleted successfully.")
        return redirect("student_list")
    # For GET request, render a confirmation page (optional, but good practice)
    return render(request, "student_confirm_delete.html", {"student": student})

