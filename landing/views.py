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

                # Prepare email content (will be sent in background thread)
                html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Aigis</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; line-height: 1.6;">
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f8fafc; padding: 40px 0;">
        <tr>
            <td align="center">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="background-color: #ffffff; border-radius: 16px; box-shadow: 0 4px 20px rgba(15, 23, 42, 0.1); overflow: hidden;">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #0067FF 0%, #00FF8C 100%); padding: 40px 40px 50px; text-align: center;">
                            <div style="font-size: 36px; font-weight: bold; color: #ffffff; margin-bottom: 12px;">🛡️</div>
                            <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 700; letter-spacing: -0.5px;">Welcome to Aigis!</h1>
                            <p style="margin: 12px 0 0; color: rgba(255, 255, 255, 0.95); font-size: 16px;">Your AI Trading Partner is Ready</p>
                        </td>
                    </tr>
                    
                    <!-- Main Content -->
                    <tr>
                        <td style="padding: 40px;">
                            <p style="margin: 0 0 24px; color: #0f172a; font-size: 18px; font-weight: 600;">Hi {full_name},</p>
                            
                            <p style="margin: 0 0 24px; color: #475569; font-size: 16px;">
                                Welcome to Aigis! We're <strong style="color: #0067FF;">thrilled</strong> to have you join us. You've just taken the first step toward trading with discipline, protection, and AI-powered accountability.
                            </p>
                            
                            <!-- Trial Active Banner -->
                            <div style="background: linear-gradient(135deg, rgba(0, 255, 140, 0.1) 0%, rgba(0, 103, 255, 0.1) 100%); border-left: 4px solid #00FF8C; padding: 20px; border-radius: 8px; margin: 32px 0;">
                                <p style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 700; margin-bottom: 8px;">🎉 Your 28-Day Free Trial is Now Active</p>
                                <p style="margin: 0; color: #64748b; font-size: 15px;">You're all set and ready to go!</p>
                            </div>
                            
                            <!-- Configuration Details -->
                            <div style="background-color: #f1f5f9; border-radius: 12px; padding: 24px; margin: 32px 0;">
                                <p style="margin: 0 0 16px; color: #0f172a; font-size: 17px; font-weight: 600;">Here's what we've configured for you:</p>
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                    <tr>
                                        <td style="padding: 8px 0;">
                                            <span style="color: #00FF8C; font-size: 20px; margin-right: 8px;">✓</span>
                                            <span style="color: #475569; font-size: 15px;"><strong style="color: #0f172a;">Loss Shield:</strong> {shield}% (Your capital protection is active)</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0;">
                                            <span style="color: #00FF8C; font-size: 20px; margin-right: 8px;">✓</span>
                                            <span style="color: #475569; font-size: 15px;"><strong style="color: #0f172a;">Account:</strong> {email}</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0;">
                                            <span style="color: #00FF8C; font-size: 20px; margin-right: 8px;">✓</span>
                                            <span style="color: #475569; font-size: 15px;"><strong style="color: #0f172a;">Full Access:</strong> All features unlocked for your trial</span>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                            
                            <!-- What You Get -->
                            <div style="margin: 32px 0;">
                                <h2 style="margin: 0 0 20px; color: #0f172a; font-size: 22px; font-weight: 700;">What happens next?</h2>
                                <p style="margin: 0 0 16px; color: #475569; font-size: 16px;">
                                    You now have an AI partner that:
                                </p>
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: 16px 0;">
                                    <tr>
                                        <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                            <span style="color: #0067FF; font-size: 18px; margin-right: 12px;">🛡️</span>
                                            <span style="color: #475569; font-size: 15px;">Protects your capital with your <strong style="color: #0f172a;">{shield}% Loss Shield</strong></span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                            <span style="color: #0067FF; font-size: 18px; margin-right: 12px;">📊</span>
                                            <span style="color: #475569; font-size: 15px;">Explains every decision in <strong style="color: #0f172a;">plain English</strong> (XAI transparency)</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                            <span style="color: #0067FF; font-size: 18px; margin-right: 12px;">🧠</span>
                                            <span style="color: #475569; font-size: 15px;">Helps you avoid <strong style="color: #0f172a;">emotional trading mistakes</strong></span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 12px 0;">
                                            <span style="color: #0067FF; font-size: 18px; margin-right: 12px;">⏰</span>
                                            <span style="color: #475569; font-size: 15px;">Works <strong style="color: #0f172a;">24/7</strong> to monitor and manage risk</span>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                            
                            <!-- Next Steps -->
                            <div style="background-color: #f8fafc; border-radius: 12px; padding: 24px; margin: 32px 0; border: 1px solid #e2e8f0;">
                                <h2 style="margin: 0 0 16px; color: #0f172a; font-size: 20px; font-weight: 700;">Next Steps:</h2>
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                    <tr>
                                        <td style="padding: 8px 0;">
                                            <span style="display: inline-block; width: 28px; height: 28px; background: linear-gradient(135deg, #0067FF, #00FF8C); border-radius: 50%; text-align: center; line-height: 28px; color: #ffffff; font-weight: bold; font-size: 14px; margin-right: 12px;">1</span>
                                            <span style="color: #475569; font-size: 15px;">Log in to your dashboard (coming soon)</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0;">
                                            <span style="display: inline-block; width: 28px; height: 28px; background: linear-gradient(135deg, #0067FF, #00FF8C); border-radius: 50%; text-align: center; line-height: 28px; color: #ffffff; font-weight: bold; font-size: 14px; margin-right: 12px;">2</span>
                                            <span style="color: #475569; font-size: 15px;">Connect your trading account when ready</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0;">
                                            <span style="display: inline-block; width: 28px; height: 28px; background: linear-gradient(135deg, #0067FF, #00FF8C); border-radius: 50%; text-align: center; line-height: 28px; color: #ffffff; font-weight: bold; font-size: 14px; margin-right: 12px;">3</span>
                                            <span style="color: #475569; font-size: 15px;">Set your investment goals</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0;">
                                            <span style="display: inline-block; width: 28px; height: 28px; background: linear-gradient(135deg, #0067FF, #00FF8C); border-radius: 50%; text-align: center; line-height: 28px; color: #ffffff; font-weight: bold; font-size: 14px; margin-right: 12px;">4</span>
                                            <span style="color: #475569; font-size: 15px;">Let Aigis start protecting your capital</span>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                            
                            <!-- Personal Message -->
                            <div style="border-left: 3px solid #0067FF; padding-left: 20px; margin: 32px 0;">
                                <p style="margin: 0 0 12px; color: #475569; font-size: 16px; font-style: italic;">
                                    We built Aigis because we know how it feels to lose money to emotional trading. <strong style="color: #0f172a; font-style: normal;">We've been there.</strong> That's why every feature is designed to give you discipline, transparency, and peace of mind.
                                </p>
                                <p style="margin: 0; color: #0f172a; font-size: 17px; font-weight: 600;">
                                    You're not just getting software—you're getting a system that fights for your financial goals.
                                </p>
                            </div>
                            
                            <!-- CTA -->
                            <div style="text-align: center; margin: 40px 0;">
                                <p style="margin: 0 0 24px; color: #0f172a; font-size: 18px; font-weight: 600;">Ready to trade smarter? Let's do this together.</p>
                            </div>
                            
                            <!-- Footer -->
                            <div style="border-top: 1px solid #e2e8f0; padding-top: 24px; margin-top: 32px;">
                                <p style="margin: 0 0 8px; color: #64748b; font-size: 14px;">
                                    Questions? Just reply to this email. We're here to help.
                                </p>
                                <p style="margin: 16px 0 0; color: #0f172a; font-size: 16px; font-weight: 600;">
                                    Welcome aboard!<br>
                                    <span style="color: #64748b; font-weight: 400; font-size: 14px;">— The Aigis Team</span>
                                </p>
                                
                                <!-- P.S. Note -->
                                <div style="background-color: #fef3c7; border-left: 3px solid #f59e0b; padding: 16px; border-radius: 8px; margin-top: 24px;">
                                    <p style="margin: 0; color: #92400e; font-size: 14px; line-height: 1.6;">
                                        <strong>P.S.</strong> Remember: Your trial is completely free, no credit card required. If you love it after 28 days, it's just <strong>₹149/month</strong>. If not, export your data and walk away—no questions asked.
                                    </p>
                                </div>
                            </div>
                        </td>
                    </tr>
                    
                    <!-- Bottom Spacer -->
                    <tr>
                        <td style="background-color: #f8fafc; padding: 20px; text-align: center;">
                            <p style="margin: 0; color: #94a3b8; font-size: 12px;">
                                © 2025 Aigis. All rights reserved.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
