---
title: Things I wish I'd known when I started using Flutter
date: 2023-08-27
published: true
last_updated: 2025-02-03
---

Recently, I've been playing around in Flutter as a way to make iOS apps. I hate basically everything
about Apple's iOS development environment, especially Swift, XCode, Apple's documentation. For me,
using frameworks has been muchs easier than trying to write native iOS code. Having tried a lot of
them at this point, Flutter seems like the current best option. However, there are definitely some
things I wish I had known when I started using Flutter. <br />

## Objects are cheap and composability is key

When I first started playing around in Flutter, I was always confused by how few properties
individual widgets have. Compared to CSS for example, there wasn't a way to define things like
padding or borders in most widgets.

What I eventually realized is that Flutter just has a very different model. Conceptually, objects
are intended to be cheap in Flutter and the primary way to build a UI is through composing widgets
together. So you don't need to feel bad wrapping that widget in an `Expanded` wrapped in a `Column`
wrapped in a `Padding`! <br />

## Most UI components don't store any state

Most (all?) built-in UI components in Flutter don't store any state. For example, the `Checkbox`
widget doesn't store a checked/unchecked value. The `TextField` widget doesn't store the current
text in the field. There's a couple interesting things that come from this:

1. This is why the various controller classes for widgets (like `TextEditingController`) exist. The
   widgets themselves don't store any state so Flutter provides the controller classes to do that.
   You can also choose to store the state yourself.
1. You _must_ redraw widgets when their state changes. In most UI frameworks that I have used, a
   checkbox has a "checked" value and if you click the checkbox, it toggles visually. In Flutter,
   clicking a checkbox does nothing by default. You have to implement the `onChanged` handler and
   have that cause a redraw by updating your application state. This one took me a while to wrap my
   head around. <br />

## Simple state management is usually best

[There][state-1] [are][state-2] [a][state-3] [lot][state-4] of libraries for state management in
Flutter. After trying a lot of different options, I believe that really simple state management is
the best option for most cases. What does this mean? There's a couple built-in classes that will
handle 99% of your state management needs: [ValueNotifier][vn]/[ChangeNotifier][cn] and
[ValueListenableBuilder][vlb]/ [ListenableBuilder][lb].

At a high level, I do the following for widgets with state:

1. Extend `StatefulWidget`
1. Have your `State<T>` class either implement/mixin `ChangeNotifier` or expose some
   `ValueNotifiers`.
1. Wrap the widgets that consume that state in `ValueListenableBuilder` or `ListenableBuilder`.

I like this because it allows me to be as granular as I want, either by defining a bunch of small
`ValueNotifiers` or having the whole state class extend `ChangeNotifier`. It does the same thing on
the widget builder side, where you can wrap your entire widget in `ListenableBuilder` or just
individual UI elements. <br />

## Don't use the Cupertino library

This is just my opinion but I would recommend against using the Cupertino library. I'm mostly aiming
to make iPhone apps so my first instinct was to use the Cupertino library to match the iOS look and
feel. Unfortunately, the library isn't very fleshed out. There's a lot of functionality you would
expect that is available in the Material library but not the Cupertino one.

I recommend using Material or some kind of third-party UI components.

[state-1]: https://docs.flutter.dev/ui/interactivity
[state-2]: https://api.flutter.dev/flutter/widgets/InheritedWidget-class.html
[state-3]: https://pub.dev/packages/provider
[state-4]: https://riverpod.dev/
[vn]: https://api.flutter.dev/flutter/foundation/ValueNotifier-class.html
[vlb]: https://api.flutter.dev/flutter/widgets/ValueListenableBuilder-class.html
[cn]: https://api.flutter.dev/flutter/foundation/ChangeNotifier-class.html
[lb]: https://api.flutter.dev/flutter/widgets/ListenableBuilder-class.html
