"""
Seed file for Node.js domain.
Creates domain, course, topics (lessons + quizzes), and practice scenarios.
"""
from sqlmodel import Session, select

from app.models.domain import Domain, Course
from app.models.lesson import Lesson, LessonContentType
from app.models.quiz import Quiz, QuizQuestion
from app.models.scenario import Difficulty, PracticeMode, Scenario, ScenarioCategory

# ─── Domain & Course ───────────────────────────────────────────────────────────

NODEJS_DOMAIN = {
    "slug": "node-js",
    "name": "Node.js Development",
    "description": "Master server-side JavaScript with Node.js — event loop, async patterns, Express.js, file system, streams, and building production-ready REST APIs.",
    "icon_name": "server",
    "color": "green",
    "order_index": 6,
    "is_active": True,
}

NODEJS_COURSE = {
    "slug": "node-js-fundamentals",
    "name": "Node.js Fundamentals",
    "description": "Core Node.js concepts every backend developer needs to know — from the event loop to building REST APIs with Express.",
    "order_index": 1,
    "is_active": True,
}

# ─── Topics ────────────────────────────────────────────────────────────────────

NODEJS_TOPICS = [
    # ── Topic 1: Event Loop ───────────────────────────────────────────────────
    {
        "name": "nodejs_event_loop",
        "title": "Event Loop & Runtime",
        "description": "Understand how Node.js works under the hood — the event loop, microtasks, libuv thread pool, and why Node.js excels at I/O-heavy workloads.",
        "icon_name": "refresh-cw",
        "order_index": 1,
        "lesson": {
            "title": "Node.js Event Loop: How It Really Works",
            "content": """# Node.js Event Loop & Runtime

Node.js is **single-threaded** but achieves high concurrency through its **event-driven, non-blocking I/O** architecture.

## The V8 Engine + libuv

Node.js = **V8** (JavaScript engine) + **libuv** (cross-platform async I/O library).

- V8 compiles and executes JS on a single thread (the "main thread")
- libuv provides the event loop, thread pool, and async I/O primitives
- The thread pool (default: 4 threads) handles blocking operations (file I/O, crypto, DNS)

## Event Loop Phases

The event loop cycles through 6 phases:

```
   ┌───────────────────────────┐
┌─>│           timers          │ setTimeout / setInterval callbacks
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │     pending callbacks     │ I/O callbacks deferred from previous cycle
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │       idle, prepare       │ internal use
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │           poll            │ retrieve new I/O events; execute I/O callbacks
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │           check           │ setImmediate() callbacks
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
└──┤      close callbacks      │ socket.on('close', ...)
   └───────────────────────────┘
```

## Microtasks (Priority Queue)

Microtasks run **between each phase**, not just at the end:

```
process.nextTick()  — highest priority, runs before any microtask
Promise callbacks   — .then(), .catch(), .finally()
queueMicrotask()    — explicit microtask
```

**Key rule**: process.nextTick() always runs before Promises.

```js
console.log('1')
setTimeout(() => console.log('2'), 0)
Promise.resolve().then(() => console.log('3'))
process.nextTick(() => console.log('4'))
console.log('5')

// Output: 1 → 5 → 4 → 3 → 2
```

## setImmediate vs setTimeout(fn, 0)

```js
// Inside I/O callbacks:
const fs = require('fs')
fs.readFile('/file.txt', () => {
  setTimeout(() => console.log('timeout'), 0)
  setImmediate(() => console.log('immediate'))
})
// immediate runs first (check phase comes right after poll)
// Outside I/O: order is non-deterministic (depends on event loop state)
```

## What Blocks the Event Loop?

- CPU-intensive sync operations (large JSON.parse, heavy crypto)
- Large synchronous loops
- Complex regex on long strings

```js
// ❌ Blocks the event loop — no requests can be processed
function fibonacci(n) {
  if (n <= 1) return n
  return fibonacci(n - 1) + fibonacci(n - 2)
}

// ✅ Non-blocking alternative: split work with setImmediate
function fibonacciAsync(n, cb) {
  if (n <= 1) return setImmediate(() => cb(n))
  setImmediate(() => fibonacciAsync(n-1, (r1) =>
    fibonacciAsync(n-2, (r2) => setImmediate(() => cb(r1 + r2)))
  ))
}
```

## Interview Tip
"Explain the event loop to me" is the most common Node.js interview question. Know the phases, microtask priority, and the difference between nextTick, microtasks, and setImmediate.
""",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "Event Loop Quiz",
            "description": "Test your understanding of the Node.js event loop.",
            "questions": [
                {
                    "question": "Which runs first: process.nextTick() or a resolved Promise callback?",
                    "options": [
                        "Promise callback runs first",
                        "process.nextTick() always runs first",
                        "They run in the order they are registered",
                        "Neither — they are in different phases",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "process.nextTick() has the highest priority in the microtask queue. It runs before any Promise callback, even if the Promise was resolved before nextTick was called.",
                    "order_index": 1,
                },
                {
                    "question": "What is the output order of setTimeout(fn, 0) vs setImmediate(fn) inside an I/O callback?",
                    "options": [
                        "Timeout always runs first",
                        "setImmediate always runs first inside I/O callbacks",
                        "The order is random",
                        "Both run simultaneously",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Inside the poll phase (I/O callbacks), the next phase is 'check' where setImmediate runs. setTimeout must wait for the next timer phase, so setImmediate runs first.",
                    "order_index": 2,
                },
                {
                    "question": "Why can a CPU-intensive synchronous operation be dangerous in Node.js?",
                    "options": [
                        "It crashes the V8 engine",
                        "It blocks the event loop, preventing any other requests from being handled",
                        "It increases memory usage exponentially",
                        "Synchronous code is always dangerous in Node.js",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Since Node.js runs on a single thread, a CPU-intensive synchronous operation blocks the event loop completely. No I/O, timers, or requests can be processed until it finishes.",
                    "order_index": 3,
                },
                {
                    "question": "What is libuv's default thread pool size?",
                    "options": ["2", "4", "8", "Depends on CPU cores"],
                    "correct_answer_index": 1,
                    "explanation": "libuv creates a thread pool with 4 threads by default. This can be changed by setting the UV_THREADPOOL_SIZE environment variable (up to 1024).",
                    "order_index": 4,
                },
                {
                    "question": "Which operations use the libuv thread pool?",
                    "options": [
                        "All I/O operations including network requests",
                        "File system operations, DNS lookups, and crypto operations",
                        "Only setTimeout and setInterval",
                        "All asynchronous operations in Node.js",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "File I/O, DNS lookups (dns.lookup), and CPU-intensive crypto use the thread pool. Network I/O (HTTP requests) are handled natively by the OS kernel, not the thread pool.",
                    "order_index": 5,
                },
            ],
        },
    },

    # ── Topic 2: Modules & npm ─────────────────────────────────────────────────
    {
        "name": "nodejs_modules",
        "title": "Modules & npm",
        "description": "Master CommonJS vs ES modules, package.json, semantic versioning, and npm best practices.",
        "icon_name": "package",
        "order_index": 2,
        "lesson": {
            "title": "Modules & npm: Package Management in Node.js",
            "content": """# Modules & npm

Node.js supports two module systems: **CommonJS** (require) and **ECMAScript Modules** (import/export).

## CommonJS (CJS)

The traditional Node.js module system. Synchronous, works everywhere.

```js
// math.js — exporting
const add = (a, b) => a + b
const PI = 3.14159
module.exports = { add, PI }
// or: exports.add = add

// app.js — importing
const { add, PI } = require('./math')
console.log(add(2, 3)) // 5
```

**How require() works internally:**
1. Resolve — find the file
2. Load — read the file content
3. Wrap — wrap in a function: `(function(exports, require, module, __filename, __dirname) { ... })`
4. Evaluate — execute the wrapped function
5. Cache — store the result in `require.cache`

## ECMAScript Modules (ESM)

Modern standard. Must use `.mjs` extension or `"type": "module"` in package.json.

```js
// math.mjs — exporting
export const add = (a, b) => a + b
export const PI = 3.14159
export default function greet(name) { return `Hello ${name}` }

// app.mjs — importing
import greet, { add, PI } from './math.mjs'
console.log(add(2, 3))
```

| Feature | CJS | ESM |
|---------|-----|-----|
| Syntax | require() / module.exports | import / export |
| Loading | Synchronous | Asynchronous |
| Tree shaking | No | Yes |
| Top-level await | No | Yes |
| Strict mode | No | Yes (implicit) |

**CJS → ESM rules:**
- CJS cannot `require()` ESM (use dynamic import)
- ESM can `import` CJS (default import only, no named destructuring)
- ESM can use `import()` to load CJS dynamically

## package.json Essentials

```json
{
  "name": "my-express-api",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "node src/index.js",
    "dev": "node --watch src/index.js",
    "test": "node --test"
  },
  "dependencies": {
    "express": "^4.18.2"
  },
  "devDependencies": {
    "nodemon": "^3.1.0"
  }
}
```

## Semantic Versioning (semver)

```
^4.18.2  → compatible with 4.x.x  (>=4.18.2 <5.0.0)
~4.18.2  → compatible with 4.18.x (>=4.18.2 <4.19.0)
4.18.2   → exact version only
*        → any version (dangerous!)
```

`npm ci` (clean install) uses exact versions from `package-lock.json` — always use in CI/CD.

## Best Practices

- Use `npm ci` in CI/CD (faster and reproducible)
- Commit `package-lock.json` (but never edit manually)
- Use `npx` for one-off CLI tools
- Run `npm audit` regularly
- Use `"engines"` field to specify Node.js version

## Interview Tip
"Why choose ESM over CommonJS?" — ESM enables tree shaking for smaller bundles, supports top-level await, and is the web standard. For new projects, ESM is recommended. For existing codebases, the migration cost may not be justified.
""",
            "content_type": LessonContentType.explanation,
            "order_index": 2,
            "estimated_minutes": 10,
        },
        "quiz": {
            "title": "Modules & npm Quiz",
            "description": "Test your knowledge of Node.js modules and npm.",
            "questions": [
                {
                    "question": "What does `^4.18.2` allow in semver?",
                    "options": [
                        "Only version 4.18.2 exactly",
                        "Any version >= 4.18.2 and < 5.0.0",
                        "Any version >= 4.18.2 and < 4.19.0",
                        "Any version including 5.0.0 and above",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "The caret ^ allows changes that do not modify the left-most non-zero digit. For ^4.18.2, it accepts any 4.x.x version >= 4.18.2.",
                    "order_index": 1,
                },
                {
                    "question": "Why should you use `npm ci` instead of `npm install` in CI/CD pipelines?",
                    "options": [
                        "It installs newer versions automatically",
                        "It uses exact versions from package-lock.json and is faster",
                        "It installs only devDependencies",
                        "It creates a new package-lock.json",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "npm ci is designed for CI environments. It uses exact versions from package-lock.json (no version resolution), deletes node_modules first, and is significantly faster than npm install.",
                    "order_index": 2,
                },
                {
                    "question": "Can a CommonJS module directly require() an ES module?",
                    "options": [
                        "Yes, with require('./module.mjs')",
                        "No, CommonJS cannot require ES modules — use dynamic import() instead",
                        "Yes, if 'type: module' is in package.json",
                        "Yes, CJS and ESM are fully interoperable",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "CommonJS cannot synchronously require ES modules because ESM loads asynchronously. Use `import('./module.mjs')` which returns a Promise, or convert to ESM.",
                    "order_index": 3,
                },
                {
                    "question": "What is one advantage of ES modules over CommonJS?",
                    "options": [
                        "ESM files load synchronously which is faster",
                        "ESM enables tree shaking and supports top-level await",
                        "ESM is required for all npm packages",
                        "ESM uses less memory than CJS",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "ES modules support static analysis (enabling tree shaking to remove unused code) and top-level await. They're also the standard for modern JavaScript and browsers.",
                    "order_index": 4,
                },
                {
                    "question": "What does the `require.cache` object do?",
                    "options": [
                        "It stores all npm registry URLs",
                        "It caches loaded modules so they are not re-executed on subsequent requires",
                        "It stores environment variables",
                        "It caches HTTP responses from the module",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Once a module is loaded with require(), it's stored in require.cache. Subsequent require() calls return the cached exports without re-executing the module code.",
                    "order_index": 5,
                },
            ],
        },
    },

    # ── Topic 3: File System & Streams ─────────────────────────────────────────
    {
        "name": "nodejs_filesystem",
        "title": "File System & Streams",
        "description": "Read, write, and stream files efficiently. Master fs, path, and Node.js streams for handling large data.",
        "icon_name": "folder",
        "order_index": 3,
        "lesson": {
            "title": "File System & Streams: Handling Data Efficiently",
            "content": """# File System & Streams

Node.js provides the **fs** module for file operations and **streams** for handling large amounts of data efficiently.

## File System (fs)

Node.js offers three ways to work with files:

### 1. Synchronous (blocking)
```js
const fs = require('fs')
const data = fs.readFileSync('/file.txt', 'utf8')
console.log(data)
fs.writeFileSync('/output.txt', 'Hello World')
```

### 2. Callback-based (async, non-blocking)
```js
fs.readFile('/file.txt', 'utf8', (err, data) => {
  if (err) return console.error(err)
  console.log(data)
})
```

### 3. Promise-based (fs/promises)
```js
const fs = require('fs/promises')
async function readFile() {
  try {
    const data = await fs.readFile('/file.txt', 'utf8')
    console.log(data)
  } catch (err) {
    console.error(err)
  }
}
```

**Rule**: Always use promise-based or callback API in production. Sync methods block the event loop.

### Common fs Operations
```js
fs.existsSync(path)          // check if path exists
fs.mkdir('dir', { recursive: true }) // create directory tree
fs.readdir('/path')          // list directory contents
fs.stat('/file')             // get file metadata
fs.unlink('/file')           // delete file
fs.rename('/old', '/new')    // move/rename
fs.access('/file', fs.constants.R_OK) // check permissions
```

## The path Module
```js
const path = require('path')
path.join('/users', 'alice', 'docs')      // → \\users\\alice\\docs (cross-platform)
path.resolve('src', 'index.js')           // → absolute path
path.extname('file.txt')                  // → .txt
path.basename('/users/file.txt')          // → file.txt
path.dirname('/users/file.txt')           // → /users
path.parse('/users/alice/docs/file.txt')  // → { root, dir, base, ext, name }
```

## Streams

Streams process data **chunk by chunk** without loading everything into memory.

### Four Types of Streams
| Type | Purpose | Example |
|------|---------|---------|
| Readable | Read data from source | fs.createReadStream() |
| Writable | Write data to destination | fs.createWriteStream() |
| Duplex | Both readable and writable | net.Socket |
| Transform | Modify data as it passes through | zlib.createGzip() |

### Piping Streams
```js
const { createReadStream, createWriteStream } = require('fs')
const { createGzip } = require('zlib')

// Read → Compress → Write (all streaming, minimal memory)
createReadStream('input.txt')
  .pipe(createGzip())
  .pipe(createWriteStream('output.txt.gz'))
  .on('finish', () => console.log('Compression done!'))
```

### Custom Transform Stream
```js
const { Transform } = require('stream')

const upperCaseTransform = new Transform({
  transform(chunk, encoding, callback) {
    this.push(chunk.toString().toUpperCase())
    callback()
  }
})

process.stdin.pipe(upperCaseTransform).pipe(process.stdout)
```

## When to Use Streams vs readFile

| Scenario | Use |
|----------|-----|
| Small config file (few KB) | readFile / readFileSync |
| 10MB JSON file | readFile (fine for 10MB) |
| 2GB CSV data processing | createReadStream (or memory will explode) |
| Real-time log tailing | createReadStream with watch |
| HTTP file server | pipe file stream to response |

## Interview Tip
"When would you use streams?" — "When dealing with large files. Reading a 2GB file with readFileSync would crash the process. Streams process data in chunks, keeping memory usage constant regardless of file size."
""",
            "content_type": LessonContentType.explanation,
            "order_index": 3,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "File System & Streams Quiz",
            "description": "Test your knowledge of Node.js file system and streams.",
            "questions": [
                {
                    "question": "Why should you avoid fs.readFileSync() in a web server?",
                    "options": [
                        "It returns a Buffer instead of a string",
                        "It blocks the event loop, preventing the server from handling other requests",
                        "It doesn't support UTF-8 encoding",
                        "Synchronous methods are deprecated in Node.js",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Synchronous methods block the event loop. If readFileSync takes 100ms for a large file, the server cannot handle any other requests during that time — including new incoming connections.",
                    "order_index": 1,
                },
                {
                    "question": "What is the main advantage of using streams over reading an entire file at once?",
                    "options": [
                        "Streams are always faster",
                        "Streams process data in chunks, keeping memory usage low regardless of file size",
                        "Streams can only be used for text files",
                        "Streams automatically compress data",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Streams process data in small chunks. A 2GB file streamed uses ~16KB of memory, whereas reading it entirely would consume 2GB+ of memory.",
                    "order_index": 2,
                },
                {
                    "question": "What does the .pipe() method do in Node.js streams?",
                    "options": [
                        "It creates a Unix pipe to an external process",
                        "It connects the output of one stream to the input of another, handling backpressure automatically",
                        "It buffers all data before writing",
                        "It converts a stream to a Promise",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "pipe() connects a readable stream to a writable stream. It automatically handles backpressure — pausing the readable stream when the writable is slow and resuming when ready.",
                    "order_index": 3,
                },
                {
                    "question": "Which path method creates a cross-platform path string?",
                    "options": [
                        "path.resolve()",
                        "path.join()",
                        "path.normalize()",
                        "path.concat()",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "path.join() concatenates path segments using the correct separator for the platform (/ on Linux, \\ on Windows). Always use it instead of string concatenation.",
                    "order_index": 4,
                },
                {
                    "question": "What is a Transform stream?",
                    "options": [
                        "A stream that can only read data",
                        "A stream that modifies data as it passes through — both readable and writable",
                        "A stream that writes data to multiple destinations",
                        "A stream that converts between file formats",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "A Transform stream is a Duplex stream that modifies or transforms data as it passes through. Examples: zlib compression, crypto encryption, CSV → JSON conversion.",
                    "order_index": 5,
                },
            ],
        },
    },

    # ── Topic 4: Express.js ────────────────────────────────────────────────────
    {
        "name": "nodejs_express",
        "title": "Express.js Fundamentals",
        "description": "Build REST APIs with Express.js — routing, middleware, error handling, and best practices for production apps.",
        "icon_name": "globe",
        "order_index": 4,
        "lesson": {
            "title": "Express.js: Building REST APIs",
            "content": """# Express.js Fundamentals

Express.js is the most popular Node.js web framework. It provides routing, middleware, and HTTP utilities on top of Node's built-in `http` module.

## Basic Server

```js
const express = require('express')
const app = express()

app.get('/', (req, res) => {
  res.json({ message: 'Hello World' })
})

app.listen(3000, () => console.log('Server on http://localhost:3000'))
```

## Routing

```js
// Route parameters
app.get('/users/:id', (req, res) => {
  const userId = req.params.id
  res.json({ userId })
})

// Query strings: GET /users?page=2&limit=10
app.get('/users', (req, res) => {
  const { page = 1, limit = 10 } = req.query
  res.json({ page: Number(page), limit: Number(limit) })
})

// Route grouping with Router
const router = express.Router()
router.get('/', listUsers)
router.post('/', createUser)
router.get('/:id', getUser)
router.put('/:id', updateUser)
router.delete('/:id', deleteUser)
app.use('/api/users', router)
```

## Middleware

Middleware functions have access to `req`, `res`, and the `next` function.

```js
// Application-level middleware
app.use(express.json())        // parse JSON bodies
app.use(express.urlencoded({ extended: true })) // parse form data

// Custom middleware — runs on every request
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`)
  next()
})

// Route-specific middleware
const requireAuth = (req, res, next) => {
  if (!req.headers.authorization) {
    return res.status(401).json({ error: 'Unauthorized' })
  }
  next()
}
app.get('/admin', requireAuth, adminHandler)

// Error-handling middleware (4 params = error handler)
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).json({ error: 'Something broke!' })
})
```

## Request Lifecycle

```
Request → middleware1 → middleware2 → route handler → response
                ↓ (if error)
           error middleware → error response
```

## Common Middleware Stack

```js
const express = require('express')
const cors = require('cors')
const helmet = require('helmet')
const morgan = require('morgan')
const rateLimit = require('express-rate-limit')

const app = express()

app.use(helmet())                // security headers
app.use(cors())                  // cross-origin
app.use(morgan('dev'))           // logging
app.use(rateLimit({              // rate limiting
  windowMs: 15 * 60 * 1000,
  max: 100,
}))
app.use(express.json())
```

## REST API Conventions

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /api/users | List users |
| GET | /api/users/:id | Get user by ID |
| POST | /api/users | Create user |
| PUT | /api/users/:id | Replace user |
| PATCH | /api/users/:id | Partial update |
| DELETE | /api/users/:id | Delete user |

**Response format:**
```json
{
  "success": true,
  "data": { "id": 1, "name": "Alice" }
}
```

**Error format:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Name is required"
  }
}
```

## Production Best Practices

- Use the `cluster` module or PM2 for multi-core utilization
- Set `NODE_ENV=production` (enables caching and disables verbose errors)
- Don't expose stack traces in production
- Use `compression` middleware for gzip
- Set proper HTTP status codes (200, 201, 204, 400, 401, 403, 404, 500)
- Never use `res.send()` with user input — prefer `res.json()`

## Interview Tip
"Design an API for a todo app" — show RESTful endpoints, proper HTTP methods, error handling, URL parameterization, and middleware for validation/auth. This demonstrates you think about the full request lifecycle.
""",
            "content_type": LessonContentType.explanation,
            "order_index": 4,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "Express.js Quiz",
            "description": "Test your knowledge of building REST APIs with Express.js.",
            "questions": [
                {
                    "question": "What is the correct order of middleware execution in Express?",
                    "options": [
                        "Route handler → middleware → error handler",
                        "Middleware → route handler → error handler (if error)",
                        "Error handler → middleware → route handler",
                        "Random order based on async completion",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Express processes middleware in the order they are registered. If a middleware calls next() without an error, the chain continues. If next(err) is called, Express skips to error-handling middleware.",
                    "order_index": 1,
                },
                {
                    "question": "What is the difference between app.use() and app.get()?",
                    "options": [
                        "app.use() only handles POST requests",
                        "app.use() matches any HTTP method and path prefix; app.get() only matches GET requests on the exact path",
                        "app.use() is for middleware only; app.get() is for route handlers only",
                        "There is no difference",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "app.use() is a middleware mount — it matches any HTTP method and triggers for URL prefixes. app.get() (and post, put, etc.) matches only the specified method and exact path.",
                    "order_index": 2,
                },
                {
                    "question": "How does Express distinguish an error-handling middleware from regular middleware?",
                    "options": [
                        "By prefixing the function name with 'error'",
                        "By accepting 4 parameters: (err, req, res, next)",
                        "By using app.error() instead of app.use()",
                        "By setting the status code to 500",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Express identifies error-handling middleware by its arity (number of parameters). Functions with 4 parameters are treated as error handlers and receive the error as the first argument.",
                    "order_index": 3,
                },
                {
                    "question": "Which HTTP status code should a POST /users endpoint return on success?",
                    "options": ["200 OK", "201 Created", "204 No Content", "302 Found"],
                    "correct_answer_index": 1,
                    "explanation": "201 Created is the correct status for successful resource creation. Return the created resource in the response body and optionally a Location header with the new resource URL.",
                    "order_index": 4,
                },
                {
                    "question": "Why use the compression middleware in production?",
                    "options": [
                        "It makes JavaScript execution faster",
                        "It gzips response bodies, significantly reducing bandwidth for JSON/text responses",
                        "It minifies JavaScript code sent to clients",
                        "It compresses request bodies from clients",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "The compression middleware gzips response bodies. For JSON APIs, this can reduce response size by 60-80%, improving latency and reducing bandwidth costs.",
                    "order_index": 5,
                },
            ],
        },
    },

    # ── Topic 5: Async Patterns ────────────────────────────────────────────────
    {
        "name": "nodejs_async",
        "title": "Asynchronous Patterns",
        "description": "Master async/await, Promise patterns, error handling in async code, and avoiding common pitfalls like callback hell.",
        "icon_name": "loader",
        "order_index": 5,
        "lesson": {
            "title": "Async Patterns: Callbacks, Promises, and async/await",
            "content": """# Asynchronous Patterns in Node.js

Node.js is fundamentally asynchronous. Understanding the evolution from callbacks to async/await is essential.

## 1. Callbacks (The Old Way)

```js
const fs = require('fs')

fs.readFile('/data.json', 'utf8', (err, data) => {
  if (err) return console.error('Failed:', err)
  try {
    const parsed = JSON.parse(data)
    console.log(parsed)
  } catch (e) {
    console.error('Invalid JSON')
  }
})
```

### Callback Hell (Pyramid of Doom)

```js
// ❌ Nested callbacks — hard to read, hard to debug
getUser(id, (err, user) => {
  if (err) return handleError(err)
  getOrders(user.id, (err, orders) => {
    if (err) return handleError(err)
    getDetails(orders[0].id, (err, details) => {
      if (err) return handleError(err)
      renderPage(user, orders, details)
    })
  })
})
```

## 2. Promises

```js
function readFilePromise(path) {
  return new Promise((resolve, reject) => {
    fs.readFile(path, 'utf8', (err, data) => {
      err ? reject(err) : resolve(data)
    })
  })
}

// Chaining — flatter than callbacks
readFilePromise('/data.json')
  .then(data => JSON.parse(data))
  .then(parsed => console.log(parsed))
  .catch(err => console.error('Failed:', err))
```

### Promise.all / Promise.allSettled / Promise.race

```js
// all — fails fast if any promise rejects
const [user, posts] = await Promise.all([
  fetchUser(1),
  fetchPosts(1),
])

// allSettled — waits for all, never rejects
const results = await Promise.allSettled([
  fetchUser(1),
  fetchUser(2),
  fetchUser(999), // might fail
])
// results: [{ status: 'fulfilled', value: ... }, { status: 'rejected', reason: ... }]

// race — resolves/rejects with first settled
const result = await Promise.race([
  fetchWithTimeout('/api', 5000),
  timeout(5000), // rejects after 5s
])
```

## 3. async/await (Modern Standard)

```js
async function loadDashboard(userId) {
  try {
    const user = await fetchUser(userId)
    const orders = await fetchOrders(user.id)
    return { user, orders }
  } catch (err) {
    console.error('Failed to load dashboard:', err)
    throw new Error('Dashboard unavailable')
  }
}

// Top-level await (ESM only)
const config = await fs.readFile('./config.json', 'utf8')
```

### Common Async Mistakes

```js
// ❌ Sequential where parallel is possible
const user = await fetchUser(id)      // wait 200ms
const posts = await fetchPosts(id)    // wait 200ms
// Total: 400ms

// ✅ Parallel with Promise.all
const [user, posts] = await Promise.all([
  fetchUser(id),
  fetchPosts(id),
])
// Total: 200ms

// ❌ forEach with async (doesn't await!)
users.forEach(async (user) => {
  await saveUser(user) // BUG: not awaited!
})

// ✅ for...of or Promise.all with map
for (const user of users) {
  await saveUser(user) // works for sequential
}
// or
await Promise.all(users.map(user => saveUser(user)))
```

## Error Handling Patterns

```js
// Pattern 1: try/catch (preferred for async/await)
async function handler(req, res) {
  try {
    const data = await processRequest(req)
    res.json(data)
  } catch (err) {
    res.status(500).json({ error: err.message })
  }
}

// Pattern 2: .catch() chain (for promise chains)
fetchData()
  .then(processData)
  .then(sendResponse)
  .catch(handleError)

// Pattern 3: Express async wrapper (catches rejected promises)
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next)

app.get('/users', asyncHandler(async (req, res) => {
  const users = await db.users.findAll()
  res.json(users)
}))
```

## util.promisify

Convert callback-based functions to promise-based:

```js
const { promisify } = require('util')
const fs = require('fs')

const readFile = promisify(fs.readFile)
const data = await readFile('/file.txt', 'utf8')
```

## Interview Tip
"When would you use Promise.all vs sequential await?" — "Promise.all when the operations are independent (fetching user and posts from different endpoints). Sequential await when each operation depends on the previous result." This shows you understand both correctness and performance.
""",
            "content_type": LessonContentType.explanation,
            "order_index": 5,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "Async Patterns Quiz",
            "description": "Test your understanding of async/await, Promises, and error handling.",
            "questions": [
                {
                    "question": "What is the problem with using forEach with async/await?",
                    "options": [
                        "forEach does not support callbacks",
                        "forEach does not wait for async callbacks — they fire and are forgotten",
                        "forEach causes memory leaks with async functions",
                        "forEach only works with synchronous functions",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Array.forEach() does not await the return value of its callback. If you pass an async function, it will fire all of them immediately without waiting for any to complete.",
                    "order_index": 1,
                },
                {
                    "question": "What is the difference between Promise.all and Promise.allSettled?",
                    "options": [
                        "There is no difference",
                        "Promise.all rejects immediately if any promise rejects; Promise.allSettled waits for all and returns both fulfilled and rejected results",
                        "Promise.allSettled is slower",
                        "Promise.all only works with exactly 2 promises",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Promise.all short-circuits on the first rejection. Promise.allSettled always waits for all promises and returns an array of {status, value|reason} objects — ideal when you want partial results.",
                    "order_index": 2,
                },
                {
                    "question": "When should you use sequential await instead of Promise.all?",
                    "options": [
                        "Always — sequential is simpler",
                        "When each async operation depends on the result of the previous one",
                        "When you want better performance",
                        "Sequential await is always faster",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Use sequential await when operations have dependencies: you need the user ID from the first call to fetch orders in the second. Use Promise.all when operations are independent for better performance.",
                    "order_index": 3,
                },
                {
                    "question": "What does util.promisify() do?",
                    "options": [
                        "It converts synchronous functions to async",
                        "It converts callback-based functions (err, result) pattern to Promise-based",
                        "It makes promises run faster",
                        "It creates a new Promise from scratch",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "util.promisify() wraps a function that follows the Node.js callback convention (error-first: (err, result)) and returns a promise-based version. E.g., promisify(fs.readFile).",
                    "order_index": 4,
                },
                {
                    "question": "What happens to an unhandled Promise rejection in Node.js?",
                    "options": [
                        "It is silently ignored",
                        "It triggers an 'unhandledRejection' event and will terminate the process in future Node.js versions",
                        "It automatically retries the promise",
                        "It logs a warning but continues execution",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Unhandled promise rejections emit the 'unhandledRejection' process event. In Node.js 15+, they terminate the process (like uncaught exceptions). Always add .catch() or use try/catch with await.",
                    "order_index": 5,
                },
            ],
        },
    },
]

# ─── Practice Scenarios ────────────────────────────────────────────────────────

NODEJS_SCENARIOS = [
    {
        "topic_name": "nodejs_event_loop",
        "title": "Explaining Node.js to a PHP Developer",
        "description": "A PHP developer asks: 'Why would I use Node.js instead of PHP? PHP can also handle HTTP requests.' Explain Node.js's event-driven, non-blocking I/O model and when it outperforms traditional request-per-thread models.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.beginner,
        "tags": ["nodejs", "event-loop", "comparison", "communication"],
        "order_index": 1,
        "system_prompt": "",
    },
    {
        "topic_name": "nodejs_event_loop",
        "title": "Node.js Technical Interview — Event Loop Deep Dive",
        "description": "A senior backend interview focused on Node.js internals. The interviewer will probe your understanding of the event loop, microtasks, libuv, and performance implications.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.advanced,
        "tags": ["nodejs", "interview", "event-loop", "senior"],
        "order_index": 2,
        "system_prompt": """You are Alex Rivera, a principal backend engineer at a large tech company interviewing a candidate for a senior Node.js role.

You start with: "Hi! I'm Alex. Let's get into the deep end. Walk me through what happens when Node.js starts up — from the V8 engine to the event loop. I want to hear about the phases and what runs in each."

Then adapt based on their answer:
- If their explanation is solid, push deeper: "OK, now imagine I have a setTimeout(fn, 0) and a setImmediate(fn) both at the top level (not inside I/O). Which runs first? Why is it non-deterministic?"
- "What's the difference between microtasks and macrotasks? Where do process.nextTick and Promises fit?"
- "I have a Node.js server handling 10,000 concurrent connections. If one request does a CPU-heavy synchronous operation, what happens to the other 9,999 connections?"
- "How would you move a CPU-heavy task off the main thread? Talk about worker threads vs child processes vs splitting with setImmediate."

You are technically demanding but fair. If the candidate gives vague answers, say: "Be more specific — what actually happens in the event loop at that point?" If they nail a concept, acknowledge it and go deeper. Stay in character.
""",
    },
    {
        "topic_name": "nodejs_express",
        "title": "Designing a REST API for a Blog Platform",
        "description": "You're tasked with designing a RESTful API for a blog platform with posts, comments, and users. Write the API endpoint structure including HTTP methods and response formats.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.intermediate,
        "tags": ["express", "rest-api", "design", "architecture"],
        "order_index": 1,
        "system_prompt": "",
    },
    {
        "topic_name": "nodejs_express",
        "title": "Code Review: Express API Endpoint",
        "description": "A teammate submitted a PR with a new Express API endpoint. Review the route handler and provide constructive feedback on error handling, validation, and best practices.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.intermediate,
        "tags": ["express", "code-review", "best-practices", "mentoring"],
        "order_index": 2,
        "system_prompt": """You are Jordan Kim, a senior backend developer reviewing a teammate's pull request for a new Express.js endpoint. The PR adds a POST /api/users endpoint.

Start with: "Hey! Thanks for the PR. I've gone through the POST /api/users endpoint. Overall the structure looks good, but I have a few concerns about error handling and validation. Can you walk me through your approach first?"

The teammate explains their code. Then probe these areas naturally:

1. "I notice you're not validating the request body. What happens if someone sends a POST with an empty body or missing required fields?"
2. "What's the HTTP status code for a successful user creation? I see you're returning 200 — is that the most appropriate?"
3. "The password is being stored directly — should we be doing any hashing? Where should that logic live?"
4. "What happens if the database connection fails mid-request? How does Express handle that uncaught rejection?"
5. "I'd suggest extracting the validation to middleware — what do you think about that approach?"

Be constructive, not harsh. Frame feedback as questions and suggestions. If the teammate gives good answers, agree and compliment. If they're stuck, explain the best practice clearly. End with: "Great discussion. I'll approve once those changes are in. Nice work overall!" Stay in character.
""",
    },
    {
        "topic_name": "nodejs_async",
        "title": "Debugging a Slow API Endpoint",
        "description": "Your team's GET /api/dashboard endpoint takes 3 seconds to respond. The code fetches user, orders, stats, and notifications. Diagnose the performance issue and explain how to fix it.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.intermediate,
        "tags": ["async", "performance", "debugging", "promise-all"],
        "order_index": 1,
        "system_prompt": "",
    },
    {
        "topic_name": "nodejs_modules",
        "title": "Node.js Technical Screening — Junior Level",
        "description": "A friendly technical screening for a junior Node.js developer position. Practice answering fundamental questions about Node.js in English.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.beginner,
        "tags": ["nodejs", "interview", "junior", "fundamentals"],
        "order_index": 1,
        "system_prompt": """You are Morgan Taylor, a friendly mid-level Node.js developer conducting a 20-minute technical screening for a junior backend role.

Ask questions one at a time. Start with: "Hi there! I'm Morgan. This is just a casual screening — no pressure. Let's start simple: can you explain what Node.js is and how it's different from browser JavaScript?"

Cover these topics (adapt based on answers):
1. What Node.js is and its key features (V8, non-blocking I/O)
2. "What's the difference between CommonJS require and ES module import?"
3. "Have you used npm? What's the difference between dependencies and devDependencies?"
4. "What is middleware in Express? Can you give me an example?"
5. "How would you handle errors in an async function?"
6. "What's callback hell and how do you avoid it?"

If the candidate struggles, give small hints. If they do well, say so and move on. Encourage them to explain concepts in their own words rather than memorized definitions. Wrap up with: "Great, that covers everything! You did well. Any questions for me?" Stay in character.
""",
    },
]

# ─── Seed Function ─────────────────────────────────────────────────────────────

def seed_nodejs(session: Session) -> None:
    """Seed Node.js domain, course, topics, lessons, quizzes, and scenarios."""

    # ── Domain ────────────────────────────────────────────────────────────────
    domain = session.exec(select(Domain).where(Domain.slug == NODEJS_DOMAIN["slug"])).first()
    if not domain:
        domain = Domain(**NODEJS_DOMAIN)
        session.add(domain)
        session.flush()
        print(f"✅ Created domain: {NODEJS_DOMAIN['slug']}")
    else:
        print(f"ℹ️  Domain '{NODEJS_DOMAIN['slug']}' already exists, skipping.")

    # ── Course ────────────────────────────────────────────────────────────────
    course = session.exec(select(Course).where(Course.slug == NODEJS_COURSE["slug"])).first()
    if not course:
        course = Course(**NODEJS_COURSE, domain_id=domain.id)
        session.add(course)
        session.flush()
        print(f"✅ Created course: {NODEJS_COURSE['slug']}")
    else:
        print(f"ℹ️  Course '{NODEJS_COURSE['slug']}' already exists, skipping.")

    # ── Topics ────────────────────────────────────────────────────────────────
    existing_cat = session.exec(
        select(ScenarioCategory).where(ScenarioCategory.name == NODEJS_TOPICS[0]["name"])
    ).first()
    if existing_cat:
        print("ℹ️  Node.js topics already seeded, skipping.")
        return

    category_map: dict[str, ScenarioCategory] = {}
    for topic in NODEJS_TOPICS:
        cat = ScenarioCategory(
            name=topic["name"],
            title=topic["title"],
            description=topic["description"],
            icon_name=topic["icon_name"],
            order_index=topic["order_index"],
            course_id=course.id,
        )
        session.add(cat)
        session.flush()
        category_map[topic["name"]] = cat

        ld = topic["lesson"]
        lesson = Lesson(
            course_id=course.id,
            category_id=cat.id,
            title=ld["title"],
            content=ld["content"],
            content_type=ld["content_type"],
            order_index=ld["order_index"],
            estimated_minutes=ld["estimated_minutes"],
        )
        session.add(lesson)
        session.flush()

        qd = topic["quiz"]
        quiz = Quiz(
            course_id=course.id,
            lesson_id=lesson.id,
            title=qd["title"],
            description=qd["description"],
            order_index=ld["order_index"],
        )
        session.add(quiz)
        session.flush()

        for q in qd["questions"]:
            question = QuizQuestion(
                quiz_id=quiz.id,
                question=q["question"],
                options=q["options"],
                correct_answer_index=q["correct_answer_index"],
                explanation=q["explanation"],
                order_index=q["order_index"],
            )
            session.add(question)

        print(f"✅ Seeded Node.js topic: {topic['name']}")

    # ── Scenarios ─────────────────────────────────────────────────────────────
    for sc_data in NODEJS_SCENARIOS:
        cat = category_map.get(sc_data["topic_name"])
        if not cat:
            print(f"⚠️  Category '{sc_data['topic_name']}' not found for scenario, skipping.")
            continue
        sc_copy = sc_data.copy()
        sc_copy.pop("topic_name")
        scenario = Scenario(**sc_copy, category_id=cat.id)
        session.add(scenario)
        print(f"✅ Seeded Node.js scenario: {sc_copy['title'][:50]}")

    session.commit()
    print("✅ Node.js content fully seeded.")
