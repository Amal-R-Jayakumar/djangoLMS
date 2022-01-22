from courses.models import Session,Course,TestQuestion
course = Course.objects.get(slug='more-2019')
session = Session.objects.get(session_number=52)
questions = [
    "What is the purpose of MS Office, Outlook?",
    "Is it possible to add G-mail account with Outlook platform?",
    "Purpose of ‘Tell me what you want to do option’ in outlook?",
    "How to create an Outlook shortcut key from desktop?",
    "Is it possible to create/ delete folders inside Outlook? "
    ]
opt1_list = [
    "For creating notes & presentation",
    "Yes",
    "Helps to save an email.",
    "Properties > Shortcut > Shortcut key",
    "Possible only on Outlook 2021 latest version",
]
opt2_list = [
    "For sharing files",
    "No",
    "Helps to find the appropriate tool for the best action.",
    "Properties > Shortcut > Keyboard settings > Shortcut key",
    "Yes",
]
opt3_list = [
    "Primarily for sharing email and personal information management system.",
    "Only outlook mail-id could be added.",
    "Leads to Outlook video tutorial class.",
    "Properties > General > Application settings > Keyboard > Shortcut key",
    "No",
]

opt4_list = [
    "None of these",
    "None of these",
    "None of these",
    "Properties > General > Windows Shortkey",
    "There is no folder option in outlook",

]
correct_ans = [
    "Primarily for sharing email and personal information management system.",
    "Yes",
    "Helps to find the appropriate tool for the best action.",
    "Properties > Shortcut > Shortcut key",
    "Yes",

]
for i in range(5):
    TestQuestion.objects.create(course=course,session=session,question=questions[i],opt1=opt1_list[i],opt2=opt2_list[i],opt3=opt3_list[i],opt4=opt4_list[i],correct_ans=correct_ans[i])
