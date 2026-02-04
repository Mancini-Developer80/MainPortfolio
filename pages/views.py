import os
import requests
import resend
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import ContactSubmission, CaseStudy

# Configura l'API Key (assicurati che sia impostata su Render)
resend.api_key = os.environ.get('RESEND_API_KEY')

def verify_turnstile(token):
    """Verifica il token con l'API di Cloudflare."""
    if not token:
        return False
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    data = {
        'secret': settings.TURNSTILE_SECRET_KEY,
        'response': token,
    }
    try:
        response = requests.post(url, data=data, timeout=5)
        return response.json().get('success', False)
    except Exception:
        return False

def home(request):
    if request.method == 'POST':
        # 1. TURNSTILE CHECK (Nuova difesa primaria)
        token = request.POST.get('cf-turnstile-response')
        if not verify_turnstile(token):
            # Se fallisce la verifica bot, reindirizziamo senza salvare nulla
            return redirect('pages:home')

        # 2. HONEYPOT CHECK (Difesa secondaria legacy)
        if request.POST.get('hp_field'):
            return redirect('pages:home')

        # 3. DATA EXTRACTION & TRUNCATION
        subject_raw = request.POST.get('subject', '').strip()
        name_raw = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()[:250]
        message_raw = request.POST.get('message', '').strip()

        # Tronchiamo per il DB (Anti-Overflow)
        subject = subject_raw[:200]
        name = name_raw[:200]
        
        # 4. ANTI-SPAM ATTACK (Se l'input è assurdamente lungo scartiamo)
        if len(subject_raw) > 1000 or len(name_raw) > 1000:
            return redirect('pages:home')

        if not all([subject, name, email, message_raw]):
            messages.error(request, 'All fields are required.')
            return redirect('pages:home')
        
        try:
            # 5. SALVATAGGIO NEL DB (Tronchiamo anche il messaggio per il DB)
            submission = ContactSubmission.objects.create(
                subject=subject,
                name=name,
                email=email,
                message=message_raw[:1000] # Limite prudenziale per il DB
            )
            
            # 6. SILENZIATORE EMAIL (Logica da Architect)
            # Inviamo email solo se il messaggio originale non è sospettosamente lungo (>2000 char)
            # e solo se non siamo in DEBUG.
            if not settings.DEBUG and len(message_raw) < 2000:
                try:
                    # Email per te
                    resend.Emails.send({
                        "from": "Portfolio <info@giuseppemancini.dev>",
                        "to": ["info@giuseppemancini.dev"],
                        "subject": f"New message: {subject}",
                        "reply_to": email,
                        "html": f"<p><strong>From:</strong> {name}</p><p>{message_raw[:2000]}</p>"
                    })
                    
                    # Auto-reply per l'utente
                    resend.Emails.send({
                        "from": "Giuseppe Mancini <info@giuseppemancini.dev>",
                        "to": [email],
                        "subject": f"Receipt: {subject}",
                        "html": f"<p>Hi {name}, I've received your message.</p>"
                    })
                except Exception as email_error:
                    print(f"RESEND ERROR: {email_error}")

            messages.success(request, 'Thank you! Your message has been sent.')
            return redirect('pages:home')
            
        except Exception as e:
            print(f"FORM ERROR: {e}")
            messages.error(request, 'An error occurred.')
            return redirect('pages:home')
    
    # GET request
    featured_case_studies = CaseStudy.objects.filter(is_featured=True).order_by('order')[:3]
    context = {
        'case_studies': featured_case_studies,
        'TURNSTILE_SITE_KEY': settings.TURNSTILE_SITE_KEY  # Passiamo la chiave al template
    }
    return render(request, 'pages/home.html', context)

def projects(request):
	case_studies = CaseStudy.objects.all().order_by('order')
	return render(request, 'pages/projects.html', {'case_studies': case_studies})

# Sezione da migliorare
def about(request):
	return render(request, 'pages/about.html')

def case_study_detail(request, slug):
	case_study = get_object_or_404(CaseStudy, slug=slug)
	return render(request, 'pages/case_detail.html', {'case_study': case_study})
