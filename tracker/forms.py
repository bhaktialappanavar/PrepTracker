from django import forms
from .models import Skill, Topic, DailyTask, StudyLog
from django.core.exceptions import ValidationError
from datetime import date


class SkillForm(forms.ModelForm):

    class Meta:
        model = Skill
        fields = ["name"]
        labels = {
            "name": "Skill",
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        user = self.initial.get("user")
        if user:
            exists = Skill.objects.filter(
                user=user,
                name__iexact=name
            )
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)
            if exists.exists():
                raise ValidationError(
                    "You already have this skill."
                )
        return name


class TopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = [
            "skill",
            "title",
            "completed",
        ]

    def clean(self):
        cleaned_data = super().clean()
        skill = cleaned_data.get("skill")
        title = cleaned_data.get("title")
        if skill and title:
            exists = Topic.objects.filter(
                skill=skill,
                title__iexact=title.strip(),
                user=self.initial.get("user")
            )
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)
            if exists.exists():
                raise forms.ValidationError(
                    "This topic already exists for the selected skill."
                )
        return cleaned_data

class DailyTaskForm(forms.ModelForm):

    class Meta:
        model = DailyTask
        fields = [
            "title",
            "due_date",
            "completed",
        ]

    def clean_due_date(self):
        due_date = self.cleaned_data["due_date"]
        if due_date < date.today():
            raise forms.ValidationError(
                "Due date cannot be in the past."
            )
        return due_date


class StudyLogForm(forms.ModelForm):

    class Meta:
        model = StudyLog
        fields = [
            "date",
            "hours",
            "notes",
        ]

    def clean_hours(self):
        hours = self.cleaned_data["hours"]
        if hours <= 0:
            raise forms.ValidationError(
                "Study hours must be greater than 0."
            )
        if hours > 24:
            raise forms.ValidationError(
                "Study hours cannot exceed 24 hours in a day."
            )
        return hours
    
    def clean_notes(self):
        notes = self.cleaned_data["notes"].strip()
        if len(notes) < 5:
            raise forms.ValidationError(
                "Please enter meaningful study notes."
            )
        return notes

