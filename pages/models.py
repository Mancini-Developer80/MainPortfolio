from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

class Technology(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class CaseStudy(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.TextField(max_length=300)
    full_description = models.TextField()
    
    # New detailed fields
    purpose = models.TextField(blank=True, null=True, help_text="Project purpose and objectives")
    features = models.TextField(blank=True, null=True, help_text="Key features (one per line)")
    architecture = models.TextField(blank=True, null=True, help_text="System architecture details (one per line)")
    technical_challenges = models.TextField(blank=True, null=True, help_text="Technical challenges faced (one per line)")
    accomplishments = models.TextField(blank=True, null=True, help_text="Key accomplishments and outcomes")
    final_consideration = models.TextField(blank=True, null=True, help_text="Final thoughts and lessons learned")
    
    technologies = models.ManyToManyField(Technology, related_name='case_studies')
    image = CloudinaryField('image', blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Case Study"
        verbose_name_plural = "Case Studies"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('pages:case-detail', kwargs={'slug': self.slug})
    
    def get_tech_classes(self):
        """Return space-separated list of technology slugs for filtering"""
        return ' '.join([tech.slug for tech in self.technologies.all()])


class ContactSubmission(models.Model):
    """Model for storing contact form submissions"""
    STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read'),
        ('responded', 'Responded'),
    ]
    
    subject = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unread')
    submitted_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Admin notes about this submission")
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.submitted_at.strftime('%Y-%m-%d')})"
