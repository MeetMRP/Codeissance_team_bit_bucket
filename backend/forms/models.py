from django.db import models
from accounts.models import AccountsUser

class Form(models.Model):
    title = models.CharField(max_length=255)

    creator = models.ForeignKey(
        AccountsUser, 
        on_delete=models.CASCADE, 
        related_name="created_forms"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    TEXT = 'text'
    MCQ = 'multiple_choice'
    
    QUESTION_TYPES = [
        (TEXT, 'Text'),
        (MCQ, 'Multiple Choice')
    ]

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    question_type = models.CharField(max_length=255, choices=QUESTION_TYPES, default=TEXT)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Response(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="responses")
    user = models.ForeignKey(AccountsUser, on_delete=models.CASCADE, related_name="responses")
    created_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text_answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Answer to {self.question.text}"
