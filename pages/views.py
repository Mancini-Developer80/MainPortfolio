import os
import resend
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import ContactSubmission, CaseStudy

# Configura l'API Key (assicurati che sia impostata su Render)
resend.api_key = os.environ.get('RESEND_API_KEY')

def home(request):
    if request.method == 'POST':
        # 1. HONEYPOT CHECK - Se il campo è compilato, è un bot.
        # Restituiamo un redirect silenzioso senza dare errori (per non "istruire" il bot)
        if request.POST.get('hp_field'):
            return redirect('pages:home')

        # Get form data
        subject = request.POST.get('subject', '').strip()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Validate required fields
        if not all([subject, name, email, message]):
            messages.error(request, 'All fields are required.')
            return redirect('pages:home')
        
        try:
            # 2. Salva nel database
            # Ricorda: devi avere eseguito le migrazioni con max_length=255!
            submission = ContactSubmission.objects.create(
                subject=subject,
                name=name,
                email=email,
                message=message
            )
            
            # 3. Invio email (Resend) - Solo in produzione
            if not settings.DEBUG:
                try:
                    # Email per te
                    resend.Emails.send({
                        "from": "Portfolio <info@giuseppemancini.dev>",
                        "to": ["info@giuseppemancini.dev"],
                        "subject": f"Nuovo messaggio da {name}: {subject}",
                        "reply_to": email,
                        "html": f"""
                            <p><strong>Da:</strong> {name} ({email})</p>
                            <p><strong>Oggetto:</strong> {subject}</p>
                            <p><strong>Messaggio:</strong></p>
                            <p>{message}</p>
                            <hr>
                            <p>Ricevuto il: {submission.submitted_at.strftime('%d/%m/%Y %H:%M')}</p>
                        """
                    })
                    
                    # Auto-reply per l'utente
                    resend.Emails.send({
                        "from": "Giuseppe Mancini <info@giuseppemancini.dev>",
                        "to": [email],
                        "subject": f"Thank you for reaching out - {subject}",
                        "html": f"""
                            <p>Hi {name},</p>
                            <p>Thank you for contacting me. I have received your message and I will get back to you as soon as possible.</p>
                            <p><strong>Your message:</strong><br>"{message}"</p>
                            <br>
                            <p>Best regards,<br>Giuseppe Mancini<br>Full Stack Web Developer</p>
                        """
                    })
                except Exception as email_error:
                    print(f"RESEND ERROR: {email_error}")

            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('pages:home')
            
        except Exception as e:
            # Qui è dove PostgreSQL lanciava l'errore "value too long"
            print(f"FORM ERROR: {e}")
            messages.error(request, 'An error occurred. Please try again later.')
            return redirect('pages:home')
    
    # GET request
    featured_case_studies = CaseStudy.objects.filter(is_featured=True).order_by('order')[:3]
    return render(request, 'pages/home.html', {'case_studies': featured_case_studies})

def projects(request):
	case_studies = CaseStudy.objects.all().order_by('order')
	return render(request, 'pages/projects.html', {'case_studies': case_studies})

# Sezione da migliorare
def about(request):
	return render(request, 'pages/about.html')

def case_study_detail(request, slug):
	case_study = get_object_or_404(CaseStudy, slug=slug)
	return render(request, 'pages/case_detail.html', {'case_study': case_study})
