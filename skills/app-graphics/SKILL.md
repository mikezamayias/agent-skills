---
name: app-graphics
description: >-
  Generate a complete store and marketing graphics package for a Flutter or web app from its local files. Covers store icons (adaptive Android, iOS 18 light, dark, tinted), feature graphic, social banners and press kit hero. Also covers App Store product page header and search result creative assets, image or video. Use when preparing store or launch artwork, building app icons, rebranding an icon or making an OG card.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
metadata:
  docs-verified: "2026-09-28"
  openclaw:
    emoji: 🎨
---

# app-graphics

This skill covers every app graphic that is not a screenshot: app icons, feature graphics, App Store creative assets (product page header and search results), banners, social art, and the press kit hero.
Screenshots have a separate skill (`app-screenshots`).

## When to invoke

The human says something like "generate the graphics package", "build the icons", "make a Play Store feature graphic", "create an OG card for this app", "rebrand this app's icon", or "I need launch art for X".

## Activation rules

1. **The working directory must be a project root.**
   If it has no `pubspec.yaml`, `package.json`, or `README.md`, ask the human to `cd` first.
   Do not invent a project.
2. **An image generation tool must be available.**
   Use whatever the environment provides, such as a built-in image tool, an image generation MCP server, an image model API, or an agent CLI with image generation.
   If none is available, say so and stop.
   Do not install or sign up for a tool without the human's approval.
3. **Record the chosen tool** in `BRAND_PROFILE.md` so re-runs use the same one and the set stays coherent.

## Phases

| Phase | What                                                                                                 | Why                            |
| ----- | ---------------------------------------------------------------------------------------------------- | ------------------------------ |
| 0     | Discover the brand from local files (`pubspec.yaml`, `README.md`, existing icon files, theme tokens) | Do not hallucinate the brand   |
| 1     | Write `store_assets/BRAND_PROFILE.md` and get human confirmation                                     | Sets the visual direction once |
| 2     | Generate the app icon set                                                                            | 9 icon variants per spec       |
| 3     | Generate banners and social art                                                                      | 6 standard banner sizes        |
| 4     | Wire icons into the Flutter build (`flutter_launcher_icons`) if applicable                           | Makes the assets actually ship |
| 5     | Verify dimensions and alpha, then write `GRAPHICS_INDEX.md`                                          | Leaves a trail for re-runs     |

## Required output paths (per project)

```text
store_assets/
├── BRAND_PROFILE.md
├── GRAPHICS_INDEX.md
└── graphics/
    ├── app_icon/
    │   ├── app_store_1024x1024.png        # PNG, NO alpha, no rounded corners
    │   ├── play_store_512x512.png         # PNG, alpha allowed
    │   ├── adaptive_foreground_432x432.png # transparent bg, glyph in 264x264 safe zone
    │   ├── adaptive_background_432x432.png # solid/gradient fill
    │   ├── adaptive_monochrome_432x432.png # single-color glyph on transparent, Android 13+ themed icons
    │   ├── notification_96x96.png         # monochrome white on transparent
    │   ├── ios18_light_1024x1024.png      # iOS 18+ light variant
    │   ├── ios18_dark_1024x1024.png       # iOS 18+ dark variant
    │   └── ios18_tinted_1024x1024.png     # iOS 18+ tinted variant
    ├── feature_graphic/
    │   └── play_store_1024x500.png
    ├── app_store_creative/                # optional, iOS 27 and iPadOS 27 and later
    │   ├── header_3840x1646.png           # 21:9, no alpha, header only
    │   ├── universal_5244x2950.png        # 16:9 PNG, accepted for header and search results
    │   ├── search_3840x2560.png           # 3:2, 1920x1280 to 3840x2560
    │   ├── header_3840x1646.mp4           # optional video, 30 or 60 fps, 5-30 s, loops cleanly
    │   └── header_poster.png              # chosen poster frame
    ├── social/
    │   ├── og_card_1200x630.png
    │   ├── square_1080x1080.png
    │   ├── x_header_1500x500.png          # optional (per-app X account only)
    │   └── linkedin_banner_1584x396.png   # optional
    └── press/
        └── hero_1920x1080.png
```

