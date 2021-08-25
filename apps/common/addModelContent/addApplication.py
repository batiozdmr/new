from ...parameter.models import Application, ApplicationEvaluation, Program


def ApplicationAdd(program=None, team=None, applicant=None):
    contentProgram = Program.objects.filter(id=program.id).first()
    if contentProgram.noLimit == False:
        checkApplication = Application.objects.filter(program=program, applicantTeam_id=team, applicant=applicant)
        if checkApplication:
            pass
        else:
            Application.objects.create(program=program, applicantTeam_id=team, applicant=applicant)
    else:
        Application.objects.create(program=program, applicantTeam_id=team, applicant=applicant)


def ApplicationEvaluationAdd(application=None, newStatus=None):
    checkApplicationEvaluation = ApplicationEvaluation.objects.filter(application=application, newStatus=newStatus)

    if checkApplicationEvaluation:
        pass
    else:
        applicationEvaluatinAdd = ApplicationEvaluation()
        applicationEvaluatinAdd.application = application
        applicationEvaluatinAdd.newStatus = newStatus
        applicationEvaluatinAdd.save()
