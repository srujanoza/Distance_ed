from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class Student(models.Model):
    STUDENT_STATUS_CHOICES = [
        ('ER', 'Enrolled'),
        ('SP', 'Suspended'),
        ('GD', 'Graduated'),
    ]
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

    username = models.CharField(max_length=100, validators=[alphanumeric], default='defaultuser123')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date_of_birth = models.DateField()
    status = models.CharField(max_length=10, choices=STUDENT_STATUS_CHOICES, default='enrolled')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()
    student = models.ManyToManyField(Student)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Course(models.Model):
    LEVEL_CHOICES = [
        ("BE", "Beginner"),
        ("IN", "Intermediate"),
        ("AD", "Advanced"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, default=None)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default="BE")
    interested = models.PositiveIntegerField(default=0)
    interested_students = models.ManyToManyField(Student, related_name='interested_courses', blank=True)

    def get_level_id(self):
        if self.level == "BE":
            return 1
        elif self.level == "IN":
            return 2
        elif self.level == "AD":
            return 3

    def __str__(self):
        return f'{self.title}'


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        (0, 'Order Confirmed'),
        (1, 'Order Cancelled'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    order_date = models.DateField(default=timezone.now)
    order_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    levels = models.PositiveIntegerField(default=1)

    def discount(self):
        discount_value = 0.1 * float(self.course.price)  # 10% discount
        self.order_price = float(self.course.price) - discount_value

    def __str__(self):
        return f'{self.student} - {self.course} - {self.get_order_status_display()}'
