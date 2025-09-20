from django.shortcuts import render,redirect
import base64

def dashboard(request):
    return render(request, 'tools/dashboard.html')

def cv_maker(request):
    return redirect("https://old.likhon.com.bd/tools/cv-maker/")
    if request.method == 'POST':
        photo_base64 = None
        if request.FILES.get('photo'):
            photo = request.FILES['photo']
            photo_base64 = base64.b64encode(photo.read()).decode('utf-8')

        signature_base64 = None
        if request.FILES.get('signature'):
            signature = request.FILES['signature']
            signature_base64 = base64.b64encode(signature.read()).decode('utf-8')

        education_type = request.POST.get('education_type')
        educations = []
        if education_type == 'table':
            exam_names = request.POST.getlist('exam_name')
            institutes = request.POST.getlist('institute')
            passing_years = request.POST.getlist('passing_year')
            results = request.POST.getlist('result')
            for i in range(len(exam_names)):
                educations.append({
                    'exam_name': exam_names[i],
                    'institute': institutes[i],
                    'passing_year': passing_years[i],
                    'result': results[i],
                })
        else:
            educations = request.POST.getlist('education_simple')

        experience_type = request.POST.get('experience_type')
        experiences = []
        if experience_type == 'table':
            company_names = request.POST.getlist('company_name')
            positions = request.POST.getlist('position')
            start_dates = request.POST.getlist('start_date')
            end_dates = request.POST.getlist('end_date')
            for i in range(len(company_names)):
                experiences.append({
                    'company_name': company_names[i],
                    'position': positions[i],
                    'start_date': start_dates[i],
                    'end_date': end_dates[i],
                })
        else:
            experiences = request.POST.getlist('experience_simple')

        context = {
            'preview': True,
            'name': request.POST.get('name'),
            'fatherName': request.POST.get('fatherName'),
            'motherName': request.POST.get('motherName'),
            'nationality': request.POST.get('nationality'),
            'dob': request.POST.get('dob'),
            'religion': request.POST.get('religion'),
            'maritalStatus': request.POST.get('maritalStatus'),
            'gender': request.POST.get('gender'),
            'blood_group': request.POST.get('blood_group'),
            'height': request.POST.get('height'),
            'weight': request.POST.get('weight'),
            'skills': request.POST.get('skills'),
            'mobileNumber': request.POST.get('mobileNumber'),
            'email': request.POST.get('email'),
            'presentAddress': request.POST.get('presentAddress'),
            'permanentAddress': request.POST.get('permanentAddress'),
            'photo': photo_base64,
            'signature': signature_base64,
            'education_type': education_type,
            'educations': educations,
            'experience_type': experience_type,
            'experiences': experiences,
        }
        return render(request, 'tools/cvmaker.html', context)
    return render(request, 'tools/cvmaker.html')