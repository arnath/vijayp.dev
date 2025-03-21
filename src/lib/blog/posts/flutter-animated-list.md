---
title: "Random Flutter tip: How to delay the animation when removing from AnimatedList"
date: 2025-03-21
published: true
---

_TL;DR: Flutter's `AnimatedList` uses `AnimationController.reverse` to run the remove animation so
the delay needs to be flipped using `Interval.flipped`._

## The Problem

Flutter provides an [`AnimatedList`][al] widget that animates items when they are inserted or
removed. To remove an item, you have to get the [`AnimatedListState`][als] and call this API:

```dart
void removeItem(
    int index,
    Widget Function(BuildContext, int, Animation<double>) builder, {
    Duration duration = _kDuration,
})
```

To remove an item with an animation (for example, sliding it off the screen), you can use things
like [`SlideTransition`][st]:

```dart
animatedListState.removeItem(
  index,
  (context, index, animation) => SlideTransition(
    position: Tween<Offset>(
      begin: const Offset(1, 0),
      end: Offset.zero,
    ).animate(animation),
    child: SizedBox.shrink(),
  ),
);
```

A quick comment because I was confused by this at first: the `child` here is expected to be a
non-interactive version of your list item. The purpose is basically to give you the chance to remove
any touch interactions before the removal animation starts.

I wanted to add a delay to this animation. When a user does something that causes an item to be
removed, I wanted there to be a slight delay so that they can see what's going on. I looked around
and found the [`Interval`][i] class.

I poked around and put together this code, which I thought would do nothing for most of the
animation and then slide it out quickly at the end:

```dart
SlideTransition(
  position: Tween<Offset>(
    begin: const Offset(1, 0),
    end: Offset.zero,
  ).animate(
    CurvedAnimation(parent: animation, curve: const Interval(0.9, 1)),
  ),
  child: SizedBox.shrink(),
)
```

Instead, what happened was that the animation happened _super_ quickly, as soon as I performed the
interaction. I was super confused by this so I went digging into the code. I found out that
`AnimatedListState.removeItem` does this internally:

```dart
controller.reverse().then<void>((void value) {
  ...
});
```

Basically, they use the same [`AnimationController`][ac] for both inserts and removes and for
removes, they run it in reverse. My interval wasn't working because the animation was being run in
reverse, which put the active interval at the very beginning. Luckily, there is an
`Interval.flipped` property you can access.

## The Solution

That led me to this, succesful code that lets you delay the removal animation from an
`AnimatedList`. The `Duration` you specify will apply to the whole `Interval`. So if you supply a
duration of 1 second and an interval of 0.5-1, it will do nothing for half a second and then perform
the animation for the other half.

```dart
animatedListState.removeItem(
  index,
  (context, index, animation) => SlideTransition(
    position: Tween<Offset>(
      begin: const Offset(1, 0),
      end: Offset.zero,
    ).animate(
      CurvedAnimation(parent: animation, curve: const Interval(0.5, 1)),
    ),
    child: SizedBox.shrink(),
  ),
  duration: const Duration(milliseconds: 1000),
);
```

[al]: https://api.flutter.dev/flutter/widgets/AnimatedList-class.html
[als]: https://api.flutter.dev/flutter/widgets/AnimatedListState-class.html
[st]: https://api.flutter.dev/flutter/widgets/SlideTransition-class.html
[i]: https://api.flutter.dev/flutter/animation/Interval-class.html
[ac]: https://api.flutter.dev/flutter/animation/AnimationController-class.html
