"""Email service for sending emails like password reset links."""
from typing import Optional
from app.core.config import settings


def send_password_reset_email(email: str, reset_token: str, reset_url: Optional[str] = None) -> bool:
    """
    Send a password reset email to the user.
    
    Args:
        email: The recipient's email address
        reset_token: The password reset token
        reset_url: Optional custom reset URL. If not provided, a default format will be used.
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    
    Note:
        This is a placeholder implementation. In production, you should integrate
        with an email service like SendGrid, AWS SES, or SMTP.
        
        To implement actual email sending:
        1. Install an email library (e.g., `fastapi-mail` or `sendgrid`)
        2. Configure SMTP settings in your .env file
        3. Update this function to send actual emails
        
        Example with fastapi-mail:
        ```python
        from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
        
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_TLS=True,
            MAIL_SSL=False,
        )
        
        message = MessageSchema(
            subject="Password Reset Request",
            recipients=[email],
            body=f"Click here to reset your password: {reset_url}",
            subtype="html"
        )
        
        fm = FastMail(conf)
        await fm.send_message(message)
        ```
    """
    # Default reset URL format
    if reset_url is None:
        # In production, replace with your frontend URL
        reset_url = f"http://localhost:8000/reset-password?token={reset_token}"
    
    # TODO: Implement actual email sending
    # For now, we'll just log the reset link (in production, remove this)
    print(f"[EMAIL SERVICE] Password reset link for {email}: {reset_url}")
    print(f"[EMAIL SERVICE] Reset token: {reset_token}")
    
    # In a real implementation, you would:
    # 1. Connect to your email service (SMTP, SendGrid, etc.)
    # 2. Send the email with the reset link
    # 3. Handle errors appropriately
    
    # Return True to indicate "success" for now
    # In production, return the actual result from your email service
    return True

