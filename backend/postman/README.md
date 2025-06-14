# Postman Collection for Defeah Marketing Backend

Complete Postman collection for testing and interacting with the Defeah Marketing Backend API.

## 📁 Collection Contents

- **`Defeah_Marketing_Backend.postman_collection.json`** - Main API collection with all endpoints
- **`Defeah_Marketing_Local.postman_environment.json`** - Local development environment variables
- **`Defeah_Marketing_Production.postman_environment.json`** - Production environment variables
- **`README.md`** - This documentation file

## 🚀 Quick Setup

### 1. Import Collection and Environments

1. **Open Postman**
2. **Import Collection:**
   - Click "Import" button
   - Select `Defeah_Marketing_Backend.postman_collection.json`
   - Collection will appear in your workspace

3. **Import Environments:**
   - Click "Import" button
   - Select both environment files:
     - `Defeah_Marketing_Local.postman_environment.json`
     - `Defeah_Marketing_Production.postman_environment.json`

### 2. Configure Environment Variables

#### Local Development Environment
Select "Defeah Marketing - Local Development" environment and update:

```
base_url: http://localhost:8080
test_email: your-test-email@example.com
test_password: your-secure-password
instagram_client_id: your-instagram-app-client-id
```

#### Production Environment
Select "Defeah Marketing - Production" environment and update:

```
base_url: https://api.defeah.com
test_email: your-production-email@defeah.com
test_password: your-production-password
instagram_client_id: your-production-instagram-client-id
```

### 3. Authentication Workflow

1. **Register User** (if needed)
   - Use "Authentication > Register User" request
   - Modify email and password in request body
   - User ID will be auto-stored in environment

2. **Login**
   - Use "Authentication > Login User" request
   - Access token will be auto-stored and used for subsequent requests

3. **Test Authentication**
   - Use "Authentication > Get Current User" to verify login

## 📋 Collection Structure

### Authentication
- **Register User** - Create new user account
- **Login User** - Authenticate and get JWT token
- **Get Current User** - Get authenticated user info
- **Refresh Token** - Refresh JWT token
- **Logout** - Invalidate token

### Instagram Integration
- **Connect Instagram Account** - OAuth Instagram connection
- **Get Instagram Account Info** - Account details and stats
- **Disconnect Instagram Account** - Remove Instagram connection
- **Get Instagram Insights** - Analytics from Instagram

### Posts
- **Create Post** - Create new content post
- **Get All Posts** - List user's posts with pagination
- **Get Post by ID** - Get specific post details
- **Update Post** - Modify existing post
- **Delete Post** - Remove post (soft delete)
- **Publish Post to Instagram** - Publish to Instagram immediately
- **Get Post Analytics** - Post performance metrics

### Campaigns
- **Create Campaign** - Create marketing campaign
- **Get All Campaigns** - List campaigns with filtering
- **Get Campaign by ID** - Campaign details and metrics
- **Update Campaign** - Modify campaign settings
- **Get Campaign Posts** - Posts in specific campaign
- **Get Campaign Analytics** - Campaign performance data
- **Delete Campaign** - Archive campaign

### AI Content Generation
- **Generate Caption** - AI-powered caption creation
- **Generate Hashtags** - Relevant hashtag suggestions
- **Generate Image** - AI image generation with DALL-E
- **Analyze Content Performance** - Content optimization analysis
- **Get AI Generation History** - AI usage history and costs

### Media Management
- **Upload Media File** - Upload images/videos
- **Get Media Files** - List uploaded media with filtering
- **Get Media File by ID** - Media file details
- **Update Media Metadata** - Modify media information
- **Delete Media File** - Remove media from storage

### Analytics
- **Get User Dashboard** - Comprehensive analytics overview
- **Get Performance Analytics** - Detailed performance metrics
- **Get AI Usage Analytics** - AI usage and cost tracking
- **Get ROI Analytics** - Return on investment data
- **Export Analytics Data** - Export data in various formats

### System
- **Health Check** - API health status
- **API Root** - Root endpoint information
- **API Documentation** - Interactive docs access
- **OpenAPI Schema** - API specification

## 🔧 Environment Variables

### Automatically Populated
These variables are automatically set by test scripts:

- `access_token` - JWT token from login
- `user_id` - Current user ID
- `test_post_id` - Created post ID for testing
- `test_campaign_id` - Created campaign ID for testing
- `test_media_id` - Uploaded media file ID

### Manually Configured
These should be set manually based on your setup:

- `base_url` - API base URL
- `test_email` - Test user email
- `test_password` - Test user password
- `instagram_auth_code` - Instagram OAuth code
- `instagram_client_id` - Instagram app client ID

## 🧪 Testing Features

### Automated Tests
The collection includes automated tests that:

- ✅ Verify response status codes
- ✅ Validate response structure
- ✅ Check security headers
- ✅ Monitor response times
- ✅ Auto-populate environment variables

