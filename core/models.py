from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
import watson
from jsonfield import JSONField
from sorl.thumbnail import ImageField
import StringIO
from PIL import Image, ImageOps

from util import normalize_name

from majors import MAJOR_CHOICES
from minors import MINOR_CHOICES
MINOR_CHOICES = sorted(MINOR_CHOICES, key=lambda major:major[0]) #Remove when scraper is finished

# Create your models here.

class McUser(models.Model):
  """Fields from default User model:
    username
    first_name
    last_name
    email
    password
    groups
    user_permissions
    is_staff
    is_active
    is_superuser
    last_login
    date_joined
  For more information, go to:
  https://docs.djangoproject.com/en/1.8/ref/contrib/auth/
  """
  user = models.OneToOneField(User)
  first_name = models.CharField(max_length=200, blank=True)
  middle_name = models.CharField(max_length=200, blank=True)
  last_name = models.CharField(max_length=200, blank=True)
  # Real first name
  real_name = models.CharField(max_length=200, blank=True)

  # Gender
  GENDER_CHOICES = (('', ''), ('Male', 'Male'), ('Female', 'Female'))
  gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=False)

  # Birthday
  birthday = models.DateField(null=True, blank=True)

  # e.g. 2012
  YEARS = (
      ('', ''),
      (2000, '2000'), (2001, '2001'), (2002, '2002'), (2003, '2003'), (2004, '2004'), (2005, '2005'),
      (2006, '2006'), (2007, '2007'), (2008, '2008'), (2009, '2009'), (2010, '2010'), (2011, '2011'),
      (2012, '2012'), (2013, '2013'), (2014, '2014'), (2015, '2015')
  )

  class_year = models.IntegerField(choices=YEARS, null=True, blank=True)

  # e.g. 2021135727
  utd_id = models.CharField(max_length=50, blank=True)

  # Personal info
  hometown = models.CharField(max_length=200, blank=True)
  hometown_state = models.CharField(max_length=200, blank=True)
  high_school = models.CharField(max_length=200, blank=True)
  phone_number = models.CharField(max_length=200, blank=True)
  linkedin = models.CharField(max_length=200, blank=True)
  facebook = models.CharField(max_length=200, blank=True)
  website = models.CharField(max_length=200, blank=True)

  # birthday, phone number, email, linkedin, website, facebook can be hidden
  visible_fields = JSONField()


  pic = ImageField(upload_to='img', blank=True)
  # normalized name, e.g. joshcai
  norm_name = models.CharField(max_length=400, blank=True)
  #TODO: add address field
  #TODO: allow multiple phone
  #TODO: allow backup emails

  # Staff only fields
  staff_phone = models.CharField(max_length=200, blank=True)
  staff_title = models.CharField(max_length=200, blank=True)

  def get_full_name(self):
    return '%s %s' % (self.first_name, self.last_name)

  def save(self, *args, **kwargs):
    self.norm_name = normalize_name(self.get_full_name())
    if self.pic:
      image = Image.open(StringIO.StringIO(self.pic.read()))
      if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')

      # Resize to 400x400
      imagefit = ImageOps.fit(image, (400, 400), Image.ANTIALIAS)
      output = StringIO.StringIO()
      imagefit.save(output, 'JPEG', quality=75)
      output.seek(0)
      # TODO: Find a way to delete old image files.
      self.pic = InMemoryUploadedFile(output, 'ImageField',
          '%s.jpg'  % self.norm_name, 'image/jpeg', output.len, None)
    super(McUser, self).save(*args, **kwargs)

class Degree(models.Model):
  user = models.ForeignKey(McUser, related_name='degrees')
  school = models.CharField(max_length=200, blank=True)
  degree_type = models.CharField(max_length=200, blank=True)
  start_time = models.DateField(null=True, blank=True)
  end_time = models.DateField(null=True, blank=True)
  major1 = models.CharField(max_length=200, choices=MAJOR_CHOICES, blank=True)
  major2 = models.CharField(max_length=200, choices=MAJOR_CHOICES, blank=True)
  minor1 = models.CharField(max_length=200, choices=MINOR_CHOICES, blank=True)
  minor2 = models.CharField(max_length=200, choices=MINOR_CHOICES, blank=True)

EXP_CHOICES = (('', ''), ('Research', 'Research'), ('Internship', 'Internship'),
               ('Volunteer', 'Volunteer'), ('Clubs / Leadership', 'Clubs / Leadership'),
               ('Athletic', 'Athletic'), ('Other', 'Other'))

class Experience(models.Model):
  user = models.ForeignKey(McUser, related_name='experiences')
  title = models.CharField(max_length=200, blank=True)
  exp_type = models.CharField(max_length=200, choices=EXP_CHOICES, blank=True)
  organization = models.CharField(max_length=200, blank=True)
  description = models.TextField(blank=True)
  location = models.CharField(max_length=200, blank=True)
  start_time = models.DateField(null=True, blank=True)
  end_time = models.DateField(null=True, blank=True)

STUDY_ABROAD_CHOICES = (('', ''), ('Internship', 'Internship'), ('Coursework', 'Coursework'),
                        ('Independent Study', 'Independent Study'), ('Other', 'Other'))

class StudyAbroad(models.Model):
  user = models.ForeignKey(McUser, related_name='studiesabroad')
  study_abroad_type = models.CharField(max_length=200,
                                       choices=STUDY_ABROAD_CHOICES, blank=True)
  organization = models.CharField(max_length=200, blank=True)
  description = models.TextField(blank=True)
  primary_location = models.CharField(max_length=200, blank=True)
  other_locations = models.CharField(max_length=200, blank=True)
  start_time = models.DateField(null=True, blank=True)
  end_time = models.DateField(null=True, blank=True)

watson.register(McUser, fields=('first_name', 'last_name', 'gender', 'class_year', 'hometown', 'high_school',
                                'norm_name'))
watson.register(Degree)
watson.register(Experience)
watson.register(StudyAbroad)
# at bottom for circular dependency
import signals
