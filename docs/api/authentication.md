# Authentication Guide

Complete guide for authenticating with the Defeah Marketing Backend API.

## Overview

The Defeah Marketing API uses **JWT (JSON Web Token) Bearer authentication** for securing endpoints. This guide covers authentication flows, token management, and security best practices.

## Authentication Flow

### 1. User Registration

First, register a new user account:

```bash
curl -X POST https://api.defeah.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "full_name": "John Doe"
  }'
```

**Response:**
```json
{
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "instagram_connected": false
  },
  "message": "User registered successfully"
}
```

### 2. User Login

Authenticate with email and password to receive JWT token:

```bash
curl -X POST https://api.defeah.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjNlNDU2Ny1lODliLTEyZDMtYTQ1Ni00MjY2MTQxNzQwMDAiLCJlbWFpbCI6InVzZXJAZXhhbXBsZS5jb20iLCJleHAiOjE2NDI4NjkwMDB9.signature",
  "token_type": "bearer",
  "expires_in": 604800,
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "instagram_connected": false
  }
}
```

### 3. Using the Token

Include the JWT token in the Authorization header for all protected endpoints:

```bash
curl -X GET https://api.defeah.com/api/v1/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Token Structure

### JWT Token Format

The JWT token contains three parts separated by dots (`.`):

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

1. **Header** (Algorithm & Token Type)
2. **Payload** (Claims)
3. **Signature** (Verification)

### Token Payload

```json
{
  "sub": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "exp": 1642869000,
  "iat": 1642262200,
  "jti": "token-unique-id"
}
```

**Claims:**
- `sub` - Subject (user ID)
- `email` - User email address
- `exp` - Expiration timestamp
- `iat` - Issued at timestamp
- `jti` - JWT ID (unique token identifier)

## Token Management

### Token Expiration

- **Default Expiration**: 7 days (604800 seconds)
- **Maximum Expiration**: 30 days
- **Minimum Expiration**: 1 hour

### Token Refresh

Refresh your token before it expires:

```bash
curl -X POST https://api.defeah.com/api/v1/auth/refresh \
  -H "Authorization: Bearer your-current-token"
```

**Response:**
```json
{
  "access_token": "new-jwt-token",
  "token_type": "bearer",
  "expires_in": 604800,
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "instagram_connected": true
  }
}
```

### Token Logout

Logout by invalidating your token:

```bash
curl -X POST https://api.defeah.com/api/v1/auth/logout \
  -H "Authorization: Bearer your-token"
```

**Note**: Token invalidation is primarily client-side. Remove the token from your application storage.

## Instagram OAuth Integration

### OAuth Flow

For Instagram account connection, use the OAuth 2.0 flow:

#### 1. Initiate OAuth

Redirect users to Instagram for authorization:

```
https://www.facebook.com/v18.0/dialog/oauth?
  client_id=YOUR_FACEBOOK_APP_ID&
  redirect_uri=YOUR_REDIRECT_URI&
  scope=instagram_basic,instagram_content_publish,pages_show_list&
  response_type=code&
  state=CSRF_PROTECTION_STRING
```

#### 2. Handle Callback

Instagram redirects back with authorization code:

```
https://yourapp.com/callback?
  code=AUTHORIZATION_CODE&
  state=CSRF_PROTECTION_STRING
```

#### 3. Connect Instagram Account

Exchange the authorization code for access token:

```bash
curl -X POST https://api.defeah.com/api/v1/auth/instagram/connect \
  -H "Authorization: Bearer your-jwt-token" \
  -H "Content-Type: application/json" \
  -d '{
    "auth_code": "AUTHORIZATION_CODE_FROM_INSTAGRAM"
  }'
```

## Security Best Practices

### Token Storage

#### ✅ Secure Storage Options

**Web Applications:**
- HttpOnly cookies (recommended)
- Secure sessionStorage (short-term)
- Encrypted localStorage (with caution)

**Mobile Applications:**
- iOS: Keychain Services
- Android: Android Keystore
- React Native: react-native-keychain

**Server Applications:**
- Environment variables
- Secure configuration files
- Key management services (AWS KMS, Azure Key Vault)

#### ❌ Insecure Storage (Avoid)

- Plain localStorage (XSS vulnerable)
- URL parameters
- Unencrypted cookies
- Client-side JavaScript variables

### Token Transmission

#### ✅ Secure Transmission

```bash
# Good: HTTPS with proper Authorization header
curl -X GET https://api.defeah.com/api/v1/posts \
  -H "Authorization: Bearer your-token"
```

#### ❌ Insecure Transmission (Avoid)

```bash
# Bad: HTTP transmission
curl -X GET http://api.defeah.com/api/v1/posts?token=your-token

