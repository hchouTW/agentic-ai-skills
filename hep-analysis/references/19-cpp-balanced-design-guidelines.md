# Balanced C++ Design Guidelines

General C++ design guidance, not specific to HEP or ROOT. Read
[C++/ROOT coding](14-cpp-root-coding.md) and [Code conventions](18-code-conventions.md)
first for analysis-code-specific patterns and naming; use this reference for broader
class/struct/ownership/inheritance design questions that arise while writing analysis
software.

When modifying or writing C++ code, prefer a balanced style between object-oriented and procedural programming. Follow established repository conventions when they intentionally differ from this reference.

The examples follow the
[Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html):
two-space indentation, `PascalCase` function names, `snake_case` variables,
trailing underscores for data members, and documented namespace endings.
Google-style code does not use C++ exceptions, so fallible construction is
expressed with factory functions and return values.

## Contents

- [Core Principle](#core-principle)
- [Choosing Classes, Structs, and Free Functions](#when-to-use-a-class)
- [RAII and Resource Management](#raii-and-resource-management)
- [Inheritance and Polymorphism](#inheritance-and-polymorphism)
- [Encapsulation and State](#encapsulation-guidelines)
- [Error Handling](#error-handling)
- [Const-Correctness and Ownership](#const-correctness)
- [Naming and File Organization](#naming-guidance)
- [Testing and Generic Code](#testing-guidance)
- [Standard Library and Documentation](#standard-library-preference)
- [Design Checklist](#design-checklist)
- [Preferred Style](#preferred-style)
- [Anti-Patterns](#anti-patterns-to-avoid)
- [Summary Rule](#summary-rule)

## Core Principle

Use classes to protect state, lifetime, ownership, resources, and invariants.

Use free functions to express algorithms, transformations, calculations, and procedural workflows.

Do not force everything into classes. Do not write purely global-state procedural code either.

The preferred style is simple, idiomatic, testable C++.

---

## When to Use a Class

Use a `class` when the code needs one or more of the following:

- Encapsulated state
- A clear lifetime
- Ownership of a resource
- Invariants that must be protected
- RAII behavior
- Runtime polymorphism through a stable interface

Good examples:

```cpp
class File;
class Socket;
class BankAccount;
class Parser;
class Renderer;
class Order;
```

A class should represent a real concept in the domain or architecture, not merely act as a folder for related functions.

Prefer a `class` when there is something meaningful to hide, validate, protect, or manage.

Example:

```cpp
class BankAccount {
 public:
  static std::optional<BankAccount> Create(int initial_balance) {
    if (initial_balance < 0) {
      return std::nullopt;
    }
    return BankAccount(initial_balance);
  }

  bool Deposit(int amount) {
    if (amount <= 0) {
      return false;
    }

    balance_ += amount;
    return true;
  }

  bool Withdraw(int amount) {
    if (amount <= 0 || amount > balance_) {
      return false;
    }

    balance_ -= amount;
    return true;
  }

  int balance() const { return balance_; }

 private:
  explicit BankAccount(int initial_balance) : balance_(initial_balance) {}

  int balance_;
};
```

In this example, the class is justified because it protects the invariant that the balance must not become negative.

---

## When to Use a Struct

Use a `struct` for simple passive data where public fields are clear, safe, and intentional.

Prefer this:

```cpp
struct Point {
  double x;
  double y;
};
```

Avoid unnecessary getters and setters when there is no invariant to protect.

Avoid this unless validation or encapsulation is actually needed:

```cpp
class Point {
 public:
  double x() const { return x_; }

  void set_x(double x) { x_ = x; }

  double y() const { return y_; }

  void set_y(double y) { y_ = y; }

 private:
  double x_;
  double y_;
};
```

A `struct` is not inferior to a `class`. In C++, it is often the clearest choice for simple data types.

Use `struct` when:

- The type is mainly a data carrier
- The fields are safe to expose
- There are no important invariants
- The type has no complex ownership responsibility
- The type benefits from aggregate initialization

Example:

```cpp
struct Size {
  int width;
  int height;
};
```

If later the data needs validation or lifecycle management, it can be refactored into a class.

---

## When to Use Free Functions

Use free functions for algorithms, calculations, conversions, and operations that do not need private access to an object.

Prefer this:

```cpp
struct Point {
  double x;
  double y;
};

double Distance(Point a, Point b) {
  const auto dx = a.x - b.x;
  const auto dy = a.y - b.y;
  return std::sqrt(dx * dx + dy * dy);
}
```

Do not put a function inside a class only because it is related to a type.

A function should usually remain a free function when:

- It does not need private access
- It does not modify object invariants
- It represents an algorithm rather than object behavior
- It can be tested independently
- It can operate on multiple compatible types

Use member functions when the operation must preserve, validate, or modify the object's internal invariant.

Example of a justified member function:

```cpp
class Counter {
 public:
  void Increment() { ++value_; }

  int value() const { return value_; }

 private:
  int value_ = 0;
};
```

Example of a better free function:

```cpp
struct Point {
  double x;
  double y;
};

Point Midpoint(Point a, Point b) {
  return Point{
      .x = (a.x + b.x) / 2.0,
      .y = (a.y + b.y) / 2.0,
  };
}
```

---

## Avoid Artificial Utility Classes

Do not create classes that only wrap stateless helper functions.

Avoid this:

```cpp
class MathHelper {
 public:
  static int Add(int a, int b) { return a + b; }
};
```

Prefer this:

```cpp
int Add(int a, int b) { return a + b; }
```

If grouping is needed, use a namespace:

```cpp
namespace math {

int Add(int a, int b) { return a + b; }

}  // namespace math
```

Avoid names like these unless there is a strong reason:

```cpp
class Utils;
class Helper;
class Manager;
class Processor;
class Handler;
```

These names are not forbidden, but they often indicate unclear responsibility.

Prefer precise names that describe what the code owns, does, or represents.

Better examples:

```cpp
class HttpClient;
class FileReader;
class OrderBook;
class ImageDecoder;
class CommandParser;
class FrameRenderer;
```

---

## RAII and Resource Management

Use RAII for resources such as:

- Memory
- Files
- Sockets
- Locks
- Handles
- Transactions
- Temporary state that must be restored
- Any resource that must be released reliably

Resource acquisition and release should be tied to object lifetime.

Prefer standard library RAII types where possible:

```text
std::unique_ptr<T>
std::shared_ptr<T>
std::lock_guard<std::mutex>
std::unique_lock<std::mutex>
std::fstream
std::vector<T>
std::string
```

Avoid manual `new` and `delete` in normal application code.

Prefer this:

```cpp
auto widget = std::make_unique<Widget>();
```

Avoid this:

```cpp
Widget* widget = new Widget();
// ...
delete widget;
```

Use custom RAII classes when the standard library does not already provide an appropriate abstraction.

Example:

```cpp
class FileHandle {
 public:
  static std::optional<FileHandle> Open(const char* path) {
    std::FILE* file = std::fopen(path, "r");
    if (file == nullptr) {
      return std::nullopt;
    }
    return FileHandle(file);
  }

  ~FileHandle() {
    if (file_ != nullptr) {
      std::fclose(file_);
    }
  }

  FileHandle(const FileHandle&) = delete;
  FileHandle& operator=(const FileHandle&) = delete;

  FileHandle(FileHandle&& other) noexcept
      : file_(std::exchange(other.file_, nullptr)) {}

  FileHandle& operator=(FileHandle&& other) noexcept {
    if (this != &other) {
      if (file_ != nullptr) {
        std::fclose(file_);
      }

      file_ = std::exchange(other.file_, nullptr);
    }

    return *this;
  }

  std::FILE* get() const { return file_; }

 private:
  explicit FileHandle(std::FILE* file) : file_(file) {}

  std::FILE* file_;
};
```

RAII classes should clearly express ownership.

---

## Inheritance and Polymorphism

Do not introduce inheritance just to organize code.

Use runtime polymorphism only when the code truly needs interchangeable behavior behind a common interface.

Acceptable example:

```cpp
class Shape {
 public:
  virtual ~Shape() = default;

  virtual double Area() const = 0;
};

class Circle final : public Shape {
 public:
  explicit Circle(double radius) : radius_(radius) {}

  double Area() const override { return std::numbers::pi * radius_ * radius_; }

 private:
  double radius_;
};
```

Use this style when callers need to work with different concrete implementations through the same interface:

```cpp
std::vector<std::unique_ptr<Shape>> shapes;
```

Avoid deep inheritance hierarchies unless there is a clear architectural reason.

Before adding inheritance, consider these alternatives:

- Free functions
- Templates
- `std::variant`
- Composition
- Strategy objects
- Function objects
- Lambdas
- Plain data plus algorithms

Prefer composition over inheritance when behavior can be assembled from smaller parts.

Avoid this style unless there is a strong reason:

```cpp
class Animal {
 public:
  virtual ~Animal() = default;
  virtual void Speak() = 0;
};

class Dog : public Animal {};
class Cat : public Animal {};
class Bird : public Animal {};
```

A small number of cases may be better represented with `std::variant`:

```cpp
struct Circle {
  double radius;
};

struct Rectangle {
  double width;
  double height;
};

using Shape = std::variant<Circle, Rectangle>;
```

---

## Member Functions vs Free Functions

Prefer member functions for operations that are part of the object's essential behavior.

Good member functions usually:

- Preserve invariants
- Mutate internal state intentionally
- Depend on private representation
- Represent core behavior of the abstraction

Prefer free functions for operations that are external algorithms.

Good free functions usually:

- Do not need private access
- Are broadly reusable
- Are easy to test independently
- Keep the type smaller
- Express a clear computation or transformation

Example:

```cpp
class Polygon {
 public:
  static std::optional<Polygon> Create(std::vector<Point> points) {
    if (points.size() < 3) {
      return std::nullopt;
    }
    return Polygon(std::move(points));
  }

  const std::vector<Point>& points() const { return points_; }

 private:
  explicit Polygon(std::vector<Point> points) : points_(std::move(points)) {}

  std::vector<Point> points_;
};

double Perimeter(const Polygon& polygon) {
  const auto& points = polygon.points();

  double result = 0.0;

  for (size_t i = 0; i < points.size(); ++i) {
    const auto& current = points[i];
    const auto& next = points[(i + 1) % points.size()];
    result += Distance(current, next);
  }

  return result;
}
```

In this example, `Polygon` protects the invariant that it has at least three
points. `Perimeter` is a free function because it is an algorithm over the
public interface.

---

## Encapsulation Guidelines

Encapsulation should protect meaningful invariants, not create unnecessary boilerplate.

Use private data when:

- The data must stay valid according to rules
- Changes must go through validation
- Representation may change later
- Ownership must be controlled
- Thread-safety or synchronization is involved

Public data is acceptable when:

- The type is simple passive data
- There are no invariants
- The fields are naturally part of the type's meaning
- The type is used as a value object or data transfer object

Avoid writing trivial getters and setters just to imitate other languages.

Prefer direct public fields for simple data:

```cpp
struct Color {
  int red;
  int green;
  int blue;
};
```

Prefer validation when the values must be constrained:

```cpp
class Color {
 public:
  static std::optional<Color> Create(int red, int green, int blue) {
    if (!IsChannelValid(red) || !IsChannelValid(green) ||
        !IsChannelValid(blue)) {
      return std::nullopt;
    }
    return Color(red, green, blue);
  }

  int red() const { return red_; }

  int green() const { return green_; }

  int blue() const { return blue_; }

 private:
  Color(int red, int green, int blue) : red_(red), green_(green), blue_(blue) {}

  static bool IsChannelValid(int value) { return value >= 0 && value <= 255; }

  int red_;
  int green_;
  int blue_;
};
```

---

## State Management

Minimize mutable shared state.

Prefer:

- Local variables
- Function parameters
- Return values
- Immutable values
- Clear ownership
- Explicit dependencies

Avoid:

- Hidden global variables
- Singleton abuse
- Mutable global state
- Static state that makes testing difficult
- Functions that secretly depend on external state

Avoid this:

```cpp
std::string g_current_user;

bool CanAccessDocument(const Document& document) {
  return document.owner() == g_current_user;
}
```

Prefer this:

```cpp
bool CanAccessDocument(const Document& document, const User& user) {
  return document.owner() == user.id();
}
```

Pass dependencies explicitly unless there is a strong reason not to.

---

## Error Handling

Use a clear error-handling strategy that is consistent with the surrounding component and repository conventions.

Google-style code does not use C++ exceptions. Use a factory function when
construction can fail, and return a value that makes failure explicit.

Example:

```cpp
class Config {
 public:
  static std::optional<Config> Load(std::filesystem::path path) {
    if (!std::filesystem::exists(path)) {
      return std::nullopt;
    }
    return Config(std::move(path));
  }

 private:
  explicit Config(std::filesystem::path path) : path_(std::move(path)) {}

  std::filesystem::path path_;
};
```

Use return values for expected failure paths.

Example:

```cpp
std::optional<User> FindUserById(UserId id);
```

Use `bool` when callers only need success/failure and no diagnostic value would be lost.

Example:

```cpp
bool ContainsUser(UserId id);
```

For failures that need diagnostics, prefer the repository's established status
or result type. Avoid mixing multiple error-handling styles in the same
component without a clear reason.

---

## Const-Correctness

Use `const` to communicate intent.

Prefer:

```cpp
int size() const { return size_; }
```

Pass large objects by const reference when they do not need to be copied:

```cpp
void Render(const Scene& scene);
```

Pass small value types by value:

```cpp
double Distance(Point a, Point b);
```

Use `const` local variables when the value should not change:

```cpp
const auto count = items.size();
```

Const-correctness improves readability, correctness, and API design.

---

## Ownership Guidelines

Make ownership explicit.

Use values when ownership is simple:

```cpp
std::vector<Item> items;
```

Use `std::unique_ptr` for exclusive dynamic ownership:

```cpp
std::unique_ptr<Connection> connection;
```

Use `std::shared_ptr` only when ownership is genuinely shared.

Use raw pointers for non-owning nullable references when the repository has no clearer observer type.

Use references for non-owning required dependencies.

Do not infer ownership from a raw pointer. Document non-obvious lifetime constraints and prefer values, references, or standard smart pointers when they express the contract more clearly.

Example:

```cpp
class Renderer {
 public:
  explicit Renderer(const TextureCache& texture_cache)
      : texture_cache_(texture_cache) {}

 private:
  const TextureCache& texture_cache_;
};
```

Avoid unclear ownership:

```cpp
class Renderer {
 public:
  explicit Renderer(TextureCache* texture_cache)
      : texture_cache_(texture_cache) {}

 private:
  TextureCache* texture_cache_;
};
```

If a pointer is used, clarify whether it owns the object.

---

## Naming Guidance

Use names that describe the responsibility clearly.

Prefer nouns for types:

```cpp
class HttpClient;
class FileReader;
class OrderBook;
struct Point;
struct Size;
```

Prefer verbs or verb phrases for functions:

```cpp
ParseConfig();
LoadImage();
CalculateTotal();
NormalizePath();
```

Avoid vague names:

```cpp
DoStuff();
HandleData();
Process();
Run();
Manage();
```

Short names are acceptable for small scopes:

```cpp
for (const auto& x : values) {
  // ...
}
```

Use more descriptive names for wider scopes.

---

## File Organization

Keep files focused.

A file should usually contain:

- One primary class or abstraction
- Closely related simple structs
- Closely related free functions
- Implementation details hidden in an unnamed namespace when appropriate

Use namespaces to group related functionality.

Example:

```cpp
namespace geometry {

struct Point {
  double x;
  double y;
};

double Distance(Point a, Point b);

class Polygon;

}  // namespace geometry
```

Avoid large files that mix unrelated responsibilities.

Avoid catch-all files such as:

```text
utils.cc
helpers.cc
misc.cc
common.cc
```

These are acceptable only for very small, clearly scoped collections.

---

## Testing Guidance

Prefer designs that are easy to test.

Free functions should be deterministic when possible.

Classes should expose behavior, not internal implementation details.

Avoid hidden dependencies that make tests fragile.

Prefer dependency injection over hard-coded global dependencies.

Example:

```cpp
class ReportGenerator {
 public:
  explicit ReportGenerator(const Clock& clock) : clock_(clock) {}

 private:
  const Clock& clock_;
};
```

Avoid this:

```cpp
class ReportGenerator {
 public:
  Report Generate() {
    const auto now = SystemClock::Now();
    // ...
  }
};
```

Code should be designed so that core logic can be tested without file systems, networks, timers, or global state when possible.

---

## Templates and Generic Code

Use templates when the algorithm naturally works across multiple types.

Good example:

```cpp
template <typename Range>
typename Range::value_type Sum(const Range& values) {
  typename Range::value_type result{};

  for (const auto& value : values) {
    result += value;
  }

  return result;
}
```

Do not use templates only to avoid writing clear types.

Do not over-generalize too early.

Prefer simple concrete code first. Introduce templates when repeated patterns are clear and the generic version remains readable.

---

## Standard Library Preference

Prefer the C++ standard library over custom implementations.

Use:

```text
std::vector
std::array
std::string
std::string_view
std::optional
std::variant
std::unique_ptr
std::shared_ptr
std::filesystem
std::chrono
std::span
std::ranges
```

Do not write custom containers, smart pointers, string classes, or date/time utilities unless there is a strong project-specific reason.

Prefer algorithms from the standard library when they improve clarity:

```text
std::find
std::sort
std::transform
std::accumulate
std::any_of
std::all_of
std::none_of
```

Use standard algorithms when they make intent clearer. Use loops when they are more readable.

---

## Comments and Documentation

Write comments to explain why, not what.

Avoid comments that repeat the code:

```cpp
// Increment i by 1.
++i;
```

Prefer comments that explain intent, constraints, or non-obvious decisions:

```cpp
// Keep this threshold in sync with the server-side timeout policy.
constexpr auto timeout = std::chrono::seconds{30};
```

Public APIs should have enough documentation to explain:

- What the function or type represents
- Ownership expectations
- Error behavior
- Important preconditions
- Important postconditions

Avoid excessive comments around obvious code.

---

## Design Checklist

Before adding a new class, ask:

1. Does it own state?
2. Does it protect an invariant?
3. Does it manage a resource?
4. Does it represent a real concept?
5. Does it need polymorphic behavior?
6. Would a simple `struct` plus free functions be clearer?

Before adding a new member function, ask:

1. Does it need access to private state?
2. Does it preserve or modify an invariant?
3. Is it essential behavior of the object?
4. Would a free function be more flexible and testable?

Before adding a free function, ask:

1. Is this mostly an algorithm or calculation?
2. Does it avoid unnecessary access to private state?
3. Can it be tested independently?
4. Does it make the type simpler?

Before adding inheritance, ask:

1. Is runtime polymorphism required?
2. Will callers use different implementations through a common interface?
3. Would composition be simpler?
4. Would `std::variant` be clearer?
5. Is the hierarchy likely to remain shallow and stable?

---

## Preferred Style

Prefer code shaped like this:

```cpp
namespace geometry {

struct Point {
  double x;
  double y;
};

double Distance(Point a, Point b) {
  const auto dx = a.x - b.x;
  const auto dy = a.y - b.y;
  return std::sqrt(dx * dx + dy * dy);
}

class Polygon {
 public:
  static std::optional<Polygon> Create(std::vector<Point> points) {
    if (points.size() < 3) {
      return std::nullopt;
    }
    return Polygon(std::move(points));
  }

  const std::vector<Point>& points() const { return points_; }

 private:
  explicit Polygon(std::vector<Point> points) : points_(std::move(points)) {}

  std::vector<Point> points_;
};

double Perimeter(const Polygon& polygon) {
  const auto& points = polygon.points();

  double result = 0.0;

  for (size_t i = 0; i < points.size(); ++i) {
    result += Distance(points[i], points[(i + 1) % points.size()]);
  }

  return result;
}

}  // namespace geometry
```

In this example:

- `Point` is simple data, so it is a `struct`.
- `Distance` is an algorithm, so it is a free function.
- `Polygon` has an invariant, so it is a `class`.
- `Perimeter` is an algorithm over `Polygon`, so it is a free function.

---

## Anti-Patterns to Avoid

Avoid excessive object-oriented design:

```cpp
class DistanceCalculator {
 public:
  double Calculate(const Point& a, const Point& b);
};
```

Prefer:

```cpp
double Distance(Point a, Point b);
```

Avoid stateless utility classes:

```cpp
class StringUtils {
 public:
  static std::string Trim(std::string_view input);
};
```

Prefer:

```cpp
namespace strings {

std::string Trim(std::string_view input);

}  // namespace strings
```

Avoid unnecessary inheritance:

```cpp
class BaseProcessor {
 public:
  virtual ~BaseProcessor() = default;
  virtual void Process() = 0;
};
```

Prefer a plain function or function object if only one behavior exists:

```cpp
void Process(Document& document);
```

Avoid global mutable state:

```cpp
Config g_config;
```

Prefer explicit dependencies:

```cpp
void RunApplication(const Config& config);
```

Avoid classes with unclear responsibility:

```cpp
class DataManager;
class LogicHandler;
class SystemProcessor;
```

Prefer names that describe the actual role:

```cpp
class UserRepository;
class CommandDispatcher;
class InvoiceCalculator;
```

---

## Summary Rule

As a default:

- Use `class` for state, ownership, lifetime, invariants, resources, RAII, and true runtime polymorphism.
- Use `struct` for simple passive data.
- Use free functions for algorithms, calculations, conversions, and procedural workflows.
- Avoid unnecessary inheritance.
- Avoid fake OOP such as stateless utility classes.
- Avoid hidden global mutable state.
- Prefer explicit ownership and explicit dependencies.
- Prefer standard library facilities over custom infrastructure.
- Prefer simple, readable, testable, idiomatic C++.

When uncertain, choose the simpler design first. Add abstraction only when the code clearly benefits from it.
