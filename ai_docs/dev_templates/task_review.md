# Task Review Checklist (worker-simple)

> **Note:** This checklist is tailored for the **worker-simple** template, which is a standard Next.js app (not a monorepo) with **Trigger.dev background jobs** for audio/video transcription.

Use this checklist to verify implementation quality before marking a task complete. Run through each section systematically.

---

## 1. Type Safety

### 1.1 No `any` Types
```bash
# Search for any types in changed files
grep -r "any" --include="*.ts" --include="*.tsx" <changed-files>
```

**Check for:**
- [ ] No explicit `any` type annotations
- [ ] No implicit `any` from missing types
- [ ] Proper generics used where needed

### 1.2 Explicit Return Types
```typescript
// ❌ Bad
async function getUser(id: string) {
  return await db.query.users.findFirst({ where: eq(users.id, id) });
}

// ✅ Good
async function getUser(id: string): Promise<User | undefined> {
  return await db.query.users.findFirst({ where: eq(users.id, id) });
}
```

**Check for:**
- [ ] All functions have explicit return types
- [ ] Async functions return `Promise<T>`
- [ ] Void functions explicitly return `void` or `Promise<void>`

### 1.3 No Type Assertions Without Justification
```typescript
// ❌ Bad - hiding potential issues
const user = data as User;

// ✅ Good - validate first
if (isUser(data)) {
  const user = data;
}
```

---

## 2. Drizzle ORM

### 2.1 Type-Safe Operators (No Raw SQL)
```typescript
// ❌ Bad - SQL injection risk
sql`${column} = ANY(${array})`;
where: sql`user_id = ${userId}`;

// ✅ Good - Type-safe operators
import { eq, inArray, and, or, isNull, like, between } from 'drizzle-orm';
where: eq(users.id, userId);
where: inArray(posts.status, ['draft', 'published']);
```

**Available operators:** `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `inArray`, `notInArray`, `and`, `or`, `isNull`, `isNotNull`, `like`, `ilike`, `between`

### 2.2 Proper Transaction Usage
```typescript
// ✅ Good - atomic operations
await db.transaction(async (tx) => {
  await tx.insert(orders).values(orderData);
  await tx.update(inventory).set({ quantity: sql`quantity - 1` });
});
```

### 2.3 Select Only Needed Columns
```typescript
// ❌ Bad - fetching everything
const users = await db.select().from(usersTable);

// ✅ Good - specific columns
const users = await db.select({
  id: usersTable.id,
  email: usersTable.email,
}).from(usersTable);
```

---

## 3. Next.js 15 Patterns

### 3.1 Async Params/SearchParams
```typescript
// ✅ Server Components - await the promises
interface PageProps {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ query?: string }>;
}

export default async function Page({ params, searchParams }: PageProps) {
  const { id } = await params;
  const { query } = await searchParams;
}

// ✅ Client Components - use React's use() hook
'use client';
import { use } from 'react';

export default function ClientPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
}
```

### 3.2 revalidatePath with Dynamic Routes
```typescript
// Static paths - NO type parameter needed
revalidatePath('/history');
revalidatePath('/transcripts');
revalidatePath('/profile');

// ❌ Bad - dynamic route missing type parameter
revalidatePath('/transcripts/[jobId]');

// ✅ Good - dynamic routes NEED type parameter
revalidatePath('/transcripts/[jobId]', 'page');
revalidatePath('/api/download/[jobId]/[format]', 'layout');
```

**Rule of thumb:** Only routes with `[brackets]` need the type parameter.

### 3.3 No Async Client Components
```typescript
// ❌ Bad - async client component
'use client';
export default async function Component() { // ERROR
  const data = await fetchData();
}

// ✅ Good - use hooks for data fetching
'use client';
import { useEffect, useState } from 'react';

