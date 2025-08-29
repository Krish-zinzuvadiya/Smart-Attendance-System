from django import forms
from .models import ClassSchedule, Student

class UploadPDFForm(forms.Form):
    file = forms.FileField()

class ClassScheduleForm(forms.ModelForm):
    class Meta:
        model = ClassSchedule
        fields = ['title', 'date', 'start_time', 'end_time', 'conducted_by', 'roll_from', 'roll_to', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Class Title'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'conducted_by': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Conducted By'}),
            'class_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Class No'}),
            'roll_from': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Roll From (Optional)'}),
            'roll_to': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Roll To (Optional)'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional Notes (Optional)'}),
        }

class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_no', 'enrollment_no', 'name', 'attended', 'conducted', 'mentor', 'batch', 'reason_for_low_attendance', 's_score']
        widgets = {
            'reason_for_low_attendance': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'roll_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'enrollment_no': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'attended': forms.NumberInput(attrs={'class': 'form-control'}),
            'conducted': forms.NumberInput(attrs={'class': 'form-control'}),
            'mentor': forms.TextInput(attrs={'class': 'form-control'}),
            'batch': forms.NumberInput(attrs={'class': 'form-control'}),
            's_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