# Bad: Token in URL
curl -X GET https://api.defeah.com/api/v1/posts?access_token=your-token
```

### Token Validation

#### Client-Side Validation

```javascript
// Check token expiration before API calls
function isTokenExpired(token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return Date.now() >= payload.exp * 1000;
  } catch (e) {
    return true;
  }
}

// Refresh token if needed
async function makeAuthenticatedRequest(url, options = {}) {
  let token = getStoredToken();
  
  if (isTokenExpired(token)) {
    token = await refreshToken();
  }
  
  return fetch(url, {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      ...options.headers
    }
  });
}
```

#### Server-Side Validation

The API automatically validates tokens on each request:

1. **Signature Verification**: Ensures token hasn't been tampered with
2. **Expiration Check**: Validates token hasn't expired
3. **User Existence**: Confirms user account is still active
4. **Permission Check**: Verifies user has required permissions

## Error Handling

### Authentication Errors

#### 401 Unauthorized - Missing Token

```json
{
  "error": {
    "code": "MISSING_TOKEN",
    "message": "Authentication token required",
    "details": {
      "hint": "Include 'Authorization: Bearer <token>' header"
    }
  }
}
```

#### 401 Unauthorized - Invalid Token

```json
{
  "error": {
    "code": "INVALID_TOKEN",
    "message": "Invalid authentication token",
    "details": {
      "reason": "Token signature verification failed"
    }
  }
}
```

#### 401 Unauthorized - Expired Token

```json
{
  "error": {
    "code": "TOKEN_EXPIRED",
    "message": "Authentication token has expired",
    "details": {
      "expired_at": "2024-01-15T10:30:00Z",
      "hint": "Use refresh endpoint to get new token"
    }
  }
}
```

#### 403 Forbidden - Insufficient Permissions

```json
{
  "error": {
    "code": "INSUFFICIENT_PERMISSIONS",
    "message": "User lacks required permissions",
    "details": {
      "required_permission": "instagram:publish",
      "user_permissions": ["instagram:read"]
    }
  }
}
```

### Error Recovery

```javascript
// Automatic token refresh on 401 errors
async function apiCall(url, options = {}) {
  let response = await fetch(url, {
    ...options,
    headers: {
      'Authorization': `Bearer ${getToken()}`,
      ...options.headers
    }
  });
  
  if (response.status === 401) {
    // Try refreshing token
    try {
      const newToken = await refreshToken();
      response = await fetch(url, {
        ...options,
        headers: {
          'Authorization': `Bearer ${newToken}`,
          ...options.headers
        }
      });
    } catch (refreshError) {
      // Redirect to login
      redirectToLogin();
      return;
    }
  }
  
  return response;
}
```

## Rate Limiting

### Authentication Rate Limits

- **Login**: 10 attempts per 15 minutes per IP
- **Registration**: 5 attempts per hour per IP
- **Token Refresh**: 100 requests per hour per user
- **Password Reset**: 5 requests per hour per email

### Rate Limit Headers

```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
X-RateLimit-Reset: 1642262400
X-RateLimit-RetryAfter: 900
```

### Rate Limit Exceeded Response

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many authentication attempts",
    "details": {
      "limit": 10,
      "window": "15 minutes",
      "retry_after": 900,
      "reset_time": "2024-01-15T10:45:00Z"
    }
  }
}
```

## Code Examples

### JavaScript/Node.js

```javascript
class DefeahAuth {
  constructor(baseURL) {
    this.baseURL = baseURL;
    this.token = localStorage.getItem('defeah_token');
  }
  
  async login(email, password) {
    const response = await fetch(`${this.baseURL}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: email, password })
    });
    
    if (response.ok) {
      const data = await response.json();
      this.token = data.access_token;
      localStorage.setItem('defeah_token', this.token);
      return data;
    }
    
    throw new Error('Login failed');
  }
  
  async apiCall(endpoint, options = {}) {
    return fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json',
        ...options.headers
      }
    });
  }
  
  logout() {
    this.token = null;
    localStorage.removeItem('defeah_token');
  }
}
```

### Python

```python
import requests
import json
from datetime import datetime

