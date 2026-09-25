# Oiyaji Sermons Flutter

## Overview

Oiyaji is a Flutter application project for presenting sermons, lessons, books, and related educational content associated with Sheikh Mohammed Al-Jarafi. The repository contains Flutter/Dart source, local data models, screens, assets, and Android/iOS project folders.

## Technologies Found in the Project

- Flutter and Dart
- Provider for state management
- SQLite through `sqflite` and `path`
- PDF viewing through `advance_pdf_viewer`
- `path_provider`
- Localization through Flutter localization, `intl`, and `easy_localization`
- `shared_preferences`
- `url_launcher`, `share_plus`, and `cached_network_image`
- Tajawal font assets

## Structure

- `lib/main.dart`: application entry point.
- `lib/models/`: content models such as books, chapters, lessons, sermons, and videos.
- `lib/data/`: local data and database-related code.
- `lib/presentation/`: providers and presentation screens.
- `lib/widgets/`: reusable interface components.
- `screens/`: additional screen implementations that require consolidation review.
- `assets/`: books, images, translations, database assets, and fonts.
- `android/` and `ios/`: platform projects.

## Running

From the project root, use a compatible Flutter SDK and run:

```text
flutter pub get
flutter analyze
flutter test
flutter run
```

A reproducible build has not been claimed in the current audit because Flutter is not available in the present sandbox. The local `android/local.properties` file contains machine-specific SDK paths and must remain ignored and must not be published.

## Current Status

Real Flutter project requiring cleanup and completion review. The repository appears to contain more than one generation of screen structure (`lib/presentation` and `screens`), so the active navigation path and duplicate implementations should be confirmed before portfolio publication.

## Portfolio Notes

Do not present unverified features as completed. First confirm the active screens, database flow, localization flow, and a successful clean build on a configured Flutter/Android environment.