export default function Component() {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetchData().then(setData);
  }, []);
}
```

---

## 4. Server/Client Separation

### 4.1 File Naming Convention
```
lib/
├── storage-client.ts    # Client-safe: constants, types, pure functions
├── storage.ts           # Server-only: DB access, can re-export from -client
├── auth-client.ts       # Client-safe auth utilities
└── auth.ts              # Server-only auth (createClient, etc.)
```

### 4.2 No Mixed Imports
```typescript
// ❌ Bad - mixed concerns in one file
// lib/utils.ts
import { createClient } from '@/lib/supabase/server';  // Server-only
export const MAX_SIZE = 10 * 1024 * 1024;              // Client-safe

// ✅ Good - separate files
// lib/utils-client.ts
export const MAX_SIZE = 10 * 1024 * 1024;

// lib/utils.ts
import { createClient } from '@/lib/supabase/server';
export { MAX_SIZE } from './utils-client';
```

### 4.3 Server-Only Imports Check
```typescript
// These imports are SERVER-ONLY - never import in 'use client' files:
import { createClient } from '@/lib/supabase/server';
import { db } from '@/lib/drizzle';
import { headers, cookies } from 'next/headers';
```

---

## 5. Security

### 5.1 Authentication on Protected Routes
```typescript
// ✅ Every protected API route must check auth
export async function POST(request: Request): Promise<Response> {
  const supabase = await createClient();
  const { data: { user }, error } = await supabase.auth.getUser();

  if (error || !user) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // ... rest of handler
}
```

### 5.2 Public Routes Configuration
Public routes are configured in `lib/supabase/middleware.ts`:

```typescript
// lib/supabase/middleware.ts
const publicRoutes = ["/", "/cookies", "/privacy", "/terms"];
const publicPatterns = ["/auth"];

const isPublicRoute =
  publicRoutes.includes(request.nextUrl.pathname) ||
  publicPatterns.some((pattern) =>
    request.nextUrl.pathname.startsWith(pattern)
  );
