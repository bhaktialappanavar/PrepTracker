from django.contrib import admin
from .models import Skill, Topic, DailyTask, StudyLog


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "name",
        "progress",
    )

    search_fields = (
        "name",
        "user__username",
    )

    list_filter = (
        "user",
    )

    ordering = (
        "name",
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "skill",
        "title",
        "completed",
        "completed_date",
    )

    search_fields = (
        "title",
        "user__username",
        "skill__name",
    )

    list_filter = (
        "completed",
        "skill",
    )

    ordering = (
        "title",
    )


@admin.register(DailyTask)
class DailyTaskAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "title",
        "due_date",
        "completed",
    )

    search_fields = (
        "title",
        "user__username",
    )

    list_filter = (
        "completed",
        "due_date",
    )

    ordering = (
        "-due_date",
    )


@admin.register(StudyLog)
class StudyLogAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "date",
        "hours",
    )

    search_fields = (
        "user__username",
        "notes",
    )

    list_filter = (
        "date",
    )

    ordering = (
        "-date",
    )

