---
name: ios-distribution-feature-flags
description: >-
  Make a SwiftUI or mixed iOS app behave differently in Debug, TestFlight and App Store builds at compile time. Use to hide unfinished features, turn the paywall off for testers or support trunk-based development. It covers distribution flags, not remote kill switches.
metadata:
  docs-verified: "2026-09-28"
---

# iOS distribution feature flags

Compile-time flags per distribution. This is not Firebase Remote Config. Use Remote Config later for runtime rollout — don't grow this enum into a server.

Does not replace Swift architecture or SwiftUI skills.

## Xcode

1. Duplicate the Release configuration to `AppStore` and `TestFlight`. Point schemes at them.
2. Set `SWIFT_ACTIVE_COMPILATION_CONDITIONS` to `APPSTORE $(inherited)` / `TESTFLIGHT $(inherited)` for those **configurations**, at project or target level.
   Leave Debug at the Xcode template value `DEBUG $(inherited)`.
   Neither flag is set there, so the `#else` branch below resolves Debug to `.debug`.
   Plain Release also sets neither flag and resolves to `.debug`, so archive only with `AppStore` or `TestFlight`.

Target-level values override project-level values.
If the target sets the condition list for those configurations without `$(inherited)`, the project flags are hidden and `Distribution.current` is always `.debug`.

## Code

```swift
public enum Distribution: Sendable {
  case debug, appstore, testflight
  static var current: Self {
    #if APPSTORE
    .appstore
    #elseif TESTFLIGHT
    .testflight
    #else
    .debug
    #endif
  }
}

public struct FeatureFlags: Sendable {
  public let requirePaywall: Bool
  public let featureX: Bool
  public init(distribution: Distribution) {
    switch distribution {
    case .debug:      requirePaywall = true;  featureX = true
    case .testflight: requirePaywall = false; featureX = true
    case .appstore:   requirePaywall = true;  featureX = false
    }
  }
}
```

Declare the environment value and inject once at the root:

```swift
extension EnvironmentValues {
  @Entry var featureFlags = FeatureFlags(distribution: .current)
}

RootView()
  .environment(\.featureFlags, FeatureFlags(distribution: .current))
```

Views read `featureFlags.requirePaywall`. Incomplete work stays on `main` behind a flag. Delete the flag when the feature is proven in App Store.

Do not ship TestFlight values (`requirePaywall = false`) in the App Store config. Flags that live forever become a second product matrix.

## Sources

- <https://swiftwithmajid.com/2025/09/16/feature-flags-in-swift/>
- <https://developer.apple.com/documentation/xcode/configuring-the-build-settings-of-a-target>
- <https://developer.apple.com/documentation/xcode/build-settings-reference>
- <https://developer.apple.com/documentation/swiftui/entry()>
- <https://sarunw.com/posts/how-to-check-if-swift-code-is-in-debug-build-configuration/>
