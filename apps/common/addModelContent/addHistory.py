from ...parameter.models import History

def historyAdd(application=None, staff=None, status=None, innerExplanation=None, externalExplanation=None,score=None,externalHistory=True):
    checkHistory = History.objects.filter(application=application, status=status, innerExplanation=innerExplanation,
                                          externalExplanation=externalExplanation,score=score)
    if checkHistory:
        pass
    else:
        checkHistoryInternal = History.objects.filter(application=application, status=status,
                                                      externalExplanation=externalExplanation)
        if checkHistoryInternal:

            History.objects.create(application=application, staff=staff, status=status,
                                   innerExplanation=innerExplanation,
                                   externalExplanation=externalExplanation,score=score, externalHistory=False)
        else:

            History.objects.create(application=application, staff=staff, status=status,
                                   innerExplanation=innerExplanation,
                                   externalExplanation=externalExplanation,score=score, externalHistory=True)
