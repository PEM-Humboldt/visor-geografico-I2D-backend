# Security Documentation - Visor I2D Backend

## Overview

This document outlines the comprehensive security measures implemented in the Visor I2D backend system to protect against common web vulnerabilities and ensure data integrity.

## Security Architecture

### 1. Authentication & Authorization

#### Password Security
- **Minimum Length**: 12 characters
- **Complexity Requirements**: Uppercase, lowercase, digits, special characters
- **Pattern Validation**: Blocks common patterns (123, abc, password, etc.)
- **Custom Validator**: `CustomPasswordValidator` in `applications.common.validators`

#### Session Management
- **Secure Cookies**: `SESSION_COOKIE_SECURE = True` (HTTPS only)
- **HttpOnly Cookies**: Prevents XSS access to session cookies
- **SameSite Protection**: `SESSION_COOKIE_SAMESITE = 'Lax'`
- **Session Timeout**: 1 hour default (`SESSION_COOKIE_AGE = 3600`)

### 2. Input Validation & Sanitization

#### Comprehensive Validators
- **Department Codes**: Colombian department validation (05, 08, 11, etc.)
- **Municipality Codes**: 5-digit codes with department validation
- **Biodiversity Data**: Species names, coordinates, date formats
- **GBIF Data**: Scientific nomenclature, geographic bounds
- **User Input**: Email, institution names, observations

#### XSS Prevention
- **HTML Escaping**: Automatic escaping of user input
- **Pattern Filtering**: Removes dangerous patterns (script tags, javascript:, etc.)
- **Input Sanitization**: `sanitize_input()` function for all user data
- **Length Limits**: Configurable maximum lengths for all inputs

### 3. Security Headers

#### Content Security Policy (CSP)
```
default-src 'self';
script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
font-src 'self' https://fonts.gstatic.com;
img-src 'self' data: https:;
connect-src 'self' https://api.gbif.org;
frame-ancestors 'none';
```

#### Security Headers Implementation
- **X-Frame-Options**: `DENY` (prevents clickjacking)
- **X-Content-Type-Options**: `nosniff` (prevents MIME sniffing)
- **X-XSS-Protection**: `1; mode=block` (enables XSS filtering)
- **Referrer-Policy**: `strict-origin-when-cross-origin`
- **Permissions-Policy**: Restricts geolocation, microphone, camera access

### 4. API Security

#### Rate Limiting
- **Anonymous Users**: 100 requests/hour
- **Authenticated Users**: 1000 requests/hour
- **Configurable Rates**: Environment variable controlled

#### Authentication Methods
- **Session Authentication**: For web interface
- **Token Authentication**: For API access
- **Permission Classes**: `IsAuthenticatedOrReadOnly` default

### 5. Monitoring & Logging

#### Security Logging
- **Log Location**: `/var/log/django/security.log`
- **Suspicious Activity Detection**: SQL injection, XSS, command injection attempts
- **Request Logging**: Comprehensive request/response logging

## Security Configuration

### Environment Variables
```bash
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
API_ANON_RATE=100/hour
API_USER_RATE=1000/hour
```

## Security Checklist

- [x] Password complexity validation
- [x] Session security configuration
- [x] Input validation and sanitization
- [x] Security headers implementation
- [x] Rate limiting configuration
- [x] HTTPS enforcement
- [x] XSS protection
- [x] CSRF protection
- [x] SQL injection prevention
- [x] Security logging and monitoring