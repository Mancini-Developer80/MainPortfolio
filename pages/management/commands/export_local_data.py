from django.core.management.base import BaseCommand
from pages.models import CaseStudy
from blog.models import BlogPost
import json
import sys
import io

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class Command(BaseCommand):
    help = 'Exports all case studies and blog posts to import_data.py format'

    def handle(self, *args, **options):
        self.stdout.write('Exporting data from local database...\n')
        
        # Export Case Studies
        case_studies = CaseStudy.objects.all()
        self.stdout.write(f'\n=== CASE STUDIES ({case_studies.count()}) ===')
        self.stdout.write('Copy this into import_data.py:\n')
        
        cs_list = []
        for cs in case_studies:
            cs_dict = {
                'title': cs.title,
                'slug': cs.slug,
                'short_description': cs.short_description or '',
                'full_description': cs.full_description or '',
                'purpose': cs.purpose or '',
                'features': cs.features or '',
                'architecture': cs.architecture or '',
                'technical_challenges': cs.technical_challenges or '',
                'accomplishments': cs.accomplishments or '',
                'final_consideration': cs.final_consideration or '',
                'technologies': [tech.name for tech in cs.technologies.all()],
                'live_url': cs.live_url or '',
                'github_url': cs.github_url or '',
                'order': cs.order,
                'is_featured': cs.is_featured,
            }
            cs_list.append(cs_dict)
            
        print('case_studies_data = ' + json.dumps(cs_list, indent=4, ensure_ascii=False))
        
        # Export Blog Posts
        blog_posts = BlogPost.objects.all()
        self.stdout.write(f'\n\n=== BLOG POSTS ({blog_posts.count()}) ===')
        self.stdout.write('Copy this into import_data.py:\n')
        
        bp_list = []
        for bp in blog_posts:
            bp_dict = {
                'title': bp.title,
                'slug': bp.slug,
                'excerpt': bp.excerpt or '',
                'content': bp.content or '',
                'is_published': bp.is_published,
            }
            bp_list.append(bp_dict)
            
        print('blog_posts_data = ' + json.dumps(bp_list, indent=4, ensure_ascii=False))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Export complete! Copy the data above into import_data.py'))
        self.stdout.write('Note: Images need to be re-uploaded via admin panel on Render')