'''
                
                # Plain text version for email clients that don't support HTML
                text_content = f'''Hi {full_name},

Welcome to Aigis! We're thrilled to have you join us. You've just taken the first step toward trading with discipline, protection, and AI-powered accountability.

🎉 Your 28-Day Free Trial is Now Active

Here's what we've configured for you:
✅ Loss Shield: {shield}% (Your capital protection is active)
✅ Account: {email}
✅ Full Access: All features unlocked for your trial

What happens next?

You now have an AI partner that:
• Protects your capital with your {shield}% Loss Shield
• Explains every decision in plain English (XAI transparency)
• Helps you avoid emotional trading mistakes
• Works 24/7 to monitor and manage risk

Next Steps:
1. Log in to your dashboard (coming soon)
2. Connect your trading account when ready
3. Set your investment goals
4. Let Aigis start protecting your capital

We built Aigis because we know how it feels to lose money to emotional trading. We've been there. That's why every feature is designed to give you discipline, transparency, and peace of mind.

You're not just getting software—you're getting a system that fights for your financial goals.

Ready to trade smarter? Let's do this together.

Questions? Just reply to this email. We're here to help.

Welcome aboard!
— The Aigis Team

P.S. Remember: Your trial is completely free, no credit card required. If you love it after 28 days, it's just ₹149/month. If not, export your data and walk away—no questions asked.'''

                # Emails disabled during signup to prevent 502 errors
                # Emails can be sent later via scheduled job or management command
                # This ensures signup completes immediately without timeouts
                print(f"[AIGIS] User {email} signed up successfully. Emails will be sent later.")
                
                messages.success(request, "Your 28-day trial is active! Welcome to Aigis.")
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


def privacy(request):
    return render(request, "landing/privacy.html")


def terms(request):
    return render(request, "landing/terms.html")
