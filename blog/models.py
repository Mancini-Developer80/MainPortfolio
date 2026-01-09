from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


class Tag(models.Model):
    """Blog post tags for organizing content"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:tag_posts', kwargs={'slug': self.slug})


class BlogPost(models.Model):
    """Main blog post model with rich content and SEO"""
    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='blog_posts')
    
    # Content
    excerpt = models.TextField(max_length=300, help_text='Short description for card previews (max 300 chars)')
    content = RichTextField(help_text='Full blog post content with rich text formatting')
    featured_image = CloudinaryField('image', blank=True, null=True, help_text='Main image for the post')
    
    # Organization
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    # Status & Features
    is_published = models.BooleanField(default=False, help_text='Post is visible to readers')
    is_featured = models.BooleanField(default=False, help_text='Display prominently on blog home')
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True, help_text='SEO meta description (max 160 chars)')
    meta_keywords = models.CharField(max_length=255, blank=True, help_text='SEO keywords, comma-separated')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True, help_text='When post was first published')
    
    # Stats
    views_count = models.PositiveIntegerField(default=0, editable=False)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        indexes = [
            models.Index(fields=['-published_at', '-created_at']),
            models.Index(fields=['slug']),
        ]
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Set published_at on first publish
        if self.is_published and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        
        # Auto-generate meta description from excerpt if not provided
        if not self.meta_description and self.excerpt:
            self.meta_description = self.excerpt[:160]
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def get_reading_time(self):
        """Calculate estimated reading time in minutes"""
        from django.utils.html import strip_tags
        word_count = len(strip_tags(self.content).split())
        minutes = max(1, round(word_count / 200))  # Assuming 200 words per minute
        return f"{minutes} min read"
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
