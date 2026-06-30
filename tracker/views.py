from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from .models import Skill, Topic, DailyTask, StudyLog
from .forms import SkillForm, TopicForm, DailyTaskForm, StudyLogForm

def update_skill_progress(skill):
    total_topics = Topic.objects.filter(skill=skill).count()
    completed_topics = Topic.objects.filter(
        skill=skill,
        completed=True
    ).count()
    if total_topics == 0:
        skill.progress = 0
    else:
        skill.progress = int((completed_topics / total_topics) * 100)

    skill.save()



# HOME

def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "home.html")

# DASHBOARD

@login_required
def dashboard(request):
    skills = Skill.objects.filter(user=request.user)
    topics = Topic.objects.filter(user=request.user)
    tasks = DailyTask.objects.filter(
        user=request.user,
        completed=False
    ).order_by("-id")[:5]
    studylogs = StudyLog.objects.filter(
        user=request.user
    ).order_by("-date")[:5]
    total_skills = skills.count()
    completed_topics = topics.filter(
        completed=True
    ).count()
    pending_tasks = DailyTask.objects.filter(
        user=request.user,
        completed=False
    ).count()
    study_hours = sum(
        log.hours
        for log in StudyLog.objects.filter(user=request.user)
    )
    completed = completed_topics
    remaining = total_skills - completed_topics
    study_data = [log.hours for log in studylogs]
    total_topics = topics.count()
    if total_topics:
        progress = int((completed_topics / total_topics) * 100)
    else:
        progress = 0

    progress = min(progress, 100)
    context = {
        "skills": skills,
        "tasks": tasks,
        "studylogs": studylogs,

        "total_skills": total_skills,
        "completed_topics": completed_topics,
        "pending_tasks": pending_tasks,
        "study_hours": study_hours,
        "progress": progress,

        "completed": completed,
        "remaining": remaining,
        "study_data": study_data,
    }
    return render(request, "dashboard.html", context)

# SKILL CRUD

@login_required
def skill_list(request):
    skills = Skill.objects.filter(
        user=request.user
    )
    return render(request,
                "skills/skill_list.html",
                {"skills": skills},
    )


@login_required
def add_skill(request):
    if request.method == "POST":
        form = SkillForm(request.POST,
        initial={
        "user": request.user
    }
)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(
                request,
                "Skill added successfully."
            )
            return redirect("skill_list")
    else:
        form = SkillForm(initial={
        "user": request.user
    }
)
    return render(
        request,
        "skills/add_skill.html",
        {"form": form},
    )


@login_required
def edit_skill(request, id):
    skill = get_object_or_404(
        Skill,
        id=id,
        user=request.user,
    )
    if request.method == "POST":
        form = SkillForm(
        request.POST,
        instance=skill,
        initial={
        "user": request.user
    }
)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Skill updated successfully."
            )
            return redirect("skill_list")
    else:
        form = SkillForm(
        instance=skill,
        initial={
        "user": request.user
    }
)
    return render(
        request,
        "skills/edit_skill.html",
        {"form": form},
    )


@login_required
def delete_skill(request, id):
    skill = get_object_or_404(
        Skill,
        id=id,
        user=request.user,
    )
    if request.method == "POST":
        skill.delete()
        messages.success(
            request,
            "Skill deleted successfully."
        )
        return redirect("skill_list")
    return render(
        request,
        "skills/delete_skill.html",
        {"skill": skill},
    )


# TOPIC CRUD

@login_required
def topic_list(request):
    topics = Topic.objects.filter(user=request.user)
    return render(request, "topics/topic_list.html", {
        "topics": topics
    })


@login_required
def add_topic(request):
    if request.method == "POST":
        form = TopicForm(
        request.POST,
        initial={"user": request.user}
)
        form.fields["skill"].queryset = Skill.objects.filter(
            user=request.user
        )
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user
            if topic.completed:
                topic.completed_date = date.today()
            else:
                topic.completed_date = None
            topic.save()
            update_skill_progress(topic.skill)
            messages.success(
                request,
                "Topic added successfully."
            )
            return redirect("topic_list")
    else:
        form = TopicForm(
        initial={"user": request.user}
        )
        form.fields["skill"].queryset = Skill.objects.filter(
            user=request.user
        )
    return render(
        request,
        "topics/add_topic.html",
        {"form": form},
    )


@login_required
def edit_topic(request, id):
    topic = get_object_or_404(
        Topic,
        id=id,
        user=request.user,
    )
    if request.method == "POST":
        form = TopicForm(
        request.POST,
        instance=topic,
        initial={"user": request.user}
)
        form.fields["skill"].queryset = Skill.objects.filter(
            user=request.user
        )
        if form.is_valid():
            topic = form.save(commit=False)
            if topic.completed:
                if not topic.completed_date:
                    topic.completed_date = date.today()
            else:
                topic.completed_date = None
            topic.save()
            update_skill_progress(topic.skill)
            messages.success(
            request,
            "Topic updated successfully."
            )
            return redirect("topic_list")
    else:
        form = TopicForm(
        instance=topic,
        initial={"user": request.user}
        )
        form.fields["skill"].queryset = Skill.objects.filter(
            user=request.user
        )
    return render(
        request,
        "topics/edit_topic.html",
        {"form": form},
    )


@login_required
def delete_topic(request, id):
    topic = get_object_or_404(
        Topic,
        id=id,
        user=request.user,
    )
    if request.method == "POST":
        skill = topic.skill
        topic.delete()
        update_skill_progress(skill)
        messages.success(
            request,
            "Topic deleted successfully."
        )
        return redirect("topic_list")
    return render(
        request,
        "topics/delete_topic.html",
        {"topic": topic},
    )

# TASK CRUD

@login_required
def task_list(request):
    tasks = DailyTask.objects.filter(
        user=request.user
    ).order_by("due_date")
    return render(
        request,
        "tasks/task_list.html",
        {"tasks": tasks},
    )


@login_required
def add_task(request):
    if request.method == "POST":
        form = DailyTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(
                request,
                "Task added successfully."
            )
            return redirect("task_list")
    else:
        form = DailyTaskForm()
    return render(
        request,
        "tasks/add_task.html",
        {"form": form},
    )


@login_required
def edit_task(request, id):
    task = get_object_or_404(
        DailyTask,
        id=id,
        user=request.user,
    )
    if request.method == "POST":
        form = DailyTaskForm(
            request.POST,
            instance=task
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Task updated successfully."
            )
            return redirect("task_list")
    else:
        form = DailyTaskForm(instance=task)
    return render(
        request,
        "tasks/edit_task.html",
        {"form": form},
    )


@login_required
def delete_task(request, id):
    task = get_object_or_404(
        DailyTask,
        id=id,
        user=request.user,
    )
    if request.method == "POST":
        task.delete()
        messages.success(
            request,
            "Task deleted successfully."
        )
        return redirect("task_list")
    return render(
        request,
        "tasks/delete_task.html",
        {"task": task},
    )

# STUDY LOG CRUD

@login_required
def studylog_list(request):
    studylogs = StudyLog.objects.filter(
        user=request.user
    ).order_by("-date")
    return render(
        request,
        "studylogs/studylog_list.html",
        {"studylogs": studylogs},
    )


@login_required
def add_studylog(request):
    if request.method == "POST":
        form = StudyLogForm(request.POST)
        if form.is_valid():
            studylog = form.save(commit=False)
            studylog.user = request.user
            studylog.save()
            messages.success(
                request,
                "Study log added successfully."
            )
            return redirect("studylog_list")
    else:
        form = StudyLogForm()
    return render(
        request,
        "studylogs/add_studylog.html",
        {"form": form},
    )


@login_required
def edit_studylog(request, id):
    studylog = get_object_or_404(
        StudyLog,
        id=id,
        user=request.user,
    )
    if request.method == "POST":
        form = StudyLogForm(
            request.POST,
            instance=studylog
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Study log updated successfully."
            )
            return redirect("studylog_list")
    else:
        form = StudyLogForm(instance=studylog)
    return render(
        request,
        "studylogs/edit_studylog.html",
        {"form": form},
    )


@login_required
def delete_studylog(request, id):
    studylog = get_object_or_404(
        StudyLog,
        id=id,
        user=request.user,
    )
    if request.method == "POST":
        studylog.delete()
        messages.success(
            request,
            "Study log deleted successfully."
        )
        return redirect("studylog_list")
    return render(
        request,
        "studylogs/delete_studylog.html",
        {"studylog": studylog},
    )


