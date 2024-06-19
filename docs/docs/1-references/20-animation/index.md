
# Animation for ISA Behaviors

**isa_manim** provides several animations that frequently appear in ISA so that users can build up ISA behaviors simply by choosing appropriate functions.

Animations can be categorized into three categories:

- [Animation for Registers and Elements](21-register-animation.md), including declaring and replacing registers, as well as reading, assigning, and replacing elements.
- [Animation for Functions](22-function-animation.md), including declaring and calling functions.
- [Animation for Memory](23-memory-animation.md), including declaring and reading/writing memory.

**isa_manim** provides one function for each kind of animation. Each function accepts related objects and parameters as input. Each function returns an entity of animation. Functions for animations do not create any objects.

> It is not suggested to directly call animation functions in user's codes. Instead, please use APIs provided in ISA scenes.
