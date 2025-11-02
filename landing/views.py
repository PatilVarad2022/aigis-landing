from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .forms import SignupForm
from .models import UserProfile

def index(request):
    # Storytelling context for the landing page (hero, problem, solution, transformation, founder)
    # Hero punch line (kept concise for conversion testing)
    hero = {
        # include a <br> so the template can render the two-line punch
        "headline": "91% of traders lose money.<br>Not anymore.",
        "lede": "Shield first. You set your Principal Loss Shield; the AI enforces it. Stop trading on fear. Start investing with AI accountability. 28‑day free trial.",
        "cta": "Start your 28‑day AI trial — No card required"
    }

    problem = {
        "title": "You know you shouldn't trade like this. But you do anyway.",
        "body": (
            "Emotion, FOMO (Fear of Missing Out), and a flashing screen beat logic. The tools are fast, your brain isn't. "
            "This is what 91% of traders face when they lose money. You trade impulsively, doubling down on losses (revenge trading), "
            "or buying momentum stocks at their peak. Zerodha built a system of zero-friction execution for this emotion-driven market, but it abandoned the safety net. "
            "Aigis changes the rules. You set one line in the sand—your Principal Loss Shield—and our Agent enforces it with machine discipline "
            "and tells you why every move happens. Less fear. More accountability."
        )
    }

    solution = {
        "title": "Here's what happens after you click \u201cStart Free Trial\u201d",
        "steps": [
            {"time": "Step 1 (30s)", "text": "Enter email and create password. You'll create your basic secure login and agree to the terms, establishing your account with Aigis."},
            {"time": "Step 2 (2 min)", "text": "Answer 5 questions (goal, risk, experience, capital). This is where you set your Mandate. You define your desired risk profile, target capital amount, and crucially, set your Principal Loss Shield percentage (e.g., 10%)."},
            {"time": "Step 3 (Instant)", "text": "Aigis builds your profile and shows your first insights. The AI immediately synthesizes your risk mandate and current market data, presenting you with a personalized dashboard and the core rationale behind its initial investment strategy. You receive immediate, tangible value."},
            {"time": "Day 28", "text": "We'll email you to continue to enjoy the benefits of AI-guided management and transparent XAI for \u20b9149/month, or export your learnings and portfolio data. You will have a full month of demonstrated, protective performance to base your subscription decision on."}
        ],
        "price": "\u20b9149/month"
    }

    # Problem / Mandate / Outcome block (kept in context for templates or future use)
    pmo = {
        "problem": (
            "Tools without protection. The current market setup encourages and monetizes emotional trading, where fees compound losses. "
            "This results in the statistical catastrophe of 91% of retail traders losing money — a direct failure of the system to prioritize safety."
        ),
        "mandate": (
            "You set a 5–20% loss shield. Our Agentic AI then takes a clear mandate to manage your portfolio toward your specific financial goals, "
            "respecting the hard limit you set on capital loss. This mandate-bound authority is what enables the AI to act decisively on your behalf, removing emotional conflict."
        ),
        "outcome": (
            "Disciplined execution. You gain a protective partner that eliminates speculative, emotion-driven mistakes. All actions are justified by Plain-English XAI. "
            "Your compounding growth is protected, and your long-term wealth goal is the only priority."
        )
    }

    transformation = {
        "before": {"period": "2 months", "trades": 47, "result": "−23%"},
        "after": {"period": "4 months", "trades": 18, "result": "+24%"},
        "quote": "The AI is like having my smartest friend watch over my shoulder. — Arjun K."
    }

    brand_promise = {
        "tagline": "AIGIS: The Accountable AI-First Fiduciary",
        "intro": "Aigis is an AI-Native Investment Agent engineered to correct the fundamental flaw in modern retail finance: the gap between market access and safe, profitable outcomes.",
        "pillars": {
            "autonomous": {
                "title": "AI-Guided Management (Product)",
                "description": "Aigis uses Agentic AI to guide goal-based portfolio management, focusing on disciplined execution and eliminating human emotional bias. Its primary directive is the Principal Loss Shield, a dynamic defense mechanism that acts immediately to prevent a client's capital loss from exceeding a pre-set limit."
            },
            "accountable": {
                "title": "Accountable Transparency (Design)",
                "description": "We overcome the industry's massive trust barrier by embedding Explainable AI (XAI) directly into the user experience. The XAI provides a plain-language audit trail, narrating the exact reasoning for every trade. This transparency creates a secure, accountable defense mechanism that Zerodha's anti-advice culture cannot match."
            }
        },
        "promise": "We are not high-fee financial advisors; we are builders committed to providing a secure, transparent defense mechanism that helps every disciplined trader succeed through systems and clarity. Our business model is focused on monetizing safety and accountability via a freemium/subscription model, not on profiting from the volume of trades or the 91% loss rate of the retail market.",
        "signature": "— The Aigis Founding Team"
    }
    

    # Keep Arjun's mini-story in one place for maximum hook impact
    arjun = {
        "title": "Meet Arjun — A 4-Minute Mistake",
        "paras": [
            "It was 3:42 PM. Market closing in 18 minutes. Arjun had been watching a stock all day and convinced himself he couldn't miss the move. Emotion and FOMO took over.",
            "At 3:58 PM, he quickly clicked BUY—a ₹1,40,000 position. The stock had dropped 3% and he was instantly down ₹25,000. Hands shaking, he stared at the screen. Should he sell? Hold? Average down? The market closed, and his stomach dropped.",
            "That night he searched: \"How to stop emotional trading.\" If he had Aigis, an AI Alert would have flagged FOMO, locked the trade for 10 minutes, and asked him to write down why he was buying. He would've paused—and likely saved ₹25,000."
        ]
    }

    # What if walkthrough - sequential logic flow
    whatif = {
        "title": "What if — a quick walkthrough",
        "subtitle": "What if Arjun had Aigis that day?",
        "steps": [
            {
                "time": "3:42 PM — AI Detects FOMO",
                "text": "The AI detects the high-risk behavioral pattern (rapid searching, oversized trade attempt). It locks the trade for 10 minutes and sends a prompt: \"Stop emotional trading.\""
            },
            {
                "time": "3:52 PM — Reflection",
                "text": "Arjun is prompted to write down his motive. He reviews his strategy and realizes it's just momentum chasing. He cancels the trade."
            },
            {
                "time": "Next Day — Capital Preserved",
                "text": "Reliance drops 4% the next day, confirming the AI's risk assessment. Aigis saved him ₹25,000 in capital loss."
            }
        ]
    }

    context = {
        "hero": hero,
        "problem": problem,
        "solution": solution,
        "transformation": transformation,
        "brand_promise": brand_promise,
        "arjun": arjun,
        "whatif": whatif,
        "pmo": pmo,
    }
    return render(request, "landing/index.html", context)