### Test Scripts Examples

```javascript
// Example test script in "Login User" request
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has access token", function () {
    const response = pm.response.json();
    pm.expect(response).to.have.property('access_token');
});

// Auto-store access token
const response = pm.response.json();
if (response.access_token) {
    pm.environment.set("access_token", response.access_token);
}
```

### Global Test Scripts
Applied to all requests:

- Response time validation (< 2000ms)
- JSON response validation
- Security headers verification
- Request ID and timestamp injection

## 📝 Usage Examples

### Complete Workflow Example

1. **Setup**
   ```
   1. Import collection and environment
   2. Set base_url, test_email, test_password
   3. Start local development server
   ```

2. **Authentication**
   ```
   1. Register User → Creates account
   2. Login User → Gets access token
   3. Get Current User → Verifies authentication
   ```

3. **Instagram Connection**
   ```
   1. Get Instagram OAuth URL from docs
   2. Complete OAuth flow to get auth_code
   3. Connect Instagram Account → Links Instagram
   4. Get Instagram Account Info → Verifies connection
   ```

4. **Content Creation**
   ```
   1. Create Campaign → Sets up marketing campaign
   2. Generate Caption → AI-powered caption
   3. Upload Media File → Upload images
   4. Create Post → Create content post
   5. Publish Post to Instagram → Go live
   ```

5. **Analytics**
   ```
   1. Get Post Analytics → Post performance
   2. Get Campaign Analytics → Campaign metrics
   3. Get User Dashboard → Overall insights
   ```

### Instagram OAuth Setup

To connect Instagram accounts, you need to:

1. **Create Facebook App** with Instagram Basic Display
2. **Configure OAuth redirect URI** in Facebook App settings
3. **Get authorization code** from Instagram OAuth flow:
   ```
   https://www.facebook.com/v18.0/dialog/oauth?
     client_id=YOUR_APP_ID&
     redirect_uri=YOUR_REDIRECT_URI&
     scope=instagram_basic,instagram_content_publish&
     response_type=code
   ```
4. **Use authorization code** in "Connect Instagram Account" request

## 🔍 Troubleshooting

### Common Issues

#### Authentication Errors
```
Error: 401 Unauthorized
Solution: 
1. Check if logged in (use Login User request)
2. Verify access_token in environment
3. Check token expiration (use Refresh Token)
```

#### Environment Variables Not Set
```
Error: Variable not defined
Solution:
1. Ensure correct environment is selected
2. Run authentication requests to populate tokens
3. Manually set required variables
```

#### CORS Issues (Web Postman)
```
Error: CORS policy blocking request
Solution:
1. Use Postman desktop app instead of web
2. Check CORS_ORIGINS configuration in backend
3. Add your domain to allowed origins
```

#### Rate Limiting
```
Error: 429 Too Many Requests
Solution:
1. Wait for rate limit window to reset
2. Check X-RateLimit-* headers for limits
3. Reduce request frequency
```

### Debugging Tips

1. **Check Response Headers**
   - Look for rate limit information
   - Verify security headers
   - Check response time

2. **Use Console Log**
   - Add `console.log(response)` in test scripts
   - Monitor variable values
   - Debug authentication flow

3. **Environment Switching**
   - Test on local environment first
   - Switch to production only after local success
   - Compare environment variables

## 🔐 Security Considerations

### Token Management
- Access tokens are stored as secret variables
- Tokens auto-refresh in test scripts
- Clear tokens when switching environments

### Sensitive Data
- Never commit real credentials to version control
- Use different credentials for each environment
- Regularly rotate API keys and passwords

### Production Testing
- Use dedicated test accounts in production
- Avoid modifying real user data
- Monitor API usage and costs

## 📊 Collection Statistics

- **Total Requests**: 35+
- **Authentication**: 5 endpoints
- **Instagram Integration**: 4 endpoints
- **Posts Management**: 7 endpoints
- **Campaign Management**: 7 endpoints
- **AI Generation**: 5 endpoints
- **Media Management**: 5 endpoints
- **Analytics**: 5 endpoints
- **System**: 4 endpoints

## 🔄 Updates and Maintenance

### Keeping Collection Updated
1. **API Changes**: Update requests when API endpoints change
2. **New Endpoints**: Add new requests to appropriate folders
3. **Environment Variables**: Add new variables as needed
4. **Test Scripts**: Update tests for new response formats

### Version Control
- Export updated collection after changes
- Maintain separate environments for different stages
- Document changes in commit messages

---

**⚠️ LLM Development Disclaimer**: This Postman collection has been generated by AI as part of a comprehensive system design demonstration. While functional and comprehensive, it should be thoroughly tested and adapted for your specific use case and environment setup.

## 📞 Support

For issues with the Postman collection:
1. Check this README for troubleshooting steps
2. Verify your environment setup
3. Test with local development environment first
4. Check backend logs for API errors
5. Refer to API documentation at `/docs` endpoint