If `store_assets/` already holds a prior run, **do not overwrite it**.
Append a `_v2` or `_v3` suffix and ask the human which version to ship.

## Prompt rules

Write one prompt per asset.
These rules apply to every prompt:

- Fill the app name, tagline, glyph idea, brand gradient, and voice from `BRAND_PROFILE.md`.
- State the exact target size and aspect ratio.
- **No text in icons.**
  Apple's guidelines allow text only when it is essential, and Google Play prohibits icon text that suggests ranking, deals, or program participation.
- **No copyrighted shapes**, such as the Apple silhouette, brand logos, or sports team marks.
- Ask for a full-bleed square with no rounded corners, because the stores apply their own mask.
- For the adaptive foreground, the adaptive monochrome layer, and the notification icon, ask for a transparent background.
- Reuse the same style description across the set so the assets stay coherent.

Many image tools cannot produce exact store sizes or control the alpha channel.
Generate at the closest supported size, then fix the output locally in Phase 5.
If an asset cannot be brought to spec, log it as `Stuck` in `BRAND_PROFILE.md` and move on instead of looping on it.

## Post-processing and verification (Phase 5)

Use whatever image utility is installed, such as `sips` on macOS or ImageMagick elsewhere.

Resize or crop to the exact spec size:

```bash
sips -z <height> <width> "<file>"          # macOS
magick "<file>" -resize <width>x<height>! "<file>"  # ImageMagick
```

Remove the alpha channel from the App Store icon:

```bash
magick "<file>" -background white -alpha remove -alpha off "<file>"
```

Check each file:

```bash
sips -g pixelWidth -g pixelHeight -g hasAlpha "<file>"   # macOS
magick identify -format "%w %h %A\n" "<file>"            # ImageMagick
```

Required checks:

- Dimensions match the spec table exactly.
- The App Store 1024 icon has no alpha channel.
- The Play feature graphic has no alpha channel, because Play requires JPEG or 24-bit PNG.
- App Store creative asset images match their placement size exactly and have no alpha channel.
- A creative asset video shows 3840x1646 (header), 30 or 60 fps, and a duration from 5 to 30 s in `ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate:format=duration`.
- The first and last frame of a creative asset video match, so the loop has no visible jump.
- No text appears where the prompt said "no text".
- The palette is coherent across the set, by visual comparison.

Write `store_assets/GRAPHICS_INDEX.md` listing what shipped and what was skipped.
Append one line to `store_assets/graphics-runs-log.md`:

```text
YYYY-MM-DD HH:MM - <project> - <image tool> - N icons + M banners
```

## Text inside banners

Short text inside a banner, such as a headline or subtitle, gets a plain-language pass before it goes into a prompt.
Avoid puffery such as "transformative", "revolutionary", "the best", "simplify your life", and "unlock the power of".
Image models often misspell text, so check every rendered word.
If the text keeps coming out wrong, generate the art without text and add the text as a local overlay.

## Store icon rules

- The App Store icon is a 1024x1024 PNG with no alpha and no rounded corners.
- The Play Store icon is a 512x512 32-bit PNG in sRGB, at most 1024 KB.
  It may use alpha, but Google recommends a full-square, opaque background because transparent areas show the Play UI background.
- The Android adaptive foreground keeps the glyph inside the central 264x264 safe zone of the 432x432 canvas.
- The Android adaptive monochrome layer is a single-color version of the foreground glyph on a transparent background, inside the same safe zone.
  Android 13 and later tints it from the user's wallpaper when themed icons are on.
  With `flutter_launcher_icons`, set it through `adaptive_icon_monochrome`.