class DefeahAuth:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
    
    def login(self, email, password):
        """Authenticate user and store token."""
        response = requests.post(
            f"{self.base_url}/api/v1/auth/login",
            json={"username": email, "password": password}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data["access_token"]
            return data
        
        raise Exception(f"Login failed: {response.text}")
    
    def api_call(self, method, endpoint, **kwargs):
        """Make authenticated API call."""
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f"Bearer {self.token}"
        kwargs['headers'] = headers
        
        return requests.request(
            method,
            f"{self.base_url}{endpoint}",
            **kwargs
        )
    
    def logout(self):
        """Clear stored token."""
        if self.token:
            self.api_call('POST', '/api/v1/auth/logout')
        self.token = None
```

### PHP

```php
<?php

class DefeahAuth {
    private $baseUrl;
    private $token;
    
    public function __construct($baseUrl) {
        $this->baseUrl = $baseUrl;
    }
    
    public function login($email, $password) {
        $response = $this->httpRequest('POST', '/api/v1/auth/login', [
            'username' => $email,
            'password' => $password
        ]);
        
        if ($response['status_code'] === 200) {
            $data = json_decode($response['body'], true);
            $this->token = $data['access_token'];
            return $data;
        }
        
        throw new Exception('Login failed: ' . $response['body']);
    }
    
    public function apiCall($method, $endpoint, $data = null) {
        $headers = ['Authorization: Bearer ' . $this->token];
        return $this->httpRequest($method, $endpoint, $data, $headers);
    }
    
    private function httpRequest($method, $endpoint, $data = null, $headers = []) {
        $ch = curl_init();
        
        curl_setopt_array($ch, [
            CURLOPT_URL => $this->baseUrl . $endpoint,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_CUSTOMREQUEST => $method,
            CURLOPT_HTTPHEADER => array_merge([
                'Content-Type: application/json'
            ], $headers),
            CURLOPT_POSTFIELDS => $data ? json_encode($data) : null
        ]);
        
        $response = curl_exec($ch);
        $statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        return [
            'status_code' => $statusCode,
            'body' => $response
        ];
    }
}
?>
```

## Testing Authentication

### Unit Testing

```python
import unittest
from unittest.mock import patch
import jwt
from datetime import datetime, timedelta

class TestAuthentication(unittest.TestCase):
    
    def setUp(self):
        self.secret_key = "test-secret-key"
        self.user_id = "123e4567-e89b-12d3-a456-426614174000"
    
    def test_token_generation(self):
        """Test JWT token generation."""
        payload = {
            'sub': self.user_id,
            'email': 'test@example.com',
            'exp': datetime.utcnow() + timedelta(days=7),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        decoded = jwt.decode(token, self.secret_key, algorithms=['HS256'])
        
        self.assertEqual(decoded['sub'], self.user_id)
        self.assertEqual(decoded['email'], 'test@example.com')
    
    def test_token_expiration(self):
        """Test expired token handling."""
        payload = {
            'sub': self.user_id,
            'exp': datetime.utcnow() - timedelta(hours=1)  # Expired
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        
        with self.assertRaises(jwt.ExpiredSignatureError):
            jwt.decode(token, self.secret_key, algorithms=['HS256'])
```

### Integration Testing

```bash
#!/bin/bash

# Test authentication flow
BASE_URL="http://localhost:8080"

# Register user
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "full_name": "Test User"
  }')

echo "Registration: $REGISTER_RESPONSE"

# Login user
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test@example.com",
    "password": "testpassword123"
  }')

TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')
echo "Login successful, token: ${TOKEN:0:20}..."

# Test authenticated endpoint
USER_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN")

echo "User profile: $USER_RESPONSE"

# Test token refresh
REFRESH_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/refresh" \
  -H "Authorization: Bearer $TOKEN")

echo "Token refresh: $REFRESH_RESPONSE"
```

## Troubleshooting

### Common Issues

1. **Token Not Working**
   - Check token format and presence of `Bearer` prefix
   - Verify token hasn't expired
   - Ensure token was generated by the correct environment

2. **CORS Issues**
   - Verify Origin header matches allowed origins
   - Check preflight request handling
   - Ensure credentials are included in requests

3. **Rate Limiting**
   - Implement exponential backoff
   - Cache authentication tokens
   - Monitor rate limit headers

4. **Instagram OAuth Failures**
   - Verify Facebook App configuration
   - Check redirect URI matches exactly
   - Ensure required scopes are requested

### Debug Tools

#### Token Decoder

Use [jwt.io](https://jwt.io) to decode and inspect JWT tokens.

#### API Testing

```bash
# Test with curl
curl -X GET https://api.defeah.com/api/v1/auth/me \
  -H "Authorization: Bearer your-token" \
  -v

# Test with httpie
http GET https://api.defeah.com/api/v1/auth/me \
  Authorization:"Bearer your-token"
```

#### Log Analysis

Check application logs for authentication errors:
- Invalid token signatures
- Expired tokens
- Missing permissions
- Rate limit violations

For additional support, contact our developer support team or check our status page for known authentication issues.