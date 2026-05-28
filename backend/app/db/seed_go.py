"""
Seed file for Go Programming Language domain.
Creates domain, course, topics (lessons + quizzes), and practice scenarios.
"""
from sqlmodel import Session, select

from app.models.domain import Domain, Course
from app.models.lesson import Lesson, LessonContentType
from app.models.quiz import Quiz, QuizQuestion
from app.models.scenario import Difficulty, PracticeMode, Scenario, ScenarioCategory

# ─── Domain & Course ───────────────────────────────────────────────────────────

GO_DOMAIN = {
    "slug": "go-programming",
    "name": "Go Programming",
    "description": "Learn Go (Golang) from the ground up — syntax, concurrency with goroutines, error handling, interfaces, and building real-world backend services.",
    "icon_name": "zap",
    "color": "blue",
    "order_index": 4,
    "is_active": True,
}

GO_COURSE = {
    "slug": "go-programming-fundamentals",
    "name": "Go Programming Fundamentals",
    "description": "Core Go concepts every backend developer needs to know — from syntax basics to concurrency patterns.",
    "order_index": 1,
    "is_active": True,
}

# ─── Topics ────────────────────────────────────────────────────────────────────

GO_TOPICS = [
    # ── Topic 1: Go Basics ────────────────────────────────────────────────────
    {
        "name": "go_basics",
        "title": "Go Basics & Syntax",
        "description": "Learn Go packages, variables, types, functions, and control flow — the foundation of every Go program.",
        "icon_name": "code",
        "order_index": 1,
        "lesson": {
            "title": "Go Basics: Variables, Types, and Functions",
            "content": """# Go Basics & Syntax

Go is a statically typed, compiled language designed for simplicity and performance.

## Hello World

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

Every Go file starts with a `package` declaration. The `main` package is the entry point.

## Variables

Go has three ways to declare variables:

```go
// 1. var keyword (explicit type)
var name string = "Alice"
var age int = 30

// 2. var with type inference
var city = "Hanoi"

// 3. Short declaration (inside functions only)
score := 95
```

**Key rule:** `:=` only works inside functions. Use `var` at package level.

## Basic Types

| Type | Examples | Zero Value |
|------|----------|------------|
| `int`, `int64` | `42`, `-7` | `0` |
| `float64` | `3.14` | `0.0` |
| `string` | `"hello"` | `""` |
| `bool` | `true`, `false` | `false` |
| `byte` | `'A'` (alias for uint8) | `0` |

```go
var count int = 10
var price float64 = 9.99
var message string = "Go is great"
var isActive bool = true
```

## Constants

```go
const Pi = 3.14159
const MaxRetries = 3

// iota for enums
type Direction int
const (
    North Direction = iota // 0
    East                   // 1
    South                  // 2
    West                   // 3
)
```

## Functions

```go
// Basic function
func add(a int, b int) int {
    return a + b
}

// Multiple return values (very common in Go!)
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("cannot divide by zero")
    }
    return a / b, nil
}

// Named return values
func minMax(nums []int) (min, max int) {
    min, max = nums[0], nums[0]
    for _, n := range nums {
        if n < min { min = n }
        if n > max { max = n }
    }
    return // "naked return" - returns named values
}
```

## Control Flow

```go
// if / else (no parentheses!)
if score >= 90 {
    fmt.Println("A grade")
} else if score >= 80 {
    fmt.Println("B grade")
} else {
    fmt.Println("Try harder")
}

// if with initializer
if err := doSomething(); err != nil {
    fmt.Println("Error:", err)
}

// for (the only loop in Go)
for i := 0; i < 5; i++ {
    fmt.Println(i)
}

// while-style for
for count > 0 {
    count--
}

// range over slice
fruits := []string{"apple", "banana", "mango"}
for index, fruit := range fruits {
    fmt.Printf("%d: %s\\n", index, fruit)
}

// switch
switch day {
case "Monday", "Tuesday":
    fmt.Println("Start of week")
case "Friday":
    fmt.Println("Almost weekend!")
default:
    fmt.Println("Midweek")
}
```

## Packages and Imports

```go
import (
    "fmt"      // formatted I/O
    "math"     // math functions
    "strings"  // string utilities
    "strconv"  // string conversions
)

// Only exported names start with uppercase
fmt.Println(math.Sqrt(16))   // ✅ exported
// math.sqrt(16)              // ❌ not exported
```

## Interview Tip
Go uses **capitalization** for access control — uppercase = exported (public), lowercase = unexported (private). There are no `public`/`private` keywords.""",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "Go Basics Quiz",
            "description": "Test your understanding of Go syntax fundamentals.",
            "questions": [
                {
                    "question": "Which of the following correctly declares a variable in Go inside a function?",
                    "options": [
                        "int count = 10",
                        "count := 10",
                        "let count = 10",
                        "declare count int = 10",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "The short variable declaration `:=` is the idiomatic Go way to declare and initialize a variable inside a function. `int count = 10` is C-style syntax and invalid in Go.",
                    "order_index": 1,
                },
                {
                    "question": "What is the zero value of a `string` in Go?",
                    "options": ["null", "nil", '""', "undefined"],
                    "correct_answer_index": 2,
                    "explanation": 'In Go, all variables have a zero value. For strings, it is an empty string `""`. Go never has uninitialized variables.',
                    "order_index": 2,
                },
                {
                    "question": "How does Go handle multiple return values from a function?",
                    "options": [
                        "Using an array",
                        "Using a struct",
                        "Go functions can natively return multiple values listed in parentheses",
                        "Using a pointer argument",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "Go supports multiple return values natively: `func divide(a, b float64) (float64, error)`. This is commonly used to return a result and an error together.",
                    "order_index": 3,
                },
                {
                    "question": "What makes a name exported (public) in Go?",
                    "options": [
                        "Using the `export` keyword",
                        "Adding `public` modifier",
                        "Starting the name with an uppercase letter",
                        "Declaring it at the package level",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "In Go, any identifier (function, type, variable) starting with an uppercase letter is exported and accessible from other packages. Lowercase means unexported (package-private).",
                    "order_index": 4,
                },
                {
                    "question": "Which loop construct does Go use?",
                    "options": [
                        "for, while, and do-while",
                        "Only while",
                        "Only for (used as for, while, and infinite loop)",
                        "foreach and for",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "Go has only one loop keyword: `for`. It covers traditional for loops, while-style loops (`for condition {}`), and infinite loops (`for {}`). Range-based iteration uses `for i, v := range slice`.",
                    "order_index": 5,
                },
            ],
        },
    },

    # ── Topic 2: Slices & Maps ─────────────────────────────────────────────────
    {
        "name": "go_slices_maps",
        "title": "Slices & Maps",
        "description": "Master Go's most-used data structures — dynamic slices and hash maps — with practical patterns.",
        "icon_name": "layers",
        "order_index": 2,
        "lesson": {
            "title": "Slices & Maps: Go's Core Data Structures",
            "content": """# Slices & Maps

Go provides two powerful built-in collection types: **slices** (dynamic arrays) and **maps** (hash tables).

## Slices

A slice is a flexible view into an underlying array.

```go
// Create slices
nums := []int{1, 2, 3, 4, 5}     // slice literal
empty := make([]int, 0)            // empty slice
sized := make([]int, 5)            // length 5, zero-filled
withCap := make([]int, 3, 10)      // length 3, capacity 10
```

### Append

```go
nums = append(nums, 6)             // add one element
nums = append(nums, 7, 8, 9)      // add multiple
other := []int{10, 11}
nums = append(nums, other...)      // spread another slice
```

**Important:** `append` may return a new slice if capacity is exceeded. Always reassign: `nums = append(nums, val)`.

### Slicing

```go
s := []int{0, 1, 2, 3, 4, 5}
s[1:4]   // [1, 2, 3]  — index 1 to 3
s[:3]    // [0, 1, 2]  — from start to index 2
s[3:]    // [3, 4, 5]  — from index 3 to end
s[:]     // [0,1,2,3,4,5] — full copy view
```

⚠️ Slices share the underlying array — modifying one affects the other!

```go
// Safe copy to avoid aliasing
dst := make([]int, len(src))
copy(dst, src)
```

### Iterating

```go
fruits := []string{"apple", "banana", "mango"}

for i, fruit := range fruits {
    fmt.Printf("[%d] %s\\n", i, fruit)
}

// Ignore index
for _, fruit := range fruits {
    fmt.Println(fruit)
}
```

### Common Slice Patterns

```go
// Filter (keep even numbers)
func filter(nums []int) []int {
    result := make([]int, 0)
    for _, n := range nums {
        if n%2 == 0 {
            result = append(result, n)
        }
    }
    return result
}

// Contains
func contains(slice []string, item string) bool {
    for _, s := range slice {
        if s == item {
            return true
        }
    }
    return false
}
```

## Maps

Maps store key-value pairs with O(1) average lookup.

```go
// Create maps
ages := map[string]int{
    "Alice": 30,
    "Bob":   25,
}

// make
scores := make(map[string]int)

// Set
scores["Alice"] = 95
scores["Bob"] = 82

// Get
fmt.Println(scores["Alice"]) // 95
fmt.Println(scores["Carol"]) // 0 — zero value for missing keys!

// Check existence (always use comma-ok pattern)
score, ok := scores["Carol"]
if !ok {
    fmt.Println("Carol not found")
}

// Delete
delete(scores, "Bob")
```

### Iterating Maps

```go
for key, value := range scores {
    fmt.Printf("%s: %d\\n", key, value)
}
// Note: map iteration order is RANDOM in Go
```

### Nested Maps

```go
// map of slices
groups := map[string][]string{
    "backend":  {"Alice", "Bob"},
    "frontend": {"Carol", "Dave"},
}
groups["backend"] = append(groups["backend"], "Eve")
```

## Structs vs Maps

| Use Case | Choose |
|----------|--------|
| Fixed, known fields | `struct` |
| Dynamic keys at runtime | `map` |
| JSON with unknown keys | `map[string]interface{}` |

## Interview Tip
Always use the comma-ok pattern (`value, ok := m[key]`) when reading from a map. Without it, you can't tell if a key is missing or if the stored value happens to be the zero value.""",
            "content_type": LessonContentType.explanation,
            "order_index": 2,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "Slices & Maps Quiz",
            "description": "Test your knowledge of Go slices and maps.",
            "questions": [
                {
                    "question": "What does `make([]int, 3, 10)` create?",
                    "options": [
                        "A slice with 10 elements, all set to 3",
                        "A slice of length 3 and capacity 10, zero-filled",
                        "An array of size 10 starting at index 3",
                        "A slice of length 10 and capacity 3",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "`make([]T, length, capacity)` creates a slice. Here: length=3 (3 accessible elements, zero-valued) and capacity=10 (can grow to 10 before reallocation).",
                    "order_index": 1,
                },
                {
                    "question": "Why should you always reassign the result of `append`?",
                    "options": [
                        "append always creates a brand new slice",
                        "append may allocate a new underlying array when capacity is exceeded, making the old slice stale",
                        "Go's garbage collector requires it",
                        "append modifies the slice in place but returns a length",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "When a slice's capacity is exceeded, `append` allocates a new, larger array and copies elements. The original variable still points to the old memory. Always use `s = append(s, val)`.",
                    "order_index": 2,
                },
                {
                    "question": "What is the result of reading a missing key from a map in Go?",
                    "options": [
                        "A runtime panic",
                        "nil",
                        "The zero value of the map's value type",
                        "An error is returned",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "Reading a missing key returns the zero value for the value type (0 for int, \"\" for string, etc.) — no panic, no error. Always use `val, ok := m[key]` to distinguish missing keys from zero values.",
                    "order_index": 3,
                },
                {
                    "question": "What is guaranteed about iterating a Go map with `range`?",
                    "options": [
                        "Iteration is in insertion order",
                        "Iteration is in alphabetical key order",
                        "Iteration order is random and not guaranteed",
                        "Iteration is sorted by value",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "Go deliberately randomizes map iteration order on each run to prevent developers from relying on a specific order. If you need sorted output, collect keys into a slice and sort it first.",
                    "order_index": 4,
                },
                {
                    "question": "How do you safely copy a slice to avoid sharing the underlying array?",
                    "options": [
                        "dst = src",
                        "dst := src[:]",
                        "dst := make([]int, len(src)); copy(dst, src)",
                        "dst := &src",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "Both `dst = src` and `dst := src[:]` create a slice that shares the same underlying array. Use `make` + `copy` to get a truly independent slice.",
                    "order_index": 5,
                },
            ],
        },
    },

    # ── Topic 3: Structs & Interfaces ─────────────────────────────────────────
    {
        "name": "go_structs_interfaces",
        "title": "Structs & Interfaces",
        "description": "Understand Go's approach to types — structs for data, interfaces for behavior, and embedding for composition.",
        "icon_name": "puzzle",
        "order_index": 3,
        "lesson": {
            "title": "Structs & Interfaces: Go's Object-Oriented Approach",
            "content": """# Structs & Interfaces

Go doesn't have classes. Instead it uses **structs** (data) + **methods** (behavior) + **interfaces** (contracts).

## Structs

```go
type User struct {
    ID       int
    Name     string
    Email    string
    IsAdmin  bool
}

// Create
u1 := User{ID: 1, Name: "Alice", Email: "alice@example.com"}
u2 := User{1, "Bob", "bob@example.com", false} // positional (fragile, avoid)

// Pointer to struct
u3 := &User{Name: "Carol"}
u3.Email = "carol@example.com" // Go auto-dereferences
```

### Methods

Methods are functions with a **receiver**:

```go
// Value receiver — receives a copy
func (u User) String() string {
    return fmt.Sprintf("%s <%s>", u.Name, u.Email)
}

// Pointer receiver — can modify the struct
func (u *User) Promote() {
    u.IsAdmin = true
}

// Usage
alice := User{Name: "Alice", Email: "alice@example.com"}
fmt.Println(alice.String())
alice.Promote() // Go auto-takes address: (&alice).Promote()
```

**Rule of thumb:** Use pointer receivers when you need to modify the struct OR when the struct is large (avoid copying).

### Struct Embedding (Composition over inheritance)

```go
type Base struct {
    CreatedAt time.Time
    UpdatedAt time.Time
}

type Product struct {
    Base           // embedded — promotes fields & methods
    Name  string
    Price float64
}

p := Product{Name: "Laptop", Price: 999.99}
p.CreatedAt = time.Now() // promoted from Base
```

## Interfaces

An interface defines a **set of method signatures**. Any type that implements all methods automatically satisfies the interface — no explicit declaration needed (**implicit implementation**).

```go
// Define interface
type Shape interface {
    Area() float64
    Perimeter() float64
}

// Implement for Circle
type Circle struct {
    Radius float64
}

func (c Circle) Area() float64 {
    return math.Pi * c.Radius * c.Radius
}

func (c Circle) Perimeter() float64 {
    return 2 * math.Pi * c.Radius
}

// Implement for Rectangle
type Rectangle struct {
    Width, Height float64
}

func (r Rectangle) Area() float64      { return r.Width * r.Height }
func (r Rectangle) Perimeter() float64 { return 2 * (r.Width + r.Height) }

// Use the interface
func printShape(s Shape) {
    fmt.Printf("Area: %.2f, Perimeter: %.2f\\n", s.Area(), s.Perimeter())
}

printShape(Circle{Radius: 5})
printShape(Rectangle{Width: 4, Height: 6})
```

### The Empty Interface

```go
// interface{} (or `any` in Go 1.18+) accepts any value
func printAnything(v interface{}) {
    fmt.Println(v)
}

// Type assertion
func describe(v interface{}) {
    switch t := v.(type) {
    case int:
        fmt.Printf("int: %d\\n", t)
    case string:
        fmt.Printf("string: %s\\n", t)
    default:
        fmt.Printf("unknown type: %T\\n", t)
    }
}
```

### Key Interfaces in the Standard Library

```go
// fmt.Stringer — controls how a type prints
type Stringer interface {
    String() string
}

// error — the built-in error interface
type error interface {
    Error() string
}

// io.Reader / io.Writer — used everywhere for I/O
type Reader interface {
    Read(p []byte) (n int, err error)
}
```

## Interface Best Practices

```go
// ✅ Accept interfaces, return concrete types
func NewService(db Database) *UserService { ... }

// ✅ Small, focused interfaces (Go proverb: "the bigger the interface, the weaker the abstraction")
type Writer interface {
    Write(p []byte) (n int, err error)
}

// ✅ Define interfaces where they are used (consumer side), not where types are defined
```

## Interview Tip
"How is Go's interface different from Java?" — Go uses **implicit (structural) typing** — you don't say `implements Shape`. If your type has the right methods, it automatically satisfies the interface. This enables loose coupling without requiring shared inheritance hierarchies.""",
            "content_type": LessonContentType.explanation,
            "order_index": 3,
            "estimated_minutes": 15,
        },
        "quiz": {
            "title": "Structs & Interfaces Quiz",
            "description": "Test your understanding of Go structs, methods, and interfaces.",
            "questions": [
                {
                    "question": "When should you use a pointer receiver instead of a value receiver?",
                    "options": [
                        "Always — pointer receivers are always faster",
                        "When the method needs to modify the struct, or the struct is large",
                        "Only when the struct is defined in another package",
                        "When calling the method on an interface",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Use a pointer receiver when you need to mutate the struct (value receivers receive a copy), or when the struct is large enough that copying is expensive. For small read-only methods, value receivers are fine.",
                    "order_index": 1,
                },
                {
                    "question": "How does a type satisfy an interface in Go?",
                    "options": [
                        "By declaring `implements InterfaceName`",
                        "By extending the interface with `extends`",
                        "Automatically, by implementing all the methods in the interface",
                        "By registering the type with the interface using `register()`",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "Go uses implicit (structural) interface satisfaction. Any type that has all the methods an interface requires automatically satisfies it — no explicit declaration needed.",
                    "order_index": 2,
                },
                {
                    "question": "What does struct embedding achieve in Go?",
                    "options": [
                        "Inheritance with method overriding like Java",
                        "Composition — promotes the embedded type's fields and methods into the outer struct",
                        "Creates a copy of the embedded struct's data",
                        "Allows the struct to implement multiple interfaces",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Embedding promotes the embedded type's fields and methods to the outer struct (composition, not inheritance). Go favors composition over inheritance — there's no class hierarchy.",
                    "order_index": 3,
                },
                {
                    "question": "What is `interface{}` (or `any`) in Go?",
                    "options": [
                        "A special pointer type",
                        "The base class all types inherit from",
                        "An empty interface that every type satisfies — can hold any value",
                        "A generic type parameter",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "`interface{}` (alias `any` in Go 1.18+) is an interface with zero methods. Since every type implements at least zero methods, every type satisfies it. Use type assertions or type switches to retrieve the concrete value.",
                    "order_index": 4,
                },
                {
                    "question": "What is the Go proverb about interface design?",
                    "options": [
                        "The bigger the interface, the stronger the abstraction",
                        "Always define interfaces in the package where types are declared",
                        "The bigger the interface, the weaker the abstraction",
                        "Prefer concrete types over interfaces for performance",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "Go interfaces work best when small and focused (like `io.Reader` with one method). Large interfaces are hard to implement and mock. Define interfaces where they are consumed, not where types live.",
                    "order_index": 5,
                },
            ],
        },
    },

    # ── Topic 4: Error Handling ───────────────────────────────────────────────
    {
        "name": "go_error_handling",
        "title": "Error Handling",
        "description": "Master Go's explicit error handling pattern — no exceptions, just values. Learn custom errors, wrapping, and panic/recover.",
        "icon_name": "shield",
        "order_index": 4,
        "lesson": {
            "title": "Error Handling: Go's Explicit Approach",
            "content": """# Error Handling in Go

Go has no exceptions. Errors are **values** returned from functions. This makes error paths explicit and impossible to ignore accidentally.

## The Basic Pattern

```go
result, err := someFunction()
if err != nil {
    // handle error
    return fmt.Errorf("operation failed: %w", err)
}
// use result
```

This "check every error" pattern is intentional — it forces developers to think about failure paths.

## The `error` Interface

```go
type error interface {
    Error() string
}
```

Any type with an `Error() string` method is an error.

## Creating Errors

```go
import "errors"
import "fmt"

// Simple string error
err1 := errors.New("something went wrong")

// Formatted error
err2 := fmt.Errorf("user %d not found", userID)

// Wrapping an error (Go 1.13+)
err3 := fmt.Errorf("getUserByID: %w", originalErr)
```

## Custom Error Types

```go
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed on field '%s': %s", e.Field, e.Message)
}

// Return a custom error
func validateAge(age int) error {
    if age < 0 {
        return &ValidationError{Field: "age", Message: "must be non-negative"}
    }
    return nil
}

// Check the type
err := validateAge(-1)
var valErr *ValidationError
if errors.As(err, &valErr) {
    fmt.Println("Field:", valErr.Field)
}
```

## Wrapping & Unwrapping

```go
// Wrap with %w to preserve the original error
dbErr := errors.New("connection timeout")
appErr := fmt.Errorf("fetchUser: %w", dbErr)

// errors.Is — checks if error matches anywhere in the chain
if errors.Is(appErr, dbErr) {
    fmt.Println("it's a db error") // ✅ true
}

// errors.As — extract a specific type from the chain
var valErr *ValidationError
if errors.As(err, &valErr) {
    fmt.Println(valErr.Field)
}
```

## Sentinel Errors

```go
// Define package-level errors for callers to match against
var (
    ErrNotFound   = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
)

func getUser(id int) (*User, error) {
    if id == 0 {
        return nil, ErrNotFound
    }
    // ...
}

// Caller checks
if errors.Is(err, ErrNotFound) {
    // handle not found
}
```

## Panic & Recover

`panic` is for **unrecoverable programming errors** (not expected runtime errors).

```go
// panic — stops normal execution
func mustPositive(n int) int {
    if n <= 0 {
        panic(fmt.Sprintf("expected positive, got %d", n))
    }
    return n
}

// recover — catches a panic (only works inside defer)
func safeDiv(a, b int) (result int, err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("recovered from panic: %v", r)
        }
    }()
    return a / b, nil
}
```

**Rule:** Use `error` for expected failures. Use `panic` only for bugs (nil pointer, index out of bounds) or truly unrecoverable states.

## defer

`defer` runs a function when the surrounding function returns — great for cleanup:

```go
func readFile(path string) (string, error) {
    f, err := os.Open(path)
    if err != nil {
        return "", err
    }
    defer f.Close() // always runs, even if error occurs below

    // read file...
}
```

Deferred calls run in **LIFO order** (last deferred = first to run).

## Interview Tip
"Why doesn't Go have exceptions?" — Go's designers believed exceptions lead to hidden control flow and poorly handled errors. Explicit `error` returns make failure paths visible in the code. The verbosity is intentional — it makes the code more maintainable.""",
            "content_type": LessonContentType.explanation,
            "order_index": 4,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "Error Handling Quiz",
            "description": "Test your knowledge of Go's error handling patterns.",
            "questions": [
                {
                    "question": "What is the idiomatic way to create a simple error in Go?",
                    "options": [
                        'throw new Error("message")',
                        'raise Exception("message")',
                        'errors.New("message") or fmt.Errorf("...")',
                        "panic(\"message\")",
                    ],
                    "correct_answer_index": 2,
                    "explanation": '`errors.New("message")` creates a simple static error. `fmt.Errorf("...")` creates a formatted error and supports wrapping with `%w`. There are no exceptions or throw in Go.',
                    "order_index": 1,
                },
                {
                    "question": "What does `fmt.Errorf(\"failed: %w\", err)` do compared to `%v`?",
                    "options": [
                        "Both are identical — %w and %v format the same way",
                        "%w wraps the original error so errors.Is/As can unwrap the chain; %v just formats the string",
                        "%w panics if err is nil; %v does not",
                        "%w is for warnings; %v is for errors",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "`%w` wraps the error, preserving the original in the chain so `errors.Is(wrapped, original)` returns true. `%v` just formats the error message as a string — the original error is lost.",
                    "order_index": 2,
                },
                {
                    "question": "When should you use `panic` in Go?",
                    "options": [
                        "Whenever an error occurs in your program",
                        "As a replacement for returning errors from functions",
                        "Only for unrecoverable programming errors or impossible states, not expected runtime failures",
                        "When you want to exit the program immediately",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "`panic` is for programming bugs (nil dereference, impossible state) — not for expected failures like network errors or missing records. Expected failures should use the `error` return pattern.",
                    "order_index": 3,
                },
                {
                    "question": "What is a sentinel error in Go?",
                    "options": [
                        "An error that causes a panic",
                        "A package-level error variable callers can check with errors.Is()",
                        "A custom error type with extra fields",
                        "An error returned only from the main function",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Sentinel errors are package-level `var` errors (e.g., `var ErrNotFound = errors.New(\"not found\")`). Callers use `errors.Is(err, ErrNotFound)` to check for them without string comparison.",
                    "order_index": 4,
                },
                {
                    "question": "What is `defer` used for in Go?",
                    "options": [
                        "To delay a goroutine from starting",
                        "To run a function after the surrounding function returns — useful for cleanup",
                        "To mark an error as deferred until later",
                        "To pause execution for a set duration",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "`defer` schedules a function call to run when the enclosing function exits (regardless of how). This is ideal for cleanup: `defer file.Close()`, `defer mutex.Unlock()`, etc.",
                    "order_index": 5,
                },
            ],
        },
    },

    # ── Topic 5: Goroutines & Channels ────────────────────────────────────────
    {
        "name": "go_concurrency",
        "title": "Goroutines & Channels",
        "description": "Unlock Go's killer feature — lightweight goroutines and channels for safe concurrent programming.",
        "icon_name": "zap",
        "order_index": 5,
        "lesson": {
            "title": "Goroutines & Channels: Go's Concurrency Model",
            "content": """# Goroutines & Channels

Go was built for concurrency. Its approach: **goroutines** (lightweight threads) + **channels** (communication) — summarized by the Go proverb:

> "Don't communicate by sharing memory; share memory by communicating."

## Goroutines

A goroutine is a lightweight thread managed by the Go runtime. Starting one costs ~2KB of stack (vs ~1MB for OS threads).

```go
// Start a goroutine with the `go` keyword
go func() {
    fmt.Println("running in goroutine")
}()

// Named function
go processOrder(orderID)

// main() exits when it returns — goroutines may be killed!
// Use sync mechanisms to wait
```

## sync.WaitGroup — wait for goroutines

```go
import "sync"

var wg sync.WaitGroup

for i := 0; i < 5; i++ {
    wg.Add(1)
    go func(id int) {
        defer wg.Done()
        fmt.Printf("Worker %d done\\n", id)
    }(i)
}

wg.Wait() // block until all goroutines call Done()
```

## Channels

Channels allow goroutines to communicate safely.

```go
// Unbuffered channel — sender blocks until receiver is ready
ch := make(chan int)

go func() {
    ch <- 42 // send
}()

value := <-ch // receive (blocks until data arrives)
fmt.Println(value) // 42

// Buffered channel — sender only blocks when buffer is full
buffered := make(chan string, 3)
buffered <- "a"
buffered <- "b"
buffered <- "c"
// buffered <- "d" // would block — buffer full

// Close a channel
close(ch) // receivers get zero value after close

// Receive with ok check
v, ok := <-ch
if !ok {
    fmt.Println("channel closed")
}

// Range over channel (reads until closed)
for msg := range msgChan {
    fmt.Println(msg)
}
```

## Real Example: Fan-out with goroutines

```go
func processURLs(urls []string) []string {
    results := make([]string, len(urls))
    var wg sync.WaitGroup

    for i, url := range urls {
        wg.Add(1)
        go func(i int, url string) {
            defer wg.Done()
            // fetch url...
            results[i] = "result for " + url
        }(i, url)
    }

    wg.Wait()
    return results
}
```

## select — multiplexing channels

```go
select {
case msg := <-ch1:
    fmt.Println("from ch1:", msg)
case msg := <-ch2:
    fmt.Println("from ch2:", msg)
case <-time.After(1 * time.Second):
    fmt.Println("timeout!")
default:
    fmt.Println("no activity")
}
```

`select` picks a ready case randomly if multiple are ready.

## sync.Mutex — protect shared state

```go
type SafeCounter struct {
    mu    sync.Mutex
    count int
}

func (c *SafeCounter) Inc() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

func (c *SafeCounter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.count
}
```

## Common Patterns

### Worker Pool

```go
func workerPool(jobs <-chan int, results chan<- int, numWorkers int) {
    var wg sync.WaitGroup
    for w := 0; w < numWorkers; w++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                results <- job * job // process job
            }
        }()
    }
    wg.Wait()
    close(results)
}
```

### Context for cancellation

```go
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

select {
case result := <-doWork(ctx):
    fmt.Println(result)
case <-ctx.Done():
    fmt.Println("timed out:", ctx.Err())
}
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Goroutine leak (never stopped) | Use `context.Cancel()` or done channels |
| Race condition on shared variable | Use `sync.Mutex` or channels |
| Closing a nil channel | Always initialize channels with `make` |
| Closing a channel twice | Only the sender should close |

## Interview Tip
"What's the difference between goroutines and OS threads?" — Goroutines are managed by the Go runtime (M:N threading), start with ~2KB stack (grows dynamically), and can run millions concurrently. OS threads are heavier (~1MB stack, OS-managed context switch).""",
            "content_type": LessonContentType.explanation,
            "order_index": 5,
            "estimated_minutes": 15,
        },
        "quiz": {
            "title": "Goroutines & Channels Quiz",
            "description": "Test your understanding of Go's concurrency model.",
            "questions": [
                {
                    "question": "How do you start a goroutine in Go?",
                    "options": [
                        "new Thread(() -> func()).start()",
                        "threading.Thread(target=func).start()",
                        "go funcName() or go func() { ... }()",
                        "async func()",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "The `go` keyword before a function call starts it as a goroutine. Both named functions (`go processOrder(id)`) and anonymous functions (`go func() { ... }()`) work.",
                    "order_index": 1,
                },
                {
                    "question": "What happens with an unbuffered channel when the sender sends a value?",
                    "options": [
                        "The value is discarded if no receiver is ready",
                        "The sender blocks until a receiver is ready to receive",
                        "The value is stored in a queue",
                        "A panic occurs if no receiver is ready",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "An unbuffered channel (`make(chan T)`) synchronizes sender and receiver — the sender blocks until a receiver reads the value, and vice versa. This is a synchronization point.",
                    "order_index": 2,
                },
                {
                    "question": "What is `sync.WaitGroup` used for?",
                    "options": [
                        "To limit the number of goroutines running simultaneously",
                        "To wait for a collection of goroutines to finish before continuing",
                        "To synchronize channel sends and receives",
                        "To create a pool of reusable goroutines",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "`sync.WaitGroup` tracks goroutines. Call `wg.Add(1)` before launching, `wg.Done()` (usually via defer) inside the goroutine, and `wg.Wait()` to block until all goroutines finish.",
                    "order_index": 3,
                },
                {
                    "question": "What does the `select` statement do in Go?",
                    "options": [
                        "Selects a random goroutine to run",
                        "Waits for all channels to have data",
                        "Blocks until one of the channel cases is ready, then executes that case",
                        "Filters values from a channel",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "`select` waits for one of its channel cases to be ready. If multiple are ready simultaneously, one is chosen at random. A `default` case makes it non-blocking.",
                    "order_index": 4,
                },
                {
                    "question": "What is a common cause of a goroutine leak?",
                    "options": [
                        "Using too many WaitGroups",
                        "Closing a channel that is already closed",
                        "A goroutine blocked on a channel receive with no sender, running forever",
                        "Creating goroutines inside for loops",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "A goroutine leak occurs when a goroutine is stuck waiting (e.g., blocked on a channel that is never sent to) and is never cleaned up. Use `context.WithCancel` or done channels to signal goroutines to stop.",
                    "order_index": 5,
                },
            ],
        },
    },
]

# ─── Scenarios ─────────────────────────────────────────────────────────────────

GO_SCENARIOS = [
    {
        "topic_name": "go_basics",
        "title": "Explaining Go to a Python Developer",
        "description": "A Python colleague wants to understand why your team chose Go for the new microservice. Explain Go's key advantages (static typing, compiled, concurrency) compared to Python in a clear, non-condescending way.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.beginner,
        "tags": ["go", "python", "comparison", "communication"],
        "order_index": 1,
        "system_prompt": "",
    },
    {
        "topic_name": "go_error_handling",
        "title": "Defending Go's Error Handling in Code Review",
        "description": "A teammate from a Java background says Go's error handling is 'verbose and repetitive' and suggests adding exceptions. Write a professional response defending Go's explicit error-handling approach.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.intermediate,
        "tags": ["go", "error-handling", "code-review", "communication"],
        "order_index": 1,
        "system_prompt": "",
    },
    {
        "topic_name": "go_concurrency",
        "title": "Explaining Goroutines in a Technical Interview",
        "description": "An interviewer asks: 'What are goroutines and how are they different from threads? Can you explain the Go concurrency model?' Write a clear, structured answer that would impress a senior engineer.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.intermediate,
        "tags": ["go", "goroutines", "concurrency", "interview"],
        "order_index": 1,
        "system_prompt": "",
    },
    {
        "topic_name": "go_concurrency",
        "title": "Go Technical Interview — Concurrency Deep Dive",
        "description": "Practice a real Go technical interview focused on concurrency. The interviewer will ask about goroutines, channels, race conditions, and real-world concurrency patterns. Answer clearly and confidently.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.advanced,
        "tags": ["go", "interview", "concurrency", "goroutines"],
        "order_index": 2,
        "system_prompt": """You are Sarah Kim, a senior Go engineer conducting a technical interview at a backend infrastructure company. You are assessing the candidate's Go concurrency knowledge.

Start the interview with: "Hi! Thanks for joining. I'm Sarah, a senior engineer here. Let's dive into some Go concurrency questions — I'll start with the basics and go deeper based on your answers. Ready?"

Then conduct the interview naturally. Cover these topics progressively:
1. What is a goroutine and how does it differ from an OS thread?
2. Explain buffered vs unbuffered channels — when would you use each?
3. How do you prevent race conditions? (mutex vs channels)
4. What is a goroutine leak and how would you detect/prevent one?
5. Walk me through how you'd implement a worker pool in Go.

Be professional and encouraging. If the answer is correct, acknowledge it and go deeper. If partially correct, ask a follow-up to probe understanding. If wrong, gently correct and move on. Ask one question at a time. Stay in character throughout.""",
    },
    {
        "topic_name": "go_structs_interfaces",
        "title": "Explaining Go Interfaces vs Java Interfaces",
        "description": "During an architecture discussion, a Java developer asks how Go interfaces differ from Java's. Write a clear technical explanation covering implicit implementation and why Go prefers small interfaces.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.intermediate,
        "tags": ["go", "interfaces", "java", "comparison"],
        "order_index": 1,
        "system_prompt": "",
    },
]


def seed_go(session: Session) -> None:
    """Seed Go Programming domain, course, topics, lessons, quizzes, and scenarios."""

    # ── Domain ────────────────────────────────────────────────────────────────
    domain = session.exec(select(Domain).where(Domain.slug == GO_DOMAIN["slug"])).first()
    if not domain:
        domain = Domain(**GO_DOMAIN)
        session.add(domain)
        session.flush()
        print(f"✅ Created domain: {GO_DOMAIN['slug']}")
    else:
        print(f"ℹ️  Domain '{GO_DOMAIN['slug']}' already exists, skipping.")

    # ── Course ────────────────────────────────────────────────────────────────
    course = session.exec(select(Course).where(Course.slug == GO_COURSE["slug"])).first()
    if not course:
        course = Course(**GO_COURSE, domain_id=domain.id)
        session.add(course)
        session.flush()
        print(f"✅ Created course: {GO_COURSE['slug']}")
    else:
        print(f"ℹ️  Course '{GO_COURSE['slug']}' already exists, skipping.")

    # ── Topics ────────────────────────────────────────────────────────────────
    existing_cat = session.exec(
        select(ScenarioCategory).where(ScenarioCategory.name == GO_TOPICS[0]["name"])
    ).first()
    if existing_cat:
        print("ℹ️  Go topics already seeded, skipping.")
        return

    category_map: dict[str, ScenarioCategory] = {}
    for topic in GO_TOPICS:
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

        print(f"✅ Seeded Go topic: {topic['name']}")

    # ── Scenarios ─────────────────────────────────────────────────────────────
    for sc_data in GO_SCENARIOS:
        cat = category_map.get(sc_data["topic_name"])
        if not cat:
            print(f"⚠️  Category '{sc_data['topic_name']}' not found for scenario, skipping.")
            continue
        sc_copy = sc_data.copy()
        sc_copy.pop("topic_name")
        scenario = Scenario(**sc_copy, category_id=cat.id)
        session.add(scenario)
        print(f"✅ Seeded Go scenario: {sc_copy['title'][:50]}")

    session.commit()
    print("✅ Go Programming content fully seeded.")
