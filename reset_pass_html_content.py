email_html_content = """
<p>Hello,</p>
<p>You are receiving this email because you requested a password reset for your account.</p>
<p>
    To reset your password
    <a href="{{ reset_pass_url }}">click here</a>.
</p>
<p>
    Alternatively, you may paste the following link in your browser's address bar: <br>
    {{ reset_pass_url }}
</p>
<p>
    The password reset link will expire in 10 minutes, so act fast!
    Thank you!
</p>
"""