- The Android notification icon is white on transparent, with no color.
- The iOS 18 dark variant uses a transparent or dark background, and the tinted variant is a grayscale glyph that the system tints.
- Since iOS 26, Apple recommends layered icons built in Icon Composer, which adds Liquid Glass effects and default, dark, clear, and tinted appearances.
  Flattened 1024x1024 images are still accepted, and the system generates any appearance variant you do not provide.

## App Store creative assets

On iOS 27 and iPadOS 27 and later, a product page can show a header image or video, and search results can show a creative asset.
Creative assets for the product page header and for search results support both images and videos.
Specs come from Apple's "Creative assets specifications" page:

| Placement      | Image                                                                          | Video                                                                     |
| -------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------- |
| Product header | 21:9 at 3840x1646 (jpeg, jpg or png), or 16:9 at 5244x2950 (png)               | 21:9 at 3840x1646, 30 or 60 fps, 5 to 30 s, mov, m4v or mp4               |
| Search results | 3:2 from 1920x1280 to 3840x2560 (jpeg, jpg or png), or 16:9 at 5244x2950 (png) | 3:2 from 1920x1280 to 3840x2560, 30 or 60 fps, 5 to 30 s, mov, m4v or mp4 |

- Images cannot include alpha channels or transparency.
- The spec page lists no 16:9 video size and no GIF format, so an animated header is a video file.
- Videos are muted by default in both placements and loop continuously.
  People can unmute them on the product page but not in search results.
  Apple says the creative "must work silently first".
- If an app has no search result creative asset, the App Store shows its in-app events, app previews, and screenshots in search results.
- A universal creative asset can serve both placements.
  Otherwise select a dedicated asset for each.
- Design with a safe area in mind and keep the focal point in the center of the composition, so different devices and orientations do not clip it.
  Apple publishes Figma, Sketch, Photoshop, and Pixelmator templates that define the safe area, linked from the asset best practices page.
- Focus on a single, clear idea.
  Avoid quick cuts and fast-moving visuals.
  Lead with the value proposition or the most compelling feature.
- If the asset has text, use a short phrase that enhances the visual rather than describes it, and localize it for every supported language.
- Content bans from guideline 2.3.14 and Apple's best practices:
  - No inappropriate content, no references to other apps with an intent to mislead, and no unverifiable product claims.
  - No specific or discounted pricing, no website URLs, and no copyright symbols.
  - No logos of, or references to, other platforms or marketplaces.
  - The asset must meet a 4+ age rating, even if the app's rating is higher.
- Creative assets are distinct from the in-use requirement for screenshots and app previews.
  They may show brand, seasonal offerings, or new content.
- Choose the poster frame deliberately.
  It applies everywhere the asset is used and cannot be edited after the asset is approved.
- Review is separate from screenshots.
  Standalone assets are reviewed against the app's latest version, and approved assets can replace the ones on a live version without submitting a new version.
- Upload and submit with the `asc asset-library` commands in `asc-cli-usage`, then check each device and orientation in App Store Connect's preview before submitting.

## Related skills

- `app-screenshots` for screenshot capture and framing, which this skill does not duplicate.
- `app-landing-page` for landing page art, which uses the graphics from this skill.

## Sources

- <https://developer.apple.com/design/human-interface-guidelines/app-icons>
- <https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications/>
- <https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets/>
- <https://developer.apple.com/app-store/asset-best-practices/>
- <https://developer.apple.com/app-store/review/guidelines/>
- <https://support.google.com/googleplay/android-developer/answer/9866151>
- <https://developer.android.com/distribute/google-play/resources/icon-design-specifications>
- <https://developer.android.com/develop/ui/views/launch/icon_design_adaptive>
- <https://developer.android.com/about/versions/lollipop/android-5.0-changes>
- <https://pub.dev/packages/flutter_launcher_icons>
- <https://developers.facebook.com/docs/sharing/webmasters/images/>
- <https://help.x.com/en/managing-your-account/common-issues-when-uploading-profile-photo>
- <https://www.linkedin.com/help/linkedin/answer/a566232>
