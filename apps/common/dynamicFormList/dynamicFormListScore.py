def dynamicFormScoreSum(answer=None, question=None, questionValue=None):
    scoreSum = 0
    scoreList = []
    for index, item in enumerate(answer):
        if (index + 1) % question.count() == 0:
            if item.dynamicQuestion.dynamicQuestionType_id == 6 or item.dynamicQuestion.dynamicQuestionType_id == 7:
                valueSTR = (item.answer[2:-2])
                valueList = valueSTR.split("', '")
                for i in valueList:
                    newScore = questionValue.objects.filter(id=i).first()
                    if newScore:
                        scoreSum = scoreSum + newScore.score

            else:
                scoreSum = scoreSum + item.dynamicQuestion.score

            scoreList.append({"user_id": item.user, "user_score": scoreSum, "user_form": item.dynamicForm})

            scoreSum = 0

        else:
            if item.dynamicQuestion.dynamicQuestionType_id == 6 or item.dynamicQuestion.dynamicQuestionType_id == 7:
                valueSTR = (item.answer[2:-2])
                valueList = valueSTR.split("', '")
                for i in valueList:
                    newScore = questionValue.objects.filter(id=i).first()
                    if newScore:
                        scoreSum = scoreSum + newScore.score


            else:
                scoreSum = scoreSum + item.dynamicQuestion.score

            scoreList.append({"user_id": item.user, "user_score": scoreSum, "user_form": item.dynamicForm})

    return scoreList