def signup(request):
    try:
        if request.method == "POST":
            form = SignupForm(request.POST)
            if form.is_valid():
                user = None
                try:
                    email = form.cleaned_data["email"].lower()
                    password = form.cleaned_data["password"]
                    full_name = form.cleaned_data["full_name"]
                    phone = form.cleaned_data["phone"]
                    shield = form.cleaned_data["shield_limit_percent"]

                    # Use transaction with timeout handling
                    with transaction.atomic():
                        # Check if user already exists (this will wake up Neon if sleeping)
                        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
                            form.add_error('email', 'An account with this email already exists. Please use a different email or try logging in.')
                            return render(request, "landing/signup.html", {"form": form})

                        user = User.objects.create_user(username=email, email=email, password=password)
                        UserProfile.objects.create(user=user, full_name=full_name, phone=phone, shield_limit_percent=shield)
                except Exception as db_error:
                    # Catch database constraint errors (duplicate username/email)
                    error_msg = str(db_error)
                    if 'duplicate key' in error_msg.lower() or 'already exists' in error_msg.lower() or 'unique constraint' in error_msg.lower():
                        form.add_error('email', 'An account with this email already exists. Please use a different email or try logging in.')
                        return render(request, "landing/signup.html", {"form": form})
                    else:
                        # Re-raise other database errors to be caught by outer exception handler
                        raise

                # If user creation failed, don't proceed
                if not user:
                    form.add_error(None, 'Failed to create account. Please try again.')
                    return render(request, "landing/signup.html", {"form": form})

                messages.success(request, "Your 28-day trial is active!")
                return redirect("signup_success")
            else:
                # Form is invalid, render with errors
                return render(request, "landing/signup.html", {"form": form})
        else:
            form = SignupForm()
            return render(request, "landing/signup.html", {"form": form})
    except Exception as e:
        # Log the error for debugging
        import logging
        import traceback
        logger = logging.getLogger(__name__)
        logger.error(f"Error in signup view: {e}", exc_info=True)
        
        # Check if it's a database connection error
        error_msg = str(e).lower()
        if 'connection' in error_msg or 'timeout' in error_msg or 'operationalerror' in error_msg:
            # Database connection issue - return user-friendly error page
            messages.error(request, "Database connection timeout. Please try again in a few seconds.")
            form = SignupForm()
            return render(request, "landing/signup.html", {"form": form})
        
        # For other errors, return error page without 500 status (to prevent 502)
        messages.error(request, "An error occurred during signup. Please try again or contact support.")
        form = SignupForm()
        return render(request, "landing/signup.html", {"form": form})


def signup_success(request):
    return render(request, "landing/success.html")


def process_emails(request):
    """API endpoint to process pending emails - called by JavaScript timer"""
    from django.http import JsonResponse
    from landing.models import PendingEmail
    from django.utils import timezone
    from datetime import timedelta
    
    try:
        # Process emails older than 2 minutes (prevents race conditions)
        cutoff_time = timezone.now() - timedelta(minutes=2)
        pending_emails = PendingEmail.objects.filter(
            sent=False,
            created_at__lte=cutoff_time
        ).order_by('created_at')[:10]  # Process max 10 at a time
        
        sent_count = 0
        failed_count = 0
        
        for pending_email in pending_emails:
            try:
                email_data = pending_email.email_data
                
                if pending_email.email_type == 'welcome':
                    # Send welcome email to user
                    msg = EmailMultiAlternatives(
                        subject=email_data['subject'],
                        body=email_data['text_content'],
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[email_data['to']],
                    )
                    msg.attach_alternative(email_data['html_content'], "text/html")
                    msg.send(fail_silently=True)
                    
                elif pending_email.email_type == 'admin_notification':
                    # Send admin notification
                    send_mail(
                        subject=email_data['subject'],
                        message=email_data['message'],
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email_data['to']],
                        fail_silently=True,
                    )
                
                # Mark as sent
                pending_email.sent = True
                pending_email.sent_at = timezone.now()
                pending_email.save()
                sent_count += 1
                
            except Exception:
                # If email fails, don't break - will retry later
                pending_email.attempts += 1
                pending_email.save()
                failed_count += 1
                pass
        
        return JsonResponse({
            'success': True,
            'processed': sent_count + failed_count,
            'sent': sent_count,
            'failed': failed_count
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def privacy(request):
    return render(request, "landing/privacy.html")


def terms(request):
    return render(request, "landing/terms.html")