```

**When adding new public routes:**
- [ ] Add exact paths to `publicRoutes` array
- [ ] Add prefix patterns to `publicPatterns` array
- [ ] Webhooks are auto-skipped: `/api/webhooks/*`

### 5.3 Input Validation
```typescript
// ✅ Validate all user input
import { z } from 'zod';

const CreatePostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
  published: z.boolean().default(false),
});

export async function POST(request: Request): Promise<Response> {
  const body = await request.json();
  const result = CreatePostSchema.safeParse(body);

  if (!result.success) {
    return Response.json({ error: result.error.issues }, { status: 400 });
  }

  // Use result.data - it's typed!
}
```

### 5.4 No Secrets in Client Code
```typescript
// ❌ Bad - exposing secrets
const apiKey = process.env.STRIPE_SECRET_KEY; // In client component

// ✅ Good - only NEXT_PUBLIC_ vars in client
const publishableKey = process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY;
```

---

## 6. Trigger.dev Background Jobs

### 6.1 Task Structure
Tasks are located in `trigger/tasks/` and exported from `trigger/index.ts`.

```typescript
// ✅ Proper task structure
import { logger, task, metadata } from "@trigger.dev/sdk";

export interface MyTaskPayload {
  jobId: string;
  userId: string;
  // ... other fields
}

export const myTask = task({
  id: "my-task-name",
  run: async (payload: MyTaskPayload) => {
    const { jobId, userId } = payload;

    // Always log task start
    logger.info("Starting task", { jobId, userId });

    try {
      // Task logic here
      return { success: true };
    } catch (error) {
      logger.error("Task failed", { error, jobId });
      throw error;
    }
  },
});
```

### 6.2 Progress Tracking with Metadata
Use `metadata.root.set()` to update progress that the UI can poll:

```typescript
// ✅ Good - Update progress throughout the task
metadata.root.set("progress", 35);
metadata.root.set("currentStep", "Processing audio chunks");

// After each major step
metadata.root.set("progress", 60);
metadata.root.set("currentStep", "Transcribing with Whisper");

// On completion
metadata.root.set("progress", 100);
metadata.root.set("currentStep", "Transcription complete");

// On error
metadata.root.set("progress", 0);
metadata.root.set("currentStep", "Transcription failed");
metadata.root.set("error", error instanceof Error ? error.message : String(error));
```

### 6.3 User-Scoped Security Tags
**ALWAYS** include user tags when triggering tasks for token-level security:

```typescript
// ✅ Good - Include user tag when triggering tasks
await nextTask.trigger(
  {
    jobId,
    userId,
    // ... other payload
  },
  {
    tags: [`user:${userId}`], // User scoping for token-level security
  }
);

// ❌ Bad - Missing user tag
await nextTask.trigger({
  jobId,
  userId,
});
```

### 6.4 Error Handling in Tasks
```typescript
// ✅ Good - Proper error handling
try {
  // Task logic
} catch (error) {
  logger.error("Task failed", { error, jobId });

  // Update metadata for UI
  metadata.root.set("progress", 0);
  metadata.root.set("currentStep", "Task failed");
  metadata.root.set("error", error instanceof Error ? error.message : String(error));

  // Update job status in database
  await supabase
    .from("transcription_jobs")
    .update({
      status: "failed",
      error_message: error instanceof Error ? error.message : String(error),
    })
    .eq("id", jobId);

  throw error; // Re-throw for Trigger.dev to mark as failed
}
```

### 6.5 Task Chaining
When one task triggers another, always pass required context:

```typescript
// ✅ Good - Pass all required context to next task
await transcribeAudioTask.trigger(
  {
    jobId,
    userId,
    chunks: chunkRefs,
  },
  {
    tags: [`user:${userId}`],
  }
);
```

---

## 7. Error Handling

### 7.1 Consistent Error Responses
```typescript
// ✅ Standard error response format
return Response.json(
  { error: 'Resource not found' },
  { status: 404 }
);

// ✅ With details for validation errors
return Response.json(
  { error: 'Validation failed', details: result.error.issues },
  { status: 400 }
);
```

### 7.2 Try-Catch for External Calls
```typescript
// ✅ Wrap external API calls
try {
  const response = await stripe.customers.create({ email });
  return Response.json({ customerId: response.id });
} catch (error) {
  console.error('Stripe error:', error);
  return Response.json(
    { error: 'Payment service unavailable' },
    { status: 503 }
  );
}
```

### 7.3 Database Error Handling
```typescript
// ✅ Handle database errors gracefully
try {
  await db.insert(users).values(userData);
} catch (error) {
  if (error.code === '23505') { // Unique violation
    return Response.json({ error: 'Email already exists' }, { status: 409 });
  }
  console.error('Database error:', error);
  return Response.json({ error: 'Database error' }, { status: 500 });
}
```

---

## 8. Server Actions

### 8.1 Proper Server Action Structure
```typescript
// ✅ Server action with auth check
'use server';

import { createClient } from '@/lib/supabase/server';
import { revalidatePath } from 'next/cache';

export async function updateProfile(formData: FormData): Promise<{ error?: string }> {
  const supabase = await createClient();
  const { data: { user }, error: authError } = await supabase.auth.getUser();

  if (authError || !user) {
    return { error: 'Unauthorized' };
  }

  const name = formData.get('name') as string;

  // Validate input
  if (!name || name.length < 2) {
    return { error: 'Name must be at least 2 characters' };
  }

  // Perform action
  await db.update(profiles)
    .set({ name, updatedAt: new Date() })
    .where(eq(profiles.userId, user.id));

  revalidatePath('/profile');
  return {};
}
```

### 8.2 Return Types for Actions
```typescript
// ✅ Define clear return types
type ActionResult<T = void> =
  | { success: true; data: T }
  | { success: false; error: string };

export async function createPost(data: CreatePostInput): Promise<ActionResult<{ id: string }>> {
  // ...
  return { success: true, data: { id: post.id } };
}
```

---

## 9. Logging

### 9.1 Use the Logger Utility
This template has a logger utility at `lib/logger.ts` that provides environment-aware logging:

```typescript
import { logger } from "@/lib/logger";

// ✅ Good - Use logger instead of console
logger.debug("Debug message");  // Development only
logger.info("Info message");    // Development only
logger.warn("Warning message"); // Development only
logger.error("Error message");  // Development + Production

// ❌ Bad - Raw console statements
console.log('user:', user);
```

**Log levels:**
- `debug` - Verbose internal details (development only)
- `info` - General information (development only)
- `warn` - Potential issues (development only)
- `error` - Critical issues (development + production)

### 9.2 Trigger.dev Task Logging
Inside Trigger.dev tasks, use the SDK's logger (different from app logger):

```typescript
import { logger } from "@trigger.dev/sdk";

// ✅ Good - Trigger.dev's logger for tasks
logger.info("Starting transcription", { jobId, chunkCount });
logger.error("Transcription failed", { error, jobId });
```

---

## 10. Code Quality

### 10.1 No TODO/FIXME in Production Code
```bash
# Check for leftover TODOs
grep -r "TODO\|FIXME\|XXX\|HACK" --include="*.ts" --include="*.tsx" <changed-files>
```

### 10.2 No Debug Console Statements
```typescript
// ❌ Bad - debug logging
console.log('user:', user);

// ✅ OK - use logger utility
logger.debug('user:', user);

// ✅ OK - error logging (use logger or console.error)
logger.error('Failed to process:', error);
```

### 10.3 No Commented-Out Code
```typescript
// ❌ Bad - dead code
// const oldImplementation = () => { ... };

// ✅ Good - remove it entirely, git has history
```

### 10.4 Consistent Naming
- **Files:** kebab-case (`user-profile.tsx`)
- **Components:** PascalCase (`UserProfile`)
- **Functions:** camelCase (`getUserProfile`)
- **Constants:** SCREAMING_SNAKE_CASE (`MAX_FILE_SIZE`)
- **Types/Interfaces:** PascalCase (`UserProfile`, `CreateUserInput`)

---

## 11. Testing Checklist

### 11.1 Manual Testing
- [ ] Happy path works as expected
- [ ] Error states handled gracefully
- [ ] Loading states display correctly
- [ ] Auth redirects work properly

### 11.2 Edge Cases
- [ ] Empty states handled
- [ ] Invalid input rejected
- [ ] Unauthorized access blocked
- [ ] Network errors handled

### 11.3 Trigger.dev Tasks
- [ ] Task triggers successfully
- [ ] Progress updates appear in UI
- [ ] Error states update UI correctly
- [ ] User tags included for security

### 11.4 Type Checking
```bash
# Run TypeScript compiler
npm run type-check
# or
npx tsc --noEmit
```

---

## 12. Final Verification

Before marking complete, verify:

- [ ] `npm run type-check` passes (or `npx tsc --noEmit`)
- [ ] `npm run lint` passes
- [ ] No `any` types introduced
- [ ] All functions have explicit return types
- [ ] Server/client separation maintained
- [ ] Auth checks on all protected routes
- [ ] Input validation on all user input
- [ ] Error handling is consistent
- [ ] No debug console.logs (use logger utility)
- [ ] revalidatePath includes type parameter for dynamic routes only
- [ ] Trigger.dev tasks include user tags for security
- [ ] Trigger.dev tasks update metadata for progress tracking

---

## Quick Reference: Common Mistakes

| Mistake | Fix |
|---------|-----|
| `any` type | Use specific type or generic |
| Missing return type | Add explicit `: ReturnType` |
| Raw SQL in Drizzle | Use `eq`, `inArray`, etc. |
| Async client component | Use `useEffect` + `useState` |
| Missing auth check | Add `getUser()` check first |
| `revalidatePath('/path/[id]')` | `revalidatePath('/path/[id]', 'page')` |
| `revalidatePath('/static', 'page')` | `revalidatePath('/static')` (no type needed) |
| Server import in client | Create `-client.ts` file |
| `console.log` debugging | Use `logger.debug()` from `lib/logger.ts` |
| Task without user tag | Add `tags: [\`user:${userId}\`]` when triggering |
| Task without progress | Use `metadata.root.set()` for progress updates |
