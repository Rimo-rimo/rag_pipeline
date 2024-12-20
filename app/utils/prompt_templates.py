# ======================== basic chat 템플릿 ========================

basic_text_qa_template = (
    "다음은 컨텍스트 정보입니다.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "컨텍스트 정보만을 참고하여, 기존 지식에 의존하지 않고 질문에 답변해 주세요.\n"
    "답변은 꼭 한국어로 해줘야 합니다.\n"
    "답변은 마크다운 형식으로 보기 좋게 생성해 줘야합니다.\n"
    "질문: {query_str}\n"
    "답변: "
)

basic_refine_template = (
    "기존 질문은 다음과 같습니다: {query_str}\n"
    "다음은 질문에 대한 기존의 답변입니다: {existing_answer}\n"
    "아래의 추가 컨텍스트 정보를 바탕으로 기존 답변을 개선할 기회가 있습니다. (필요한 경우에만).\n"
    "------------\n"
    "{context_msg}\n"
    "------------\n"
    "새로운 컨텍스트를 참고하여, 원래 답변을 질문에 더 잘 맞도록 수정해 주세요. 만약 컨텍스트가 유용하지 않다면, 기존 답변을 반환해 주세요.\n"
    "답변은 꼭 한국어로 해줘야 합니다.\n"
    "답변은 마크다운 형식으로 보기 좋게 생성해 줘야합니다.\n"
    "수정된 답변: "
)


# ======================== nursing 문제 풀이 템플릿 ========================
nursing_assistant_test_text_qa_template = (
    "다음은 컨텍스트 정보입니다.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "컨텍스트 정보만을 참고하여, 기존 지식에 의존하지 않고 문제를 풀어 주세요.\n"
    "답변은 꼭 한국어로 해줘야 합니다.\n"
    "답변은 dictionay 형태로, 'answer'와 'commentary'키값으로 제공해 주셔야 합니다.\n"
    "<예시 답변>\n"
    "{'answer': 3, 'commentary':'갑상샘기능저하증의 심각한 합병증인 점액수종혼수의 증상\n\n점액수종혼수는 갑상샘기능저하증의 심각한 합병증으로, 다음과 같은 증상이 나타납니다:\n\n1. **기초대사율의 급격한 감소**\n2. **과소환기와 호흡산증**\n3. **저체온증**\n4. **저혈압**\n5. **저나트륨혈증**\n6. **고칼슘혈증**\n7. **이차성 부신기능장애**\n8. **저혈당**\n9. **수분증독증**\n\n이러한 증상들은 점액수종혼수가 발생할 경우 사망률이 높아지므로, 즉각적인 치료가 필요합니다.\n'}\n"
    "</예시 답변>\n"
    "문제: {query_str}\n"
    "답변: "
)

nursing_assistant_test_refine_template = (
    "기존 문제는 다음과 같습니다: {query_str}\n"
    "다음은 문제에 대한 기존의 답변입니다: {existing_answer}\n"
    "아래의 추가 컨텍스트 정보를 바탕으로 기존 답변을 개선할 기회가 있습니다. (필요한 경우에만).\n"
    "------------\n"
    "{context_msg}\n"
    "------------\n"
    "새로운 컨텍스트를 참고하여, 원래 답변을 문제에 더 잘 맞도록 수정해 주세요. 만약 컨텍스트가 유용하지 않다면, 기존 답변을 반환해 주세요.\n"
    "답변은 꼭 한국어로 해줘야 합니다.\n"
    "답변은 dictionay 형태로, 'answer'와 'commentary'키값으로 제공해 주셔야 합니다.\n"
    "<예시 답변>\n"
    "{'answer': 3, 'commentary':'갑상샘기능저하증의 심각한 합병증인 점액수종혼수의 증상\n\n점액수종혼수는 갑상샘기능저하증의 심각한 합병증으로, 다음과 같은 증상이 나타납니다:\n\n1. **기초대사율의 급격한 감소**\n2. **과소환기와 호흡산증**\n3. **저체온증**\n4. **저혈압**\n5. **저나트륨혈증**\n6. **고칼슘혈증**\n7. **이차성 부신기능장애**\n8. **저혈당**\n9. **수분증독증**\n\n이러한 증상들은 점액수종혼수가 발생할 경우 사망률이 높아지므로, 즉각적인 치료가 필요합니다.\n'}\n"
    "</예시 답변>\n"
    "수정된 답변: "
)