from college_or_atc.models import StudyCenter
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.urls import reverse
from accounts.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import os
from django.conf import settings
import slugify
# Create your models here.


################## COURSE MODEL ##################
class Category(models.Model):
    category_name = models.CharField(max_length=60)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"


class Course(models.Model):
    # CATEGORY = (
    #     ('Software', 'Software'),
    #     ('Hardware', 'Hardware'),
    #     ('Multimedia', 'Multimedia')
    # )
    course_name = models.CharField(max_length=200)
    slug = models.SlugField(default='', max_length=255, editable=False)
    course_description = models.TextField()
    course_image = models.ImageField(
        upload_to='images/course_images', default='images/default.png')
    completion_time = models.DurationField()
    rating = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    instructor = models.ForeignKey(
        User, related_name="course", on_delete=models.SET_NULL, null=True)

    students = models.ManyToManyField(
        User, through='Enrollment', related_name="student_course", editable=True)
    # enrollment = models.ForeignKey(Enrollment)

    def __str__(self):
        return self.course_name

    def save(self, *args, **kwargs):
        self.slug = slugify.slugify(self.course_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['course_name']


################## COURSE SECTIONS ##################


class Session(models.Model):
    session_number = models.IntegerField()
    session = models.CharField(max_length=100)
    slug = models.SlugField(default='', max_length=255, editable=False)
    is_open = models.BooleanField(default=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'Day {self.session_number} Title: {self.session}'

    def save(self, *args, **kwargs):
        self.slug = slugify.slugify(self.session)
        super().save(*args, **kwargs)

################## COURSE LESSONS ##################


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='', max_length=255, editable=False)
    video_url = models.URLField(max_length=200)
    lesson_number = models.IntegerField()
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return F'{self.session.session_number} Session {self.session.session} - Lesson {self.lesson_number}........ Title: {self.title}'

    def get_absolute_url(self):
        return reverse("courses:lesson_detail", kwargs={"course_slug": self.subject.slug, 'lesson_slug': self.slug})
        ###############################
        # SHOULD DEAL WITH THIS LATER #
        ###############################

    def save(self, *args, **kwargs):
        self.slug = slugify.slugify(self.title)
        super().save(*args, **kwargs)


################## COURSE RESOURCE MODEL ##################


class Resource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    resource_name = models.CharField(max_length=200, blank=False)
    # {User.username}/{Course.course_name}/
    # resource_file = models.FileField( upload_to=get_upload_path)
    resource_link = models.URLField(max_length=300)

    def __str__(self):
        return self.resource_name

    def get_absolute_url(self):
        return reverse('courses:list')

################## ASSIGNMENT MODEL ##################


class Assignment(models.Model):
    assignment_name = models.CharField(max_length=200, blank=False)
    assignment_description = models.TextField(blank=False)
    # start_date = models.DateTimeField(default=timezone.now)
    # due_date = models.DateTimeField(blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='images/assignments', blank=True, null=True)

    def __str__(self):
        return f'{self.lesson.session.session_number} - {self.lesson.session.session} - {self.lesson.lesson_number} - {self.assignment_name}'

    def get_absolute_url(self):
        return reverse('courses:assignment_detail', kwargs={'pk': self.pk})

def course_directory_path(instance, filename):
    return 'answerkey/course_{0}/assignment_{1}/{2}'.format(instance.course.course_name,instance.section_name, filename)


class AnswerKey(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_section = models.CharField(max_length=300)
    # resource = models.FileField(upload_to=course_directory_path)
    resource = models.CharField(max_length=400)

    def __str__(self):
        return f'{self.course.course_name} -- {self.course_section}'

################## SUBMIT ASSIGNMENT MODEL ##################
def user_directory_path(instance, filename):
    return 'assignments/user_{0}/{1}'.format(instance.user.username, filename)


class SubmitAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    assignment = models.ForeignKey(
        Assignment, related_name="question", on_delete=models.CASCADE)
    # validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'doc', 'pptx', ])])
    assignment_file = models.FileField(
        blank=False, upload_to=user_directory_path)
    submitted_date = models.DateTimeField()
    graded = models.BooleanField(default=False)
    grade = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])

    def __str__(self):
        return f'Session: {self.assignment.lesson.session.session_number}-- Lesson: {self.assignment.lesson.lesson_number}--{self.assignment.assignment_name} by {self.user.name}'

    def grade_assignment(self, grade):
        self.grade = grade
        self.graded = True
        self.save()

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.assignment_file.name))
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:submit_detail', kwargs={'pk': self.pk})


class TestQuestion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)
    opt1 = models.CharField(max_length=500)
    opt2 = models.CharField(max_length=500)
    opt3 = models.CharField(max_length=500)
    opt4 = models.CharField(max_length=500)
    correct_ans = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.session.session_number} - {self.question}'


class ConductTest(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_date = models.DateTimeField(default=timezone.now)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(0)])
    is_improved = models.BooleanField(default=False)

    def __str__(self):
        return f'Session: {self.session.session_number} || Student: {self.user.name} || Marks: {self.marks}'

################## COURSE ENROLLMENT ##################


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # study_center = models.ForeignKey(StudyCenter, on_delete=models.CASCADE)
    college = models.ForeignKey(StudyCenter, on_delete=models.CASCADE)
    enrollment_date = models.DateField(default=timezone.now)
    assignment_marks = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    assignments_total_obtainable_marks = models.IntegerField(default=0)
    final_cumulative_marks = models.IntegerField(default=0)
    total_obtainable_marks = models.IntegerField(default=0)

    def __str__(self):
        return f'enrollment - {self.student.username} - {self.course}'

    class Meta:
        unique_together = ('course', 'student')

class AssignmentGrading(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    assignment_avg_marks = models.DecimalField(max_digits=3, decimal_places=2)
    all_graded = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student.name}  --  {self.session.session} -- {self.assignment_avg_marks}'
