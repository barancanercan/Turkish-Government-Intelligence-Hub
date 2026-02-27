"""
Email Service
SendGrid/Resend integration for alerts
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class EmailService:
    """
    Email service for sending alerts.
    """
    
    def __init__(self):
        self.api_key = os.environ.get("SENDGRID_API_KEY") or os.environ.get("RESEND_API_KEY")
        self.from_email = os.environ.get("FROM_EMAIL", "alerts@mizan-ai.com")
        self.from_name = os.environ.get("FROM_NAME", "MIZAN-AI")
        self.provider = "resend" if os.environ.get("RESEND_API_KEY") else "sendgrid"
    
    async def send_email(
        self,
        to: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:
        """
        Send an email.
        
        Args:
            to: Recipient email
            subject: Email subject
            html_content: HTML body
            text_content: Plain text body
            
        Returns:
            True if successful
        """
        if not self.api_key:
            logger.warning("No email API key configured")
            return False
        
        try:
            if self.provider == "resend":
                return await self._send_resend(to, subject, html_content, text_content)
            else:
                return await self._send_sendgrid(to, subject, html_content, text_content)
        except Exception as e:
            logger.error(f"Email send error: {e}")
            return False
    
    async def _send_resend(
        self,
        to: str,
        subject: str,
        html_content: str,
        text_content: Optional[str],
    ) -> bool:
        """Send via Resend."""
        try:
            import resend
            
            resend.api_key = self.api_key
            
            params = {
                "from": f"{self.from_name} <{self.from_email}>",
                "to": [to],
                "subject": subject,
                "html": html_content,
            }
            
            if text_content:
                params["text"] = text_content
            
            resend.Emails.send(params)
            logger.info(f"Email sent to {to}")
            return True
            
        except Exception as e:
            logger.error(f"Resend error: {e}")
            return False
    
    async def _send_sendgrid(
        self,
        to: str,
        subject: str,
        html_content: str,
        text_content: Optional[str],
    ) -> bool:
        """Send via SendGrid."""
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail
            
            message = Mail(
                from_email=self.from_email,
                to_emails=to,
                subject=subject,
                html_content=html_content,
            )
            
            if text_content:
                message.content = [{"type": "text/plain", "value": text_content}]
            
            sg = SendGridAPIClient(self.api_key)
            sg.send(message)
            
            logger.info(f"Email sent to {to}")
            return True
            
        except Exception as e:
            logger.error(f"SendGrid error: {e}")
            return False
    
    async def send_alert_email(
        self,
        to: str,
        alert_type: str,
        title: str,
        content: str,
        link: Optional[str] = None,
    ) -> bool:
        """Send an alert email."""
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #1a1a2e; color: white; padding: 20px; text-align: center;">
                <h1>MIZAN-AI Alert</h1>
            </div>
            <div style="padding: 20px; border: 1px solid #ddd;">
                <h2 style="color: #333;">{title}</h2>
                <p style="color: #666; line-height: 1.6;">{content}</p>
                {f'<p><a href="{link}" style="background: #4a90d9; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Detaylar</a></p>' if link else ''}
            </div>
            <div style="padding: 20px; text-align: center; color: #999; font-size: 12px;">
                <p>Bu email MIZAN-AI alert sistemi tarafından gonderildi.</p>
                <p><a href="{{unsubscribe_url}}">Abonelikten cik</a></p>
            </div>
        </body>
        </html>
        """
        
        text = f"""
        MIZAN-AI Alert
        
        {title}
        
        {content}
        
        {f'Detaylar: {link}' if link else ''}
        
        ---
        Bu email MIZAN-AI alert sistemi tarafından gonderildi.
        """
        
        return await self.send_email(to, f"[MIZAN-AI] {title}", html, text)
    
    async def send_digest_email(
        self,
        to: str,
        alerts: List[Dict[str, Any]],
    ) -> bool:
        """Send a daily digest email."""
        
        alerts_html = ""
        for alert in alerts:
            alerts_html += f"""
            <div style="margin-bottom: 20px; padding: 15px; background: #f5f5f5; border-left: 4px solid #4a90d9;">
                <h3 style="margin: 0 0 10px 0;">{alert.get('title', 'Alert')}</h3>
                <p style="margin: 0;">{alert.get('content', '')}</p>
            </div>
            """
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #1a1a2e; color: white; padding: 20px; text-align: center;">
                <h1>MIZAN-AI Gunluk Ozet</h1>
            </div>
            <div style="padding: 20px;">
                <p>Guncel alarmlar:</p>
                {alerts_html}
            </div>
            <div style="padding: 20px; text-align: center; color: #999; font-size: 12px;">
                <p>Bu email MIZAN-AI alert sistemi tarafından gonderildi.</p>
            </div>
        </body>
        </html>
        """
        
        text = f"""
        MIZAN-AI Gunluk Ozet
        
        {len(alerts)} yeni alert:
        
        {chr(10).join([f"- {a.get('title', '')}: {a.get('content', '')}" for a in alerts])}
        """
        
        return await self.send_email(to, f"[MIZAN-AI] Gunluk Ozet - {len(alerts)} yeni alert", html, text)


email_service = EmailService()
