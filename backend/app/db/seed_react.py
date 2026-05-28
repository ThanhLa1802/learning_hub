"""
Seed file for React.js domain.
Creates domain, course, topics (lessons + quizzes), and practice scenarios.
"""
from sqlmodel import Session, select

from app.models.domain import Domain, Course
from app.models.lesson import Lesson, LessonContentType
from app.models.quiz import Quiz, QuizQuestion
from app.models.scenario import Difficulty, PracticeMode, Scenario, ScenarioCategory

# ─── Domain & Course ───────────────────────────────────────────────────────────

REACT_DOMAIN = {
    "slug": "react-js",
    "name": "React Development",
    "description": "Master React.js for modern frontend development — hooks, state management, performance optimization, and technical interviews.",
    "icon_name": "atom",
    "color": "cyan",
    "order_index": 3,
    "is_active": True,
}

REACT_COURSE = {
    "slug": "react-js-fundamentals",
    "name": "React JS Fundamentals",
    "description": "Core React concepts every frontend developer needs to know.",
    "order_index": 1,
    "is_active": True,
}

# ─── Topics (lessons + quizzes) ────────────────────────────────────────────────

REACT_TOPICS = [
    {
        "name": "react_hooks",
        "title": "React Hooks",
        "description": "Master useState, useEffect, useRef, and the rules of hooks.",
        "icon_name": "hook",
        "order_index": 1,
        "lesson": {
            "title": "React Hooks: useState, useEffect, and useRef",
            "content": """# React Hooks

Hooks let you use state and lifecycle features in functional components.

## useState

```tsx
const [count, setCount] = useState(0)
```

- State is **immutable** — always use the setter
- For objects: spread to avoid mutation `setUser({ ...user, name: 'Alice' })`
- Lazy initialization: `useState(() => expensiveCompute())`

## useEffect

```tsx
useEffect(() => {
  fetchData()
  return () => cleanup()
}, [dependency])
```

| Dependency Array | Behavior |
|-----------------|----------|
| Omitted | Runs after every render |
| `[]` | Runs once on mount |
| `[dep]` | Runs when `dep` changes |

**Common patterns:**
- Fetch data on mount: `useEffect(() => { fetch(...) }, [])`
- Subscribe/unsubscribe: return cleanup function
- Sync external system: DOM, timers, subscriptions

## useRef

```tsx
const inputRef = useRef<HTMLInputElement>(null)
// Access: inputRef.current?.focus()
```

- Accessing DOM elements
- Storing mutable values that **don't trigger re-render** (interval IDs, previous values)
- Persists across renders

## Rules of Hooks

1. **Only call hooks at the top level** — never inside loops, conditions, or nested functions
2. **Only call hooks from React components** or custom hooks
3. Hooks start with `use` by convention

## Interview Tip
"Why can't you call hooks conditionally?" — React tracks hooks by call order. If a hook is skipped in one render, the order shifts and state gets mismatched. The linter rule `react-hooks/rules-of-hooks` enforces this.""",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 10,
        },
        "quiz": {
            "title": "React Hooks Quiz",
            "description": "Test your understanding of core React hooks.",
            "questions": [
                {
                    "question": "What happens if you omit the dependency array in useEffect?",
                    "options": ["Effect runs once on mount", "Effect never runs", "Effect runs after every render", "Effect runs only when state changes"],
                    "correct_answer_index": 2,
                    "explanation": "Without a dependency array, useEffect runs after every single render — equivalent to componentDidMount + componentDidUpdate combined.",
                    "order_index": 1,
                },
                {
                    "question": "Which statement correctly updates a user object in state?",
                    "options": [
                        "user.name = 'Alice'",
                        "setUser({ ...user, name: 'Alice' })",
                        "setState(user.name = 'Alice')",
                        "setUser(user)",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "React state is immutable. Spread the existing object and override the changed field. Direct mutation won't trigger a re-render.",
                    "order_index": 2,
                },
                {
                    "question": "When would you use useRef instead of useState?",
                    "options": [
                        "When you need the component to re-render on change",
                        "To store a value that persists between renders but should NOT trigger a re-render",
                        "For derived state calculations",
                        "For async state updates",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "useRef stores a mutable value that persists across renders without causing re-renders — ideal for timers, DOM references, and tracking previous values.",
                    "order_index": 3,
                },
                {
                    "question": "Why is calling hooks inside an if-statement forbidden?",
                    "options": [
                        "Performance reasons",
                        "React tracks hooks by call order; skipping a hook shifts the order and corrupts state",
                        "Conditional hooks can't access context",
                        "The React compiler doesn't support it",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "React identifies hooks by their position in the call order. Conditionally skipping a hook causes all subsequent hooks to map to the wrong state slot.",
                    "order_index": 4,
                },
                {
                    "question": "What is the purpose of the cleanup function returned from useEffect?",
                    "options": [
                        "Reset state to initial value",
                        "Cancel pending fetches before component unmounts or effect re-runs",
                        "Clear the component's render output",
                        "Run before each re-render",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "The cleanup function runs before the next effect execution and on unmount. Use it to cancel subscriptions, clear timers, or abort fetch requests to prevent memory leaks.",
                    "order_index": 5,
                },
            ],
        },
    },
    {
        "name": "react_custom_hooks",
        "title": "Custom Hooks",
        "description": "Extract and reuse stateful logic across components with custom hooks.",
        "icon_name": "puzzle",
        "order_index": 2,
        "lesson": {
            "title": "Custom Hooks: Reusable Stateful Logic",
            "content": """# Custom Hooks

Custom hooks let you **extract stateful logic** from components into reusable functions.

## Why Custom Hooks?

Before hooks, sharing stateful logic required HOCs or render props — complex patterns. Custom hooks are simpler.

## Example: useFetch

```tsx
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    const controller = new AbortController()
    fetch(url, { signal: controller.signal })
      .then(res => res.json())
      .then(setData)
      .catch(err => { if (err.name !== 'AbortError') setError(err) })
      .finally(() => setLoading(false))
    return () => controller.abort()
  }, [url])

  return { data, loading, error }
}

// Usage
const { data, loading, error } = useFetch<User[]>('/api/users')
```

## Example: useLocalStorage

```tsx
function useLocalStorage<T>(key: string, initial: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key)
    return stored ? JSON.parse(stored) : initial
  })

  const setStored = (newValue: T) => {
    setValue(newValue)
    localStorage.setItem(key, JSON.stringify(newValue))
  }

  return [value, setStored] as const
}
```

## Example: useDebounce

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value)
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay)
    return () => clearTimeout(timer)
  }, [value, delay])
  return debounced
}
```

## Rules for Custom Hooks

1. Name must start with `use`
2. Can call other hooks inside
3. Each component using the hook gets **isolated state** — not shared
4. Share logic, not state

## Interview Tip
"Tell me about a custom hook you've written." Use useFetch as an example — it demonstrates useEffect, cleanup, AbortController, and TypeScript generics all at once.""",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 10,
        },
        "quiz": {
            "title": "Custom Hooks Quiz",
            "description": "Test your understanding of custom hooks patterns.",
            "questions": [
                {
                    "question": "What is the main purpose of a custom hook?",
                    "options": [
                        "To replace Redux",
                        "To extract and reuse stateful logic across multiple components",
                        "To create reusable UI components",
                        "To replace the Context API",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Custom hooks extract stateful logic (useState, useEffect, etc.) from components so it can be shared. They share logic, not state — each component gets its own state instance.",
                    "order_index": 1,
                },
                {
                    "question": "When two components use the same custom hook, do they share state?",
                    "options": [
                        "Yes, state is always shared in custom hooks",
                        "No, each component gets an isolated state instance",
                        "Only if the hook uses Context internally",
                        "Only if they are sibling components",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Custom hooks share logic, not state. Each component calling the hook gets its own independent state — just like calling useState twice gives two separate state variables.",
                    "order_index": 2,
                },
                {
                    "question": "Why use AbortController in a useFetch hook?",
                    "options": [
                        "To cancel the request if the URL is invalid",
                        "To cancel the in-flight fetch when the component unmounts or URL changes, preventing state updates on unmounted components",
                        "To retry failed requests automatically",
                        "AbortController is required for all fetch calls in React",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Without cleanup, a component unmounting mid-fetch would try to setState on an unmounted component. AbortController cancels the request in the useEffect cleanup function.",
                    "order_index": 3,
                },
                {
                    "question": "What must the name of a custom hook start with?",
                    "options": ["hook", "use", "get", "handle"],
                    "correct_answer_index": 1,
                    "explanation": "React enforces the 'use' prefix convention. The lint rule 'react-hooks/rules-of-hooks' only checks functions starting with 'use', so hooks inside non-'use' functions won't be validated.",
                    "order_index": 4,
                },
                {
                    "question": "What does the useDebounce hook prevent?",
                    "options": [
                        "Duplicate API requests on every keystroke",
                        "State mutation",
                        "Memory leaks from subscriptions",
                        "Re-renders of child components",
                    ],
                    "correct_answer_index": 0,
                    "explanation": "useDebounce delays updating the value until the user stops typing. This prevents an API call on every keystroke — only calling the API after the user pauses.",
                    "order_index": 5,
                },
            ],
        },
    },
    {
        "name": "react_state_management",
        "title": "State Management",
        "description": "Compare Context API, Zustand, and Redux for managing global state.",
        "icon_name": "database",
        "order_index": 3,
        "lesson": {
            "title": "State Management: Context, Zustand, and Redux",
            "content": """# React State Management

Choosing the right state management tool is critical for scalable React apps.

## When Does State Need to Be Global?

- Multiple components need the same data
- State needs to persist across route changes
- Complex shared mutations (shopping cart, auth, theme)

## Option 1: Context API + useReducer

Built-in. Good for low-frequency updates (theme, locale, auth).

```tsx
const CartContext = createContext<CartState | null>(null)

function CartProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(cartReducer, { items: [] })
  return (
    <CartContext.Provider value={{ state, dispatch }}>
      {children}
    </CartContext.Provider>
  )
}
```

**Problem**: Every Context consumer re-renders on any state change. Use multiple small contexts or `useMemo` for the value.

## Option 2: Zustand

Minimal boilerplate. No Provider needed. Selector-based re-renders.

```tsx
const useCartStore = create<CartStore>((set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) => set((state) => ({ items: state.items.filter(i => i.id !== id) })),
}))

// Usage — only re-renders when items changes
const items = useCartStore((state) => state.items)
```

## Option 3: Redux Toolkit

Industry standard for large teams. Strict patterns, DevTools, time-travel debugging.

```tsx
const cartSlice = createSlice({
  name: 'cart',
  initialState: { items: [] as CartItem[] },
  reducers: {
    addItem: (state, action) => { state.items.push(action.payload) },
    removeItem: (state, action) => {
      state.items = state.items.filter(i => i.id !== action.payload)
    },
  },
})
```

## Comparison

| | Context | Zustand | Redux Toolkit |
|---|---|---|---|
| Boilerplate | Low | Very Low | Medium |
| DevTools | No | Yes | Best |
| Re-render control | Manual | Selectors | Selectors |
| Team scale | Small | Small-Med | Large |

## Recommended Defaults

- **Auth / theme / locale**: Context API (changes rarely)
- **Feature state**: Zustand (simple, no boilerplate)
- **Large team / complex flows**: Redux Toolkit

## Interview Tip
"We chose Zustand over Redux because our app state is simple — a few stores for cart, auth, and filters. Redux's patterns are great for large teams but felt over-engineered for our 3-person team." This shows pragmatism.""",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "State Management Quiz",
            "description": "Test your knowledge of React state management options.",
            "questions": [
                {
                    "question": "What is the main performance issue with the Context API?",
                    "options": [
                        "Context is synchronous and blocks the event loop",
                        "All Context consumers re-render whenever any part of the context value changes",
                        "Context doesn't support TypeScript",
                        "Context values are not persisted across page reloads",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "When the Context value changes, every component consuming it re-renders — even if it only uses a slice of the value that didn't change. This is why Context works well for low-frequency updates.",
                    "order_index": 1,
                },
                {
                    "question": "What is Zustand's key advantage over Redux Toolkit?",
                    "options": [
                        "Better performance in all cases",
                        "Minimal boilerplate — no Provider, actions, or reducers needed",
                        "Better DevTools support",
                        "Required for Next.js",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Zustand requires no Provider wrapper and no separate action/reducer files. The entire store is defined in one create() call.",
                    "order_index": 2,
                },
                {
                    "question": "What is a selector in Zustand?",
                    "options": [
                        "A CSS selector for styling components",
                        "A function that extracts a slice of the store — component only re-renders when that slice changes",
                        "A way to combine multiple stores",
                        "A Redux-compatible adapter",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "With `useStore(state => state.items)`, the component only re-renders when `items` changes — not when other parts of the store update. This is more efficient than subscribing to the whole store.",
                    "order_index": 3,
                },
                {
                    "question": "When is Redux Toolkit the right choice?",
                    "options": [
                        "All React apps should use Redux Toolkit",
                        "For large teams needing strict patterns, time-travel debugging, and predictable state flows",
                        "When you need to avoid external dependencies",
                        "For state that rarely changes like theme or locale",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Redux Toolkit's strict patterns (slices, actions, reducers) and excellent DevTools shine in large teams. For small apps, the overhead may not be justified.",
                    "order_index": 4,
                },
                {
                    "question": "What state is best managed with Context API?",
                    "options": [
                        "A shopping cart with frequent add/remove operations",
                        "Authentication status, theme, and locale — values that change infrequently",
                        "Form state with real-time validation",
                        "Paginated list data with filters",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Context works well for low-frequency global state like auth, theme, and locale. For high-frequency updates like a cart, the re-render issue becomes a real problem.",
                    "order_index": 5,
                },
            ],
        },
    },
    {
        "name": "react_performance",
        "title": "Performance Optimization",
        "description": "Use React.memo, useMemo, useCallback, and code splitting to keep UIs fast.",
        "icon_name": "zap",
        "order_index": 4,
        "lesson": {
            "title": "React Performance: memo, useMemo, useCallback, and Lazy Loading",
            "content": """# React Performance Optimization

React re-renders a component whenever its state or props change. Understanding when this is a problem — and how to fix it — is critical.

## React.memo

Wraps a component. Skips re-render if props haven't changed (shallow comparison).

```tsx
const ProductCard = React.memo(({ product }: { product: Product }) => {
  return <div>{product.name}</div>
})
```

**When to use**: Pure components that receive the same props often — list items, cards.
**Don't overuse**: The comparison itself has a cost. Only use when you measure a problem.

## useMemo

Memoizes the result of an expensive calculation.

```tsx
const sortedProducts = useMemo(
  () => [...products].sort((a, b) => a.price - b.price),
  [products]
)
```

**When to use**: Expensive computations (sorting large lists, heavy transforms).
**Don't use for**: Simple calculations — the overhead isn't worth it.

## useCallback

Memoizes a function reference. Prevents child re-renders when passing callbacks as props.

```tsx
const handleDelete = useCallback((id: string) => {
  setItems(prev => prev.filter(item => item.id !== id))
}, []) // setItems from useState is stable

// Pass to a memoized child
<ProductList onDelete={handleDelete} />
```

**Why it matters**: A function defined in a component body is a new reference each render. If passed to `React.memo` child, it triggers a re-render anyway.

## Code Splitting with lazy()

```tsx
const HeavyChart = lazy(() => import('./HeavyChart'))

function Dashboard() {
  return (
    <Suspense fallback={<Skeleton />}>
      <HeavyChart />
    </Suspense>
  )
}
```

Loads `HeavyChart` only when `Dashboard` renders — reduces initial bundle size.

## Virtualization

For long lists (1000+ items), render only visible rows:
```tsx
import { FixedSizeList } from 'react-window'
```

## Profiling

Use React DevTools Profiler to find actual bottlenecks before optimizing.

## Interview Tip
"I profile first. `useMemo` and `useCallback` have their own overhead — adding them blindly can make performance worse. I use React DevTools Profiler to identify expensive components, then apply targeted optimization." This shows maturity.""",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "React Performance Quiz",
            "description": "Test your understanding of React performance optimizations.",
            "questions": [
                {
                    "question": "What does React.memo do?",
                    "options": [
                        "Memoizes the result of an expensive function",
                        "Wraps a component and skips re-render if props haven't changed",
                        "Stores component state between route changes",
                        "Prevents all child re-renders unconditionally",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "React.memo does a shallow comparison of props. If props are equal, it skips re-rendering the component. It doesn't memoize computed values — that's useMemo.",
                    "order_index": 1,
                },
                {
                    "question": "Why do you need useCallback when passing a handler to a React.memo child?",
                    "options": [
                        "Functions can't be passed as props without useCallback",
                        "Without useCallback, a new function reference is created each render, causing the memoized child to re-render anyway",
                        "useCallback makes the function faster",
                        "React.memo ignores function props by default",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Functions defined in a component body are new references every render. React.memo sees a new prop (even with same logic) and re-renders. useCallback returns the same reference when deps don't change.",
                    "order_index": 2,
                },
                {
                    "question": "When should you use useMemo?",
                    "options": [
                        "For every computed value in a component",
                        "For expensive computations that would be slow to recalculate on every render",
                        "Instead of useState for better performance",
                        "Always — it makes React faster",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "useMemo has overhead from the comparison check itself. Only use it for genuinely expensive computations (large sort, heavy filter). For simple operations, direct calculation is faster.",
                    "order_index": 3,
                },
                {
                    "question": "What is the benefit of React.lazy() and Suspense?",
                    "options": [
                        "Makes components load lazily based on user scrolling",
                        "Splits code so heavy components are only downloaded when they're first rendered",
                        "Suspends rendering until all data is fetched",
                        "Caches component output between route changes",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "React.lazy() enables code splitting — the component's code is put in a separate bundle that only downloads when that component is first rendered, reducing initial load time.",
                    "order_index": 4,
                },
                {
                    "question": "What is the correct approach to React performance optimization?",
                    "options": [
                        "Add React.memo, useMemo, and useCallback everywhere proactively",
                        "Profile first with React DevTools to identify actual bottlenecks, then apply targeted fixes",
                        "Replace all state with Redux for better performance",
                        "Avoid using hooks in components that re-render frequently",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Premature optimization adds code complexity with no benefit — useMemo/useCallback have their own overhead. Profile first, identify real bottlenecks, then optimize those specific components.",
                    "order_index": 5,
                },
            ],
        },
    },
    {
        "name": "react_component_patterns",
        "title": "Component Patterns",
        "description": "Compound components, render props, and composition patterns for scalable UI.",
        "icon_name": "layers",
        "order_index": 5,
        "lesson": {
            "title": "React Component Patterns: Composition and Flexibility",
            "content": """# React Component Patterns

Well-designed component APIs are as important as well-designed code architecture.

## Composition over Inheritance

React embraces composition. Pass components as children or props instead of extending.

```tsx
// Flexible Card component
function Card({ children, className }: CardProps) {
  return <div className={`card ${className}`}>{children}</div>
}

function Card.Header({ children }: { children: ReactNode }) {
  return <div className="card-header">{children}</div>
}

// Usage
<Card>
  <Card.Header>Title</Card.Header>
  <p>Content</p>
</Card>
```

## Compound Components

Components that work together, sharing implicit state via Context.

```tsx
const AccordionContext = createContext<AccordionCtx | null>(null)

function Accordion({ children }: { children: ReactNode }) {
  const [open, setOpen] = useState<string | null>(null)
  return (
    <AccordionContext.Provider value={{ open, setOpen }}>
      {children}
    </AccordionContext.Provider>
  )
}

function Accordion.Item({ id, title, children }: ItemProps) {
  const { open, setOpen } = useContext(AccordionContext)!
  return (
    <div>
      <button onClick={() => setOpen(open === id ? null : id)}>{title}</button>
      {open === id && <div>{children}</div>}
    </div>
  )
}
```

## Render Props

Pass a function as a prop to share dynamic render logic.

```tsx
function MouseTracker({ render }: { render: (pos: Position) => ReactNode }) {
  const [pos, setPos] = useState({ x: 0, y: 0 })
  return (
    <div onMouseMove={e => setPos({ x: e.clientX, y: e.clientY })}>
      {render(pos)}
    </div>
  )
}

<MouseTracker render={pos => <span>{pos.x}, {pos.y}</span>} />
```

> Note: custom hooks largely replaced render props for logic sharing.

## Controlled vs Uncontrolled Components

- **Controlled**: Form value lives in React state. Source of truth = React.
- **Uncontrolled**: Form value lives in the DOM. Access via `ref`.

```tsx
// Controlled
<input value={name} onChange={e => setName(e.target.value)} />

// Uncontrolled
const inputRef = useRef<HTMLInputElement>(null)
<input ref={inputRef} defaultValue="initial" />
```

## Polymorphic Components (as prop)

```tsx
function Button<T extends ElementType = 'button'>({
  as,
  children,
  ...props
}: PolymorphicProps<T>) {
  const Component = as ?? 'button'
  return <Component {...props}>{children}</Component>
}

<Button as="a" href="/home">Go Home</Button>
<Button onClick={handleClick}>Submit</Button>
```

## Interview Tip
"We refactored our form components from render props to custom hooks — the logic became more readable and testable. But we kept compound components for our UI library (Tabs, Accordion) because they provide a better consumer API." """,
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "Component Patterns Quiz",
            "description": "Test your understanding of React component design patterns.",
            "questions": [
                {
                    "question": "What is the key benefit of compound components?",
                    "options": [
                        "They render faster than regular components",
                        "Multiple related components share implicit state via Context, giving consumers a flexible declarative API",
                        "They eliminate the need for props",
                        "They automatically handle accessibility",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Compound components (like Accordion + Accordion.Item) share state via Context internally. Consumers get a clean declarative API without managing the shared state themselves.",
                    "order_index": 1,
                },
                {
                    "question": "What replaced render props for sharing stateful logic?",
                    "options": [
                        "HOCs (Higher-Order Components)",
                        "Redux",
                        "Custom hooks",
                        "Context API",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "Custom hooks (introduced in React 16.8) replaced render props for sharing logic. They're more readable, don't add DOM nesting, and work well with TypeScript.",
                    "order_index": 2,
                },
                {
                    "question": "What is a controlled component?",
                    "options": [
                        "A component that controls its parent",
                        "A form element whose value is controlled by React state",
                        "A component wrapped in React.memo",
                        "A component that uses useImperativeHandle",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "In a controlled component, the form element's value is always driven by React state. Every change goes through an onChange handler that updates state.",
                    "order_index": 3,
                },
                {
                    "question": "What does the 'as' prop pattern allow?",
                    "options": [
                        "Rename the component",
                        "Render the component as a different HTML element or another component while keeping the same styling/behavior",
                        "Access the component's internal state",
                        "Conditionally render the component",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "The polymorphic 'as' prop lets one component render as different elements. A Button can render as <button> or <a> depending on context while sharing the same design.",
                    "order_index": 4,
                },
                {
                    "question": "Why does React prefer composition over inheritance?",
                    "options": [
                        "JavaScript doesn't support class inheritance",
                        "Composition gives more flexibility — behavior is assembled from pieces rather than locked in a rigid hierarchy",
                        "Inherited components can't use hooks",
                        "React class components are deprecated",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Inheritance creates tight coupling. Composition (passing children, components as props) is more flexible and aligns with React's declarative model.",
                    "order_index": 5,
                },
            ],
        },
    },
    {
        "name": "react_data_fetching",
        "title": "Data Fetching & Server State",
        "description": "Manage server state efficiently with React Query / TanStack Query.",
        "icon_name": "cloud-download",
        "order_index": 6,
        "lesson": {
            "title": "Data Fetching: React Query and Server State",
            "content": """# Data Fetching in React

"Server state" (data from an API) has different needs than "client state" (UI state). Libraries like TanStack Query solve these specifically.

## The Problem with useEffect Fetching

```tsx
// Manual approach — what you have to manage yourself:
const [data, setData] = useState(null)
const [loading, setLoading] = useState(true)
const [error, setError] = useState(null)
// + caching, deduplication, refetch on focus, stale data, pagination...
```

Every app ends up reinventing the same wheel.

## TanStack Query (React Query)

```tsx
// Setup
const queryClient = new QueryClient()

// Fetch
const { data, isLoading, error } = useQuery({
  queryKey: ['products', filters],
  queryFn: () => fetchProducts(filters),
  staleTime: 5 * 60 * 1000, // 5 min — don't refetch if fresh
})

// Mutate
const mutation = useMutation({
  mutationFn: createProduct,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['products'] })
  },
})
```

## What React Query Gives You For Free

- **Caching**: Same queryKey = same cached data
- **Deduplication**: Multiple components requesting same key = one network call
- **Background refetch**: Refetches stale data when window regains focus
- **Optimistic updates**: Update UI before server confirms, rollback on failure
- **Pagination / infinite scroll**: `useInfiniteQuery`
- **DevTools**: Visual cache inspector

## Query Keys

Keys determine cache identity. Make them specific enough:

```tsx
['users']                    // all users
['users', userId]            // one user
['users', userId, 'posts']   // user's posts
['products', { page, sort }] // paginated products
```

## Optimistic Updates

```tsx
useMutation({
  mutationFn: toggleLike,
  onMutate: async (postId) => {
    await queryClient.cancelQueries({ queryKey: ['posts'] })
    const previous = queryClient.getQueryData(['posts'])
    queryClient.setQueryData(['posts'], old => old.map(p =>
      p.id === postId ? { ...p, liked: !p.liked } : p
    ))
    return { previous }
  },
  onError: (_, __, context) => {
    queryClient.setQueryData(['posts'], context.previous)
  },
})
```

## SWR (Alternative)

Simpler API by Vercel. `stale-while-revalidate` strategy: return cached (stale) data immediately, refetch in background.

```tsx
const { data, error } = useSWR('/api/user', fetcher)
```

## Interview Tip
"We replaced our custom useEffect data-fetching hooks with TanStack Query. We got caching, deduplication, and background refresh out of the box, and deleted ~300 lines of boilerplate." """,
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "Data Fetching Quiz",
            "description": "Test your knowledge of React data fetching patterns.",
            "questions": [
                {
                    "question": "What is the main benefit of TanStack Query's query key system?",
                    "options": [
                        "Keys must match API endpoint URLs",
                        "The same key maps to the same cached response — multiple components requesting the same key share one cached result",
                        "Keys encrypt the request for security",
                        "Keys are used to paginate API responses",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Query keys are cache identifiers. Components with the same queryKey share the cache — if ProductList and ProductCount both use ['products'], only one network request is made.",
                    "order_index": 1,
                },
                {
                    "question": "What does staleTime control in React Query?",
                    "options": [
                        "How long to wait before showing loading state",
                        "How long cached data is considered fresh before a background refetch is triggered",
                        "Maximum age of the cache before eviction",
                        "Timeout for the fetch request",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "staleTime tells React Query how long fetched data is 'fresh'. During this window, it won't refetch. After it expires, data is still served from cache but refetched in the background.",
                    "order_index": 2,
                },
                {
                    "question": "What is an optimistic update?",
                    "options": [
                        "Assuming the server is always available",
                        "Updating the UI immediately before the server confirms, rolling back on failure",
                        "Prefetching data before the user navigates",
                        "Using optimistic locking in the database",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Optimistic updates immediately show the expected result (e.g., liked post) while the server request is in-flight. If the server fails, rollback to the previous state. Makes UIs feel instant.",
                    "order_index": 3,
                },
                {
                    "question": "Why call queryClient.invalidateQueries() after a mutation?",
                    "options": [
                        "To delete the cache permanently",
                        "To mark related queries as stale so they refetch and reflect the mutation",
                        "To prevent duplicate mutations",
                        "To update the query key",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "After creating a product, the products list cache is stale. invalidateQueries marks it as stale and triggers a background refetch to show the new data.",
                    "order_index": 4,
                },
                {
                    "question": "What problem does React Query solve compared to manual useEffect fetching?",
                    "options": [
                        "It makes fetch requests faster",
                        "It eliminates the need for loading states",
                        "It provides caching, deduplication, background refetch, and server state sync that you'd otherwise build manually",
                        "It replaces all useState hooks",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "Manual useEffect fetching requires you to implement caching, deduplication, refetch on focus, stale management, pagination, and error handling yourself. React Query provides all of this.",
                    "order_index": 5,
                },
            ],
        },
    },
    {
        "name": "react_interview_english",
        "title": "React Interview English",
        "description": "Communicate React concepts clearly in technical interviews — vocabulary, explanations, and trade-off language.",
        "icon_name": "message-square",
        "order_index": 7,
        "lesson": {
            "title": "React Interview English: Explaining Concepts and Trade-offs",
            "content": """# React Technical Interview English

Technical React interviews test both your knowledge and your ability to explain it clearly. Here's the vocabulary and patterns you need.

## Explaining the Virtual DOM

> "React uses a **virtual DOM** — an in-memory representation of the real DOM. When state changes, React **diffs** the new virtual DOM against the previous one and applies only the **minimal set of changes** to the real DOM. This **batches** DOM operations and avoids expensive full re-renders."

## Explaining the Reconciliation Algorithm

> "React's reconciler determines what changed between renders. It uses a **heuristic O(n) algorithm** — it assumes components of different types produce different trees, and elements at the same position with the same **key** are the same element. This is why stable keys in lists are critical — using array indexes as keys can cause **incorrect reuse** of component state."

## Explaining useEffect Cleanup

> "The cleanup function returned from useEffect runs before the next effect and on unmount. Without it, you risk **memory leaks** — an event listener keeps holding a reference to a component that was removed from the DOM."

## Trade-off Language for React

| Situation | Professional Phrase |
|-----------|---------------------|
| Chose Zustand over Redux | "Redux's patterns are great for large teams but were **over-engineered** for our use case." |
| Avoided Context for frequent state | "Context causes **wholesale re-renders** of all consumers — for high-frequency updates like a cart, Zustand's selector-based updates are more performant." |
| Chose controlled inputs | "We use controlled inputs so form validation logic has **a single source of truth** in React state." |
| Added React.memo | "We profiled with DevTools first and found this list was the **rendering bottleneck** — React.memo eliminated **unnecessary re-renders** of unchanged items." |

## Answering "How would you optimize this?"

Structure:
1. **Profile first** — "I'd start with the React DevTools Profiler to find which components are re-rendering unnecessarily."
2. **Identify the cause** — "In this case it looks like every render creates a new function reference for the onDelete prop."
3. **Apply targeted fix** — "useCallback would stabilize the reference. Combined with React.memo on the list item component, we'd eliminate those re-renders."
4. **Measure after** — "I'd then re-profile to confirm the improvement."

## Answering "What's your biggest React mistake?"

> "Early on I overused useEffect — I'd put side effects everywhere, including derived state calculations. I learned to compute derived values directly in the render function and reserve useEffect only for synchronizing with external systems. The code became much more predictable."

## Interview Tip
In React interviews, always show you understand **why** — why virtual DOM is faster, why keys matter, why hooks have rules. Interviewers want depth, not just API knowledge.""",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 11,
        },
        "quiz": {
            "title": "React Interview English Quiz",
            "description": "Test your ability to explain React concepts in professional English.",
            "questions": [
                {
                    "question": "Which explanation of the Virtual DOM is most professional?",
                    "options": [
                        "It's a fake DOM that React uses.",
                        "React keeps a copy of the DOM.",
                        "React maintains an in-memory representation of the DOM, diffs it against the previous version, and applies only the minimal set of real DOM changes.",
                        "The virtual DOM makes React faster than other frameworks.",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "Strong explanations name the mechanism (in-memory representation), the process (diffing), and the benefit (minimal DOM changes). Avoid vague statements like 'fake DOM'.",
                    "order_index": 1,
                },
                {
                    "question": "Why are stable keys important in React lists?",
                    "options": [
                        "Keys make rendering faster by 10x.",
                        "Using unstable keys (like array indexes) causes React to incorrectly reuse component state when items are reordered or deleted.",
                        "React requires keys for accessibility.",
                        "Keys prevent unnecessary API calls.",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "React's reconciler uses keys to identify which elements changed. If you use array indexes, reordering list items makes React think they're the same element — leading to state corruption.",
                    "order_index": 2,
                },
                {
                    "question": "What phrase correctly explains why you chose Zustand over Redux?",
                    "options": [
                        "Redux is too complicated.",
                        "Zustand is newer.",
                        "Redux's strict patterns are valuable for large teams, but for our 3-person team they added boilerplate without proportional benefit.",
                        "We didn't know Redux.",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "Good trade-off language acknowledges the alternative's strengths ('valuable for large teams') before explaining why it wasn't right for the situation. This shows balanced judgment.",
                    "order_index": 3,
                },
                {
                    "question": "What is the correct first step when asked to optimize a React app?",
                    "options": [
                        "Add React.memo to every component",
                        "Replace useState with Redux",
                        "Profile with React DevTools to identify which components are rendering unnecessarily",
                        "Add useMemo to all computed values",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "Always measure before optimizing. The DevTools Profiler shows exactly which components re-render, how long they take, and why. Optimizing without profiling is guesswork.",
                    "order_index": 4,
                },
                {
                    "question": "What is a 'memory leak' in React context?",
                    "options": [
                        "Using too much useState",
                        "A component consuming more memory than expected",
                        "An async callback or subscription referencing a component that has been unmounted from the DOM",
                        "Re-rendering too frequently",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "Memory leaks in React happen when cleanup isn't done — event listeners, subscriptions, or async callbacks hold references to unmounted components, preventing garbage collection.",
                    "order_index": 5,
                },
            ],
        },
    },
]

# ─── Practice Scenarios ────────────────────────────────────────────────────────

REACT_SCENARIOS = [
    {
        "topic_name": "react_hooks",
        "title": "Junior React Developer Interview",
        "description": "Practice a friendly technical screening for a junior React developer role. The interviewer covers React fundamentals, hooks, and basic component design.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.beginner,
        "tags": ["react", "interview", "junior", "hooks"],
        "order_index": 10,
        "system_prompt": """You are Jamie Park, a friendly senior React developer conducting a 20-minute technical screening for a junior React developer role at a product startup.

Ask questions one at a time. Start with: "Hi! I'm Jamie. Thanks for joining — let's keep this conversational. Can you start by telling me how long you've been working with React and what kind of projects you've built?"

Cover these topics in order (adapt based on answers):
1. Project background and general React experience
2. "What's the difference between props and state?"
3. "Can you explain what useEffect does and when you'd use it?"
4. "What is the virtual DOM and why does it matter?"
5. "Have you worked with any state management tools — like Redux or Zustand?"
6. A simple scenario: "You have a component that fetches a list of users on page load and shows a loading spinner. How would you structure that?"

After each answer, give brief, encouraging feedback. If the candidate struggles, give a gentle hint. If they do well, say so. Keep the tone warm. Wrap up with: "Great, that's all from me! Do you have any questions?" Stay in character.""",
    },
    {
        "topic_name": "react_state_management",
        "title": "Senior React Developer Interview",
        "description": "A rigorous technical interview for a senior React role. Topics include performance, architecture, state management, and system design for frontend.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.advanced,
        "tags": ["react", "interview", "senior", "advanced"],
        "order_index": 10,
        "system_prompt": """You are Alex Chen, a principal frontend engineer conducting a senior React developer interview at a scale-up. You are technically demanding and probe for depth.

Start with: "Welcome. I'm Alex. Let's dive straight in — walk me through how you'd design the frontend architecture for a large e-commerce platform: product catalog, cart, checkout, and user dashboard. What are your key decisions?"

Then probe based on their answers:
1. Component architecture — how do they structure large apps? Feature folders vs type folders?
2. State management — what goes in server state (React Query) vs client state (Zustand/Redux)? Why?
3. Performance — "This product list has 500 items and re-renders on every keystroke in the search box. How do you fix it?"
4. React Query — "You have a mutation that adds an item to cart. How do you keep the cart UI in sync?"
5. Code splitting — "Your bundle is 2MB. What's your strategy?"
6. Testing — "How do you test a component that fetches data and renders based on loading/error/success states?"

Ask "Why?" and "What are the trade-offs?" frequently. If answers are vague, push back: "Be more specific." Stay in character as a demanding but fair interviewer.""",
    },
    {
        "topic_name": "react_component_patterns",
        "title": "React Component Library Design",
        "description": "You're proposing a design for a shared internal React component library. Practice explaining component API decisions to your tech lead.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.intermediate,
        "tags": ["react", "components", "design", "api"],
        "order_index": 11,
        "system_prompt": """You are Taylor, a tech lead reviewing a colleague's proposal for a shared internal React component library.

Start with: "Hi! I've seen your component library proposal. Before we greenlight it, I want to understand your design decisions better. Start with the Button component — walk me through its API."

Ask these questions naturally:
1. "Why did you choose compound components for the Modal instead of a simple open/close prop?"
2. "How are you handling the polymorphic 'as' prop — what's the TypeScript type signature?"
3. "The Form component uses controlled inputs. What's your reasoning over uncontrolled?"
4. "How will consumers style these components? CSS modules, CSS-in-JS, or className overrides?"
5. "What's your versioning strategy — if we have 5 teams using v1, how do we roll out breaking changes?"
6. "How would you test that the Accordion compound component works correctly?"

Be genuinely curious. Ask follow-ups. Occasionally push back: "That would break consumers who..." Stay in character as an experienced tech lead.""",
    },
    {
        "topic_name": "react_performance",
        "title": "React Performance Debugging Session",
        "description": "Your team's React dashboard is lagging. Debug the performance issues with your senior colleague.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.advanced,
        "tags": ["react", "performance", "debugging", "profiling"],
        "order_index": 12,
        "system_prompt": """You are Sam Rivera, a senior React engineer. You've been asked to debug a performance issue in the team's analytics dashboard. The user (the other engineer) needs to investigate with you.

Start with: "Hey, thanks for jumping on this. So the dashboard is seriously laggy — typing in the search box feels like 500ms delay, and switching between tabs takes 2+ seconds. I've already opened React DevTools Profiler. Before I show you the flame graph, what would you look for first?"

Guide the debugging session:
- If they suggest profiling correctly: show them findings: "The ProductTable component (with 200 rows) re-renders every keystroke in the search box."
- Ask about the root cause: "Why would the table re-render on search keystrokes?"
- Lead them to the solution: useDebounce for search + React.memo for table rows + useCallback for the sort handler
- If they propose unnecessary solutions: "Would that actually fix the re-render cause?"
- After each fix: "What would you measure to confirm the improvement?"

Be collaborative, not lecturing. The goal is to pair program and debug together. Stay in character.""",
    },
]


# ─── Seed Function ─────────────────────────────────────────────────────────────

def seed_react(session: Session) -> None:
    """Seed React.js domain, course, topics, lessons, quizzes, and scenarios."""

    # ── Domain ────────────────────────────────────────────────────────────────
    domain = session.exec(select(Domain).where(Domain.slug == REACT_DOMAIN["slug"])).first()
    if not domain:
        domain = Domain(**REACT_DOMAIN)
        session.add(domain)
        session.flush()
        print(f"✅ Created domain: {REACT_DOMAIN['slug']}")
    else:
        print(f"ℹ️  Domain '{REACT_DOMAIN['slug']}' already exists, skipping.")

    # ── Course ────────────────────────────────────────────────────────────────
    course = session.exec(select(Course).where(Course.slug == REACT_COURSE["slug"])).first()
    if not course:
        course = Course(**REACT_COURSE, domain_id=domain.id)
        session.add(course)
        session.flush()
        print(f"✅ Created course: {REACT_COURSE['slug']}")
    else:
        print(f"ℹ️  Course '{REACT_COURSE['slug']}' already exists, skipping.")

    # ── Topics ────────────────────────────────────────────────────────────────
    existing_cat = session.exec(
        select(ScenarioCategory).where(ScenarioCategory.name == REACT_TOPICS[0]["name"])
    ).first()
    if existing_cat:
        print("ℹ️  React topics already seeded, skipping.")
        return

    category_map: dict[str, ScenarioCategory] = {}
    for topic in REACT_TOPICS:
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

        print(f"✅ Seeded React topic: {topic['name']}")

    # ── Scenarios ─────────────────────────────────────────────────────────────
    for sc_data in REACT_SCENARIOS:
        cat = category_map.get(sc_data["topic_name"])
        if not cat:
            print(f"⚠️  Category '{sc_data['topic_name']}' not found for scenario, skipping.")
            continue
        sc_copy = sc_data.copy()
        sc_copy.pop("topic_name")
        scenario = Scenario(**sc_copy, category_id=cat.id)
        session.add(scenario)
        print(f"✅ Seeded React scenario: {sc_copy['title'][:50]}")

    session.commit()
    print("✅ React.js content fully seeded.")
