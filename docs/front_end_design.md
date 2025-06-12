# Defeah Marketing Dashboard - Frontend App Development Guide

## Table of Contents
1. [Project Overview](#project-overview)
2. [Tech Stack & Architecture](#tech-stack--architecture)
3. [Application Structure](#application-structure)
4. [User Flows & Features](#user-flows--features)
5. [Component Hierarchy](#component-hierarchy)
6. [State Management](#state-management)
7. [API Integration](#api-integration)
8. [Authentication Flow](#authentication-flow)
9. [Real-time Features](#real-time-features)
10. [UI/UX Guidelines](#uiux-guidelines)
11. [Performance Optimization](#performance-optimization)
12. [Error Handling](#error-handling)
13. [Testing Strategy](#testing-strategy)
14. [Deployment](#deployment)

## Project Overview

### Application Purpose
A comprehensive Instagram marketing dashboard for Defeah home decor brand that enables autonomous content creation, scheduling, publishing, and performance analytics.

### Core Functionality
- **Content Management**: Create, edit, schedule, and publish Instagram posts
- **AI Content Generation**: Generate captions, images, and hashtags using AI
- **Campaign Management**: Create and monitor marketing campaigns
- **Analytics Dashboard**: Track performance metrics and insights
- **User Management**: Profile settings and Instagram account connection

### Target Users
- Marketing managers
- Content creators
- Social media specialists
- Brand managers

## Tech Stack & Architecture

### Recommended Frontend Stack
```
Framework: React 18+ with TypeScript
Build Tool: Vite
UI Library: Material-UI (MUI) or Tailwind CSS + Headless UI
State Management: Redux Toolkit + RTK Query
Routing: React Router v6
Form Handling: React Hook Form + Zod validation
Charts: Recharts or Chart.js
Date Handling: date-fns
HTTP Client: RTK Query (built on fetch)
WebSocket: Native WebSocket API
Icons: Lucide React or Heroicons
Testing: Vitest + React Testing Library
```

### Architecture Pattern
```
┌─────────────────────────────────────────┐
│               Presentation Layer         │
│  (React Components + UI Libraries)      │
├─────────────────────────────────────────┤
│               State Layer               │
│     (Redux Store + RTK Query)          │
├─────────────────────────────────────────┤
│              Service Layer              │
│     (API Client + WebSocket)           │
├─────────────────────────────────────────┤
│               Data Layer                │
│     (Local Storage + Cache)            │
└─────────────────────────────────────────┘
```

## Application Structure

### Directory Structure
```
src/
├── components/          # Reusable UI components
│   ├── ui/             # Basic UI components (Button, Input, etc.)
│   ├── forms/          # Form components
│   ├── charts/         # Chart components
│   └── layout/         # Layout components
├── pages/              # Page-level components
│   ├── auth/           # Authentication pages
│   ├── dashboard/      # Dashboard pages
│   ├── posts/          # Post management pages
│   ├── campaigns/      # Campaign pages
│   ├── analytics/      # Analytics pages
│   └── settings/       # Settings pages
├── hooks/              # Custom React hooks
├── store/              # Redux store configuration
│   ├── slices/         # Redux slices
│   └── api/            # RTK Query API slices
├── services/           # External service integrations
├── utils/              # Utility functions
├── types/              # TypeScript type definitions
├── constants/          # Application constants
└── assets/             # Static assets
```

### Component Architecture
```
App
├── AuthProvider
├── ThemeProvider
├── Router
│   ├── PublicRoute (Login, Register)
│   └── PrivateRoute
│       ├── Layout
│       │   ├── Sidebar
│       │   ├── Header
│       │   └── Main Content
│       ├── Dashboard
│       ├── Posts
│       ├── Campaigns
│       ├── Analytics
│       └── Settings
└── NotificationProvider
```

## User Flows & Features

### 1. Authentication Flow
```
Landing Page → Register/Login → Instagram Connection → Dashboard
```

**Features:**
- User registration with email validation
- Secure login with JWT tokens
- Instagram OAuth integration
- Password reset functionality
- Remember me option

### 2. Dashboard Overview
```
Dashboard → Analytics Summary + Quick Actions + Recent Posts
```

**Features:**
- Key metrics overview (reach, engagement, follower growth)
- Quick post creation
- Recent post performance
- Upcoming scheduled posts
- Campaign status indicators

### 3. Content Creation Flow
```
Posts → Create New → Manual/AI Generation → Preview → Schedule/Publish
```

**Features:**
- Manual content creation
- AI-powered caption generation
- AI image generation
- Hashtag suggestions
- Post scheduling
- Multiple post types (photo, video, carousel, reel)

### 4. Campaign Management
```
Campaigns → Create Campaign → Set Parameters → Auto Content Generation → Monitor Performance
```

**Features:**
- Campaign creation wizard
- Automated content generation
- Performance tracking
- Campaign optimization suggestions

### 5. Analytics & Insights
```
Analytics → Overview → Post Performance → Audience Insights → Trend Analysis
```

**Features:**
- Performance dashboard
- Individual post analytics
- Audience demographics
- Engagement trends
- ROI calculations

## Component Hierarchy

### 1. Layout Components

#### Main Layout
```typescript
interface LayoutProps {
  children: React.ReactNode;
}

// Components:
- AppHeader: Navigation, user menu, notifications
- Sidebar: Main navigation menu
- MainContent: Page content area
- Footer: App information and links
```

#### Dashboard Layout
```typescript
interface DashboardLayoutProps {
  title: string;
  actions?: React.ReactNode;
  children: React.ReactNode;
}

// Features:
- Page title and breadcrumbs
- Action buttons area
- Content grid system
- Responsive design
```

### 2. Content Components

#### Post Components
```typescript
// PostCard: Display post information
interface PostCardProps {
  post: Post;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
  onPublish: (id: string) => void;
}

// PostForm: Create/edit posts
interface PostFormProps {
  initialData?: Partial<Post>;
  onSubmit: (data: PostFormData) => void;
  isLoading?: boolean;
}

// PostPreview: Preview post before publishing
interface PostPreviewProps {
  post: Post;
  onConfirm: () => void;
  onEdit: () => void;
}
```

#### AI Generation Components
```typescript
// CaptionGenerator: AI caption generation interface
interface CaptionGeneratorProps {
  onGenerate: (caption: string) => void;
  initialDescription?: string;
}

// ImageGenerator: AI image generation interface
interface ImageGeneratorProps {
  onGenerate: (imageUrl: string) => void;
  prompt?: string;
}

// HashtagSuggestions: Hashtag recommendation component
interface HashtagSuggestionsProps {
  content: string;
  onSelect: (hashtags: string[]) => void;
  maxCount?: number;
}
```

### 3. Analytics Components

#### Chart Components
```typescript
// EngagementChart: Engagement metrics visualization
interface EngagementChartProps {
  data: EngagementData[];
  period: DateRange;
  metric: 'likes' | 'comments' | 'shares' | 'saves';
}

// PerformanceMetrics: KPI display component
interface PerformanceMetricsProps {
  metrics: {
    reach: number;
    impressions: number;
    engagement_rate: number;
    follower_growth: number;
  };
  period: string;
  comparison?: 'previous_period' | 'last_year';
}

// AudienceInsights: Audience demographics
interface AudienceInsightsProps {
  demographics: AudienceData;
  topCountries: string[];
  ageDistribution: AgeGroup[];
}
```

### 4. Form Components

#### Smart Form Components
```typescript
// PostScheduler: Post scheduling interface
interface PostSchedulerProps {
  value?: Date;
  onChange: (date: Date) => void;
  minDate?: Date;
  timezone: string;
}

// MediaUploader: File upload with preview
interface MediaUploaderProps {
  accept: 'image' | 'video' | 'both';
  maxSize: number;
  onUpload: (files: File[]) => void;
  preview?: boolean;
}

// CampaignWizard: Multi-step campaign creation
interface CampaignWizardProps {
  onComplete: (campaign: CampaignData) => void;
  onCancel: () => void;
}
```

## State Management

### Redux Store Structure
```typescript
interface RootState {
  auth: AuthState;
  posts: PostsState;
  campaigns: CampaignsState;
  analytics: AnalyticsState;
  ui: UIState;
  notifications: NotificationsState;
}
```

### Auth Slice
```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  instagramConnected: boolean;
}

// Actions:
- login: Authenticate user
- logout: Clear user session
- refreshToken: Refresh JWT token
- connectInstagram: Link Instagram account
- updateProfile: Update user profile
```

### Posts Slice
```typescript
interface PostsState {
  items: Post[];
  selectedPost: Post | null;
  filters: PostFilters;
  isLoading: boolean;
  error: string | null;
  pagination: PaginationState;
}

// Actions:
- fetchPosts: Load posts with filters
- createPost: Create new post
- updatePost: Update existing post
- deletePost: Remove post
- publishPost: Publish post immediately
- setFilters: Update post filters
```

### Campaigns Slice
```typescript
interface CampaignsState {
  items: Campaign[];
  selectedCampaign: Campaign | null;
  isLoading: boolean;
  error: string | null;
  analytics: CampaignAnalytics | null;
}

// Actions:
- fetchCampaigns: Load campaigns
- createCampaign: Create new campaign
- updateCampaign: Update campaign
- deleteCampaign: Remove campaign
- fetchCampaignAnalytics: Load campaign performance
```

### UI Slice
```typescript
interface UIState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  notifications: Notification[];
  modals: {
    postPreview: boolean;
    deleteConfirm: boolean;
    aiGeneration: boolean;
  };
  loading: {
    aiGeneration: boolean;
    publishing: boolean;
  };
}
```

## API Integration

### RTK Query Setup
```typescript
// Base API configuration
const baseApi = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: '/api/v1',
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.token;
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ['Post', 'Campaign', 'User', 'Analytics'],
  endpoints: () => ({}),
});
```

### API Slice Examples

#### Posts API
```typescript
const postsApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getPosts: builder.query<PostsResponse, PostsQueryParams>({
      query: (params) => ({
        url: '/posts',
        params,
      }),
      providesTags: ['Post'],
    }),
    
    createPost: builder.mutation<Post, CreatePostRequest>({
      query: (post) => ({
        url: '/posts',
        method: 'POST',
        body: post,
      }),
      invalidatesTags: ['Post'],
    }),
    
    publishPost: builder.mutation<PublishResponse, string>({
      query: (postId) => ({
        url: `/posts/${postId}/publish`,
        method: 'POST',
      }),
      invalidatesTags: ['Post'],
    }),
  }),
});
```

#### AI Content API
```typescript
const aiApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    generateCaption: builder.mutation<CaptionResponse, CaptionRequest>({
      query: (request) => ({
        url: '/content/caption/generate',
        method: 'POST',
        body: request,
      }),
    }),
    
    generateImage: builder.mutation<ImageResponse, ImageRequest>({
      query: (request) => ({
        url: '/content/image/generate',
        method: 'POST',
        body: request,
      }),
    }),
    
    suggestHashtags: builder.mutation<HashtagResponse, HashtagRequest>({
      query: (request) => ({
        url: '/content/hashtags/suggest',
        method: 'POST',
        body: request,
      }),
    }),
  }),
});
```

### Custom Hooks for API Integration

#### Posts Hooks
```typescript
// Hook for posts with caching and filtering
export const usePosts = (filters?: PostFilters) => {
  const {
    data: postsResponse,
    isLoading,
    error,
    refetch,
  } = useGetPostsQuery(filters || {});

  const [createPost, { isLoading: isCreating }] = useCreatePostMutation();
  const [updatePost, { isLoading: isUpdating }] = useUpdatePostMutation();
  const [deletePost, { isLoading: isDeleting }] = useDeletePostMutation();

  return {
    posts: postsResponse?.posts || [],
    totalPosts: postsResponse?.total || 0,
    pagination: {
      page: postsResponse?.page || 1,
      pages: postsResponse?.pages || 1,
      hasNext: postsResponse?.has_next || false,
      hasPrev: postsResponse?.has_prev || false,
    },
    isLoading,
    error,
    refetch,
    createPost,
    updatePost,
    deletePost,
    isCreating,
    isUpdating,
    isDeleting,
  };
};

// Hook for AI content generation
export const useAIGeneration = () => {
  const [generateCaption, { isLoading: isGeneratingCaption }] = useGenerateCaptionMutation();
  const [generateImage, { isLoading: isGeneratingImage }] = useGenerateImageMutation();
  const [suggestHashtags, { isLoading: isGeneratingHashtags }] = useSuggestHashtagsMutation();

  return {
    generateCaption,
    generateImage,
    suggestHashtags,
    isGeneratingCaption,
    isGeneratingImage,
    isGeneratingHashtags,
    isGenerating: isGeneratingCaption || isGeneratingImage || isGeneratingHashtags,
  };
};
```

## Authentication Flow

### Implementation Strategy

#### 1. Authentication Context
```typescript
interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (userData: RegisterData) => Promise<void>;
  connectInstagram: (authCode: string) => Promise<void>;
}

// AuthProvider component wraps the entire app
// Handles token refresh, session management
// Redirects on authentication state changes
```

#### 2. Protected Routes
```typescript
// Route protection component
const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, isLoading } = useAuth();
  
  if (isLoading) return <LoadingSpinner />;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  
  return <>{children}</>;
};

// Instagram connection guard
const InstagramRequiredRoute = ({ children }: { children: React.ReactNode }) => {
  const { user } = useAuth();
  
  if (!user?.instagram_connected) {
    return <InstagramConnectionPrompt />;
  }
  
  return <>{children}</>;
};
```

#### 3. Token Management
```typescript
// Automatic token refresh
const useTokenRefresh = () => {
  const { token, refreshToken } = useAuth();
  
  useEffect(() => {
    if (!token) return;
    
    const tokenData = parseJWT(token);
    const expiresIn = tokenData.exp * 1000 - Date.now();
    
    // Refresh token 5 minutes before expiry
    const refreshTime = Math.max(expiresIn - 5 * 60 * 1000, 0);
    
    const timeoutId = setTimeout(() => {
      refreshToken();
    }, refreshTime);
    
    return () => clearTimeout(timeoutId);
  }, [token, refreshToken]);
};
```

## Real-time Features

### WebSocket Integration

#### 1. WebSocket Hook
```typescript
interface UseWebSocketOptions {
  onPostStatusChange?: (data: PostStatusChange) => void;
  onAnalyticsUpdate?: (data: AnalyticsUpdate) => void;
  onAIGenerationComplete?: (data: AIGenerationComplete) => void;
}

export const useWebSocket = (options: UseWebSocketOptions) => {
  const { user, token } = useAuth();
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!user || !token) return;

    const ws = new WebSocket(`${WS_BASE_URL}/user/${user.id}?token=${token}`);
    wsRef.current = ws;

    ws.onopen = () => setIsConnected(true);
    ws.onclose = () => setIsConnected(false);
    
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      
      switch (message.event) {
        case 'post_status_changed':
          options.onPostStatusChange?.(message.data);
          break;
        case 'analytics_updated':
          options.onAnalyticsUpdate?.(message.data);
          break;
        case 'ai_generation_complete':
          options.onAIGenerationComplete?.(message.data);
          break;
      }
    };

    return () => {
      ws.close();
    };
  }, [user, token]);

  return { isConnected };
};
```

#### 2. Real-time Updates Integration
```typescript
// Component that listens to real-time updates
const PostsListPage = () => {
  const { posts, refetch } = usePosts();
  const dispatch = useAppDispatch();

  useWebSocket({
    onPostStatusChange: (data) => {
      // Update specific post in store
      dispatch(updatePostStatus({
        postId: data.post_id,
        status: data.new_status,
        publishedAt: data.published_at,
        instagramPostId: data.instagram_post_id,
      }));
      
      // Show notification
      dispatch(addNotification({
        type: 'success',
        message: `Post "${data.post_id}" was ${data.new_status}`,
      }));
    },
    
    onAnalyticsUpdate: (data) => {
      // Update analytics in store
      dispatch(updatePostAnalytics(data));
    },
  });

  return (
    <div>
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
};
```

## UI/UX Guidelines

### Design System

#### 1. Color Palette
```typescript
const theme = {
  colors: {
    primary: {
      50: '#f0f9ff',
      500: '#3b82f6',
      600: '#2563eb',
      900: '#1e3a8a',
    },
    secondary: {
      50: '#fdf2f8',
      500: '#ec4899',
      600: '#db2777',
    },
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    gray: {
      50: '#f9fafb',
      100: '#f3f4f6',
      500: '#6b7280',
      900: '#111827',
    },
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    '2xl': '3rem',
  },
};
```

#### 2. Typography Scale
```typescript
const typography = {
  fontFamily: {
    sans: ['Inter', 'system-ui', 'sans-serif'],
    mono: ['JetBrains Mono', 'monospace'],
  },
  fontSize: {
    xs: '0.75rem',
    sm: '0.875rem',
    base: '1rem',
    lg: '1.125rem',
    xl: '1.25rem',
    '2xl': '1.5rem',
    '3xl': '1.875rem',
  },
  fontWeight: {
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },
};
```

### Component Design Patterns

#### 1. Card Components
```typescript
// Standard card design for posts, campaigns, analytics
interface CardProps {
  title?: string;
  subtitle?: string;
  actions?: React.ReactNode;
  children: React.ReactNode;
  variant?: 'default' | 'outlined' | 'elevated';
}

// Usage patterns:
- PostCard: Image, caption preview, metrics, actions
- CampaignCard: Name, date range, performance indicators
- MetricCard: Large number, label, trend indicator
```

#### 2. Data Display Components
```typescript
// Table component for data lists
interface DataTableProps<T> {
  data: T[];
  columns: ColumnDef<T>[];
  pagination?: PaginationConfig;
  sorting?: SortingConfig;
  filtering?: FilteringConfig;
  loading?: boolean;
  empty?: React.ReactNode;
}

// Chart component wrapper
interface ChartContainerProps {
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
  children: React.ReactNode;
  loading?: boolean;
  error?: string;
}
```

#### 3. Form Design Patterns
```typescript
// Consistent form layout
interface FormSectionProps {
  title: string;
  description?: string;
  children: React.ReactNode;
  required?: boolean;
}

// Form field with validation
interface FormFieldProps {
  label: string;
  error?: string;
  helperText?: string;
  required?: boolean;
  children: React.ReactNode;
}
```

### Responsive Design Strategy

#### 1. Breakpoint System
```typescript
const breakpoints = {
  xs: '475px',
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
};

// Layout adaptations:
- Mobile (xs-sm): Single column, bottom navigation
- Tablet (md): Two columns, collapsible sidebar
- Desktop (lg+): Full sidebar, three columns for content
```

#### 2. Mobile-First Approach
```typescript
// Component responsive patterns
const ResponsiveGrid = () => (
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    {/* Grid items */}
  </div>
);

const ResponsiveNavigation = () => (
  <>
    {/* Mobile navigation */}
    <div className="md:hidden">
      <MobileNavigation />
    </div>
    
    {/* Desktop sidebar */}
    <div className="hidden md:block">
      <DesktopSidebar />
    </div>
  </>
);
```

### Accessibility Implementation

#### 1. ARIA Labels and Roles
```typescript
// Screen reader support
const PostCard = ({ post }: { post: Post }) => (
  <article
    role="article"
    aria-labelledby={`post-title-${post.id}`}
    aria-describedby={`post-metrics-${post.id}`}
  >
    <h3 id={`post-title-${post.id}`}>
      {post.caption.substring(0, 50)}...
    </h3>
    <div id={`post-metrics-${post.id}`} aria-label="Post metrics">
      {post.analytics.likes_count} likes, {post.analytics.comments_count} comments
    </div>
  </article>
);
```

#### 2. Keyboard Navigation
```typescript
// Focus management
const Modal = ({ isOpen, onClose, children }: ModalProps) => {
  const focusTrapRef = useFocusTrap(isOpen);
  
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    
    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }
  }, [isOpen, onClose]);
  
  return (
    <div ref={focusTrapRef} role="dialog" aria-modal="true">
      {children}
    </div>
  );
};
```

## Performance Optimization

### Code Splitting Strategy

#### 1. Route-based Splitting
```typescript
// Lazy load page components
const Dashboard = lazy(() => import('../pages/Dashboard'));
const Posts = lazy(() => import('../pages/Posts'));
const Campaigns = lazy(() => import('../pages/Campaigns'));
const Analytics = lazy(() => import('../pages/Analytics'));

// Router with suspense
const AppRouter = () => (
  <Router>
    <Routes>
      <Route
        path="/dashboard"
        element={
          <Suspense fallback={<PageSkeleton />}>
            <Dashboard />
          </Suspense>
        }
      />
    </Routes>
  </Router>
);
```

#### 2. Component-based Splitting
```typescript
// Heavy components lazy loaded
const ChartComponent = lazy(() => import('../components/Chart'));
const ImageEditor = lazy(() => import('../components/ImageEditor'));

// Conditional loading
const ConditionalChart = ({ showChart }: { showChart: boolean }) => (
  <>
    {showChart && (
      <Suspense fallback={<ChartSkeleton />}>
        <ChartComponent />
      </Suspense>
    )}
  </>
);
```

### Data Loading Optimization

#### 1. Efficient Caching
```typescript
// RTK Query cache configuration
const postsApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getPosts: builder.query<PostsResponse, PostsQueryParams>({
      query: (params) => ({ url: '/posts', params }),
      // Cache for 5 minutes
      keepUnusedDataFor: 300,
      // Background refetch
      refetchOnMountOrArgChange: 30,
    }),
  }),
});
```

#### 2. Pagination and Virtual Scrolling
```typescript
// Infinite scroll for large lists
const useInfiniteScroll = (fetchMore: () => void) => {
  const [isFetching, setIsFetching] = useState(false);
  
  useEffect(() => {
    const handleScroll = () => {
      if (
        window.innerHeight + document.documentElement.scrollTop
        !== document.documentElement.offsetHeight
        || isFetching
      ) return;
      
      setIsFetching(true);
      fetchMore();
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [fetchMore, isFetching]);
  
  return { isFetching, setIsFetching };
};
```

### Image Optimization

#### 1. Lazy Loading and Optimization
```typescript
// Image component with lazy loading
interface OptimizedImageProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  placeholder?: string;
}

const OptimizedImage = ({ src, alt, width, height, placeholder }: OptimizedImageProps) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [error, setError] = useState(false);
  
  return (
    <div className="relative">
      {!isLoaded && !error && (
        <div className="absolute inset-0 bg-gray-200 animate-pulse" />
      )}
      <img
        src={src}
        alt={alt}
        width={width}
        height={height}
        loading="lazy"
        onLoad={() => setIsLoaded(true)}
        onError={() => setError(true)}
        className={`transition-opacity duration-200 ${
          isLoaded ? 'opacity-100' : 'opacity-0'
        }`}
      />
    </div>
  );
};
```

## Error Handling

### Error Boundary Implementation

#### 1. Global Error Boundary
```typescript
interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
  errorInfo?: ErrorInfo;
}

class GlobalErrorBoundary extends Component<
  { children: React.ReactNode },
  ErrorBoundaryState
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Global error boundary caught an error:', error, errorInfo);
    
    // Log to error reporting service
    if (process.env.NODE_ENV === 'production') {
      // Send to Sentry, LogRocket, etc.
    }
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback error={this.state.error} />;
    }

    return this.props.children;
  }
}
```

#### 2. API Error Handling
```typescript
// Centralized error handling
const useErrorHandler = () => {
  const dispatch = useAppDispatch();
  
  const handleError = useCallback((error: any) => {
    let message = 'An unexpected error occurred';
    let code = 'UNKNOWN_ERROR';
    
    if (error?.data?.error_code) {
      code = error.data.error_code;
      message = error.data.detail || message;
    }
    
    switch (code) {
      case 'INVALID_TOKEN':
        dispatch(logout());
        break;
      case 'RATE_LIMIT_EXCEEDED':
        dispatch(addNotification({
          type: 'warning',
          message: 'Rate limit exceeded. Please try again later.',
          duration: 5000,
        }));
        break;
      case 'INSTAGRAM_NOT_CONNECTED':
        dispatch(openInstagramConnectionModal());
        break;
      default:
        dispatch(addNotification({
          type: 'error',
          message,
          duration: 4000,
        }));
    }
  }, [dispatch]);
  
  return { handleError };
};
```

#### 3. Form Validation
```typescript
// Form error handling with react-hook-form
const useFormWithErrorHandling = <T extends FieldValues>(
  schema: ZodSchema<T>
) => {
  const methods = useForm<T>({
    resolver: zodResolver(schema),
    mode: 'onBlur',
  });
  
  const { handleError } = useErrorHandler();
  
  const handleSubmit = methods.handleSubmit(
    (data) => data,
    (errors) => {
      // Handle form validation errors
      Object.entries(errors).forEach(([field, error]) => {
        console.error(`Validation error in ${field}:`, error.message);
      });
    }
  );
  
  return {
    ...methods,
    handleSubmit: (onValid: (data: T) => void | Promise<void>) =>
      handleSubmit(async (data) => {
        try {
          await onValid(data);
        } catch (error) {
          handleError(error);
        }
      }),
  };
};
```

### User-Friendly Error Display

#### 1. Error Components
```typescript
// Error message component
interface ErrorMessageProps {
  title?: string;
  message: string;
  action?: {
    label: string;
    onClick: () => void;
  };
  variant?: 'inline' | 'page' | 'modal';
}

const ErrorMessage = ({ title, message, action, variant = 'inline' }: ErrorMessageProps) => {
  const baseClasses = 'p-4 rounded-lg border';
  const variantClasses = {
    inline: 'bg-red-50 border-red-200 text-red-700',
    page: 'bg-red-50 border-red-200 text-red-700 min-h-64 flex items-center justify-center',
    modal: 'bg-white border-red-200',
  };
  
  return (
    <div className={`${baseClasses} ${variantClasses[variant]}`}>
      {title && <h3 className="font-semibold mb-2">{title}</h3>}
      <p>{message}</p>
      {action && (
        <button
          onClick={action.onClick}
          className="mt-3 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          {action.label}
        </button>
      )}
    </div>
  );
};
```

#### 2. Loading States
```typescript
// Loading skeleton components
const PostCardSkeleton = () => (
  <div className="p-4 border rounded-lg animate-pulse">
    <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
    <div className="h-3 bg-gray-200 rounded w-1/2 mb-4"></div>
    <div className="h-32 bg-gray-200 rounded mb-4"></div>
    <div className="flex space-x-4">
      <div className="h-3 bg-gray-200 rounded w-16"></div>
      <div className="h-3 bg-gray-200 rounded w-16"></div>
    </div>
  </div>
);

const useLoadingState = (isLoading: boolean, minDuration = 500) => {
  const [showLoading, setShowLoading] = useState(false);
  
  useEffect(() => {
    let timer: NodeJS.Timeout;
    
    if (isLoading) {
      setShowLoading(true);
    } else {
      timer = setTimeout(() => setShowLoading(false), minDuration);
    }
    
    return () => clearTimeout(timer);
  }, [isLoading, minDuration]);
  
  return showLoading;
};
```

## Testing Strategy

### Unit Testing Setup

#### 1. Test Utilities
```typescript
// Custom render function with providers
const customRender = (
  ui: React.ReactElement,
  options?: {
    preloadedState?: Partial<RootState>;
    store?: ReturnType<typeof setupStore>;
  }
) => {
  const store = options?.store || setupStore(options?.preloadedState);
  
  const Wrapper = ({ children }: { children: React.ReactNode }) => (
    <Provider store={store}>
      <BrowserRouter>
        <ThemeProvider theme={theme}>
          {children}
        </ThemeProvider>
      </BrowserRouter>
    </Provider>
  );
  
  return {
    ...render(ui, { wrapper: Wrapper }),
    store,
  };
};

// Mock API responses
export const createMockPost = (overrides?: Partial<Post>): Post => ({
  id: 'post-1',
  caption: 'Test post caption',
  hashtags: ['#test', '#hashtag'],
  media_urls: ['https://example.com/image.jpg'],
  post_type: 'photo',
  status: 'published',
  analytics: {
    likes_count: 100,
    comments_count: 10,
    shares_count: 5,
    saves_count: 20,
    reach: 1000,
    impressions: 2000,
    engagement_rate: 13.5,
  },
  created_at: '2024-01-15T10:30:00Z',
  updated_at: '2024-01-15T10:30:00Z',
  ...overrides,
});
```

#### 2. Component Testing Examples
```typescript
// PostCard component test
describe('PostCard', () => {
  const mockPost = createMockPost();
  const mockHandlers = {
    onEdit: vi.fn(),
    onDelete: vi.fn(),
    onPublish: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('displays post information correctly', () => {
    customRender(<PostCard post={mockPost} {...mockHandlers} />);
    
    expect(screen.getByText(mockPost.caption)).toBeInTheDocument();
    expect(screen.getByText(`${mockPost.analytics.likes_count} likes`)).toBeInTheDocument();
    expect(screen.getByText(mockPost.status)).toBeInTheDocument();
  });

  it('calls onEdit when edit button is clicked', async () => {
    customRender(<PostCard post={mockPost} {...mockHandlers} />);
    
    const editButton = screen.getByRole('button', { name: /edit/i });
    await user.click(editButton);
    
    expect(mockHandlers.onEdit).toHaveBeenCalledWith(mockPost.id);
  });
});

// Form testing
describe('PostForm', () => {
  const mockOnSubmit = vi.fn();

  it('validates required fields', async () => {
    customRender(<PostForm onSubmit={mockOnSubmit} />);
    
    const submitButton = screen.getByRole('button', { name: /create post/i });
    await user.click(submitButton);
    
    expect(screen.getByText('Caption is required')).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('submits form with valid data', async () => {
    customRender(<PostForm onSubmit={mockOnSubmit} />);
    
    const captionInput = screen.getByLabelText(/caption/i);
    await user.type(captionInput, 'Test caption');
    
    const submitButton = screen.getByRole('button', { name: /create post/i });
    await user.click(submitButton);
    
    expect(mockOnSubmit).toHaveBeenCalledWith({
      caption: 'Test caption',
      // ... other form data
    });
  });
});
```

### Integration Testing

#### 1. API Integration Tests
```typescript
// Mock server setup
const server = setupServer(
  rest.get('/api/v1/posts', (req, res, ctx) => {
    return res(
      ctx.json({
        posts: [createMockPost()],
        total: 1,
        page: 1,
        pages: 1,
        has_next: false,
        has_prev: false,
      })
    );
  }),
  
  rest.post('/api/v1/posts', (req, res, ctx) => {
    return res(ctx.status(201), ctx.json(createMockPost()));
  })
);

describe('Posts Integration', () => {
  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());
  afterAll(() => server.close());

  it('loads and displays posts', async () => {
    customRender(<PostsListPage />);
    
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText('Test post caption')).toBeInTheDocument();
    });
  });
});
```

### E2E Testing Strategy

#### 1. Critical User Flows
```typescript
// Playwright E2E test example
test.describe('Post Creation Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.fill('[data-testid=email]', 'test@example.com');
    await page.fill('[data-testid=password]', 'password');
    await page.click('[data-testid=login-button]');
    await page.waitForURL('/dashboard');
  });

  test('creates a new post successfully', async ({ page }) => {
    // Navigate to posts page
    await page.click('[data-testid=posts-nav]');
    await page.waitForURL('/posts');
    
    // Click create post button
    await page.click('[data-testid=create-post-button]');
    
    // Fill post form
    await page.fill('[data-testid=post-caption]', 'Test post caption');
    await page.selectOption('[data-testid=post-type]', 'photo');
    
    // Submit form
    await page.click('[data-testid=submit-post]');
    
    // Verify success
    await expect(page.locator('[data-testid=success-message]')).toBeVisible();
    await expect(page.locator('text=Test post caption')).toBeVisible();
  });
});
```

## Deployment

### Build Configuration

#### 1. Environment Setup
```typescript
// Environment variables
interface Env {
  VITE_API_BASE_URL: string;
  VITE_WS_BASE_URL: string;
  VITE_FACEBOOK_APP_ID: string;
  VITE_SENTRY_DSN?: string;
  VITE_ENVIRONMENT: 'development' | 'staging' | 'production';
}

// Config per environment
const config = {
  development: {
    API_BASE_URL: 'http://localhost:8000/api/v1',
    WS_BASE_URL: 'ws://localhost:8000/ws',
    DEBUG: true,
  },
  staging: {
    API_BASE_URL: 'https://staging-api.defeah.com/api/v1',
    WS_BASE_URL: 'wss://staging-api.defeah.com/ws',
    DEBUG: false,
  },
  production: {
    API_BASE_URL: 'https://api.defeah.com/api/v1',
    WS_BASE_URL: 'wss://api.defeah.com/ws',
    DEBUG: false,
  },
};
```

#### 2. Build Optimization
```typescript
// Vite configuration
export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          ui: ['@mui/material', '@mui/icons-material'],
          charts: ['recharts', 'chart.js'],
          forms: ['react-hook-form', 'zod'],
        },
      },
    },
    chunkSizeWarningLimit: 1000,
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
      },
    },
  },
});
```

### CI/CD Pipeline

#### 1. GitHub Actions Workflow
```yaml
name: Deploy Frontend

on:
  push:
    branches: [main, staging]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - run: npm ci
      - run: npm run type-check
      - run: npm run lint
      - run: npm run test:unit
      - run: npm run test:e2e

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - run: npm ci
      - run: npm run build
        env:
          VITE_API_BASE_URL: ${{ secrets.API_BASE_URL }}
          VITE_FACEBOOK_APP_ID: ${{ secrets.FACEBOOK_APP_ID }}
      
      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        # Deploy to CDN/hosting service
```

### Performance Monitoring

#### 1. Analytics Integration
```typescript
// Analytics setup
const initializeAnalytics = () => {
  if (import.meta.env.PROD) {
    // Google Analytics
    gtag('config', 'GA_TRACKING_ID');
    
    // Sentry for error tracking
    Sentry.init({
      dsn: import.meta.env.VITE_SENTRY_DSN,
      environment: import.meta.env.VITE_ENVIRONMENT,
    });
  }
};

// Performance monitoring
const usePerformanceMonitoring = () => {
  useEffect(() => {
    // Monitor Core Web Vitals
    getCLS(console.log);
    getFID(console.log);
    getFCP(console.log);
    getLCP(console.log);
    getTTFB(console.log);
  }, []);
};
```

This comprehensive frontend development guide provides a complete roadmap for building the Defeah Marketing Dashboard, covering architecture, implementation patterns, best practices, and deployment strategies while leveraging the API documentation for seamless backend integration.