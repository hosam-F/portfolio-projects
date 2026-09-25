# One Piece Library Website

## Overview

A small Arabic RTL static website for presenting the services and products of One Piece Library. The current interface is implemented with HTML and CSS and uses local image assets.

## Current Scope

The page presents the library, product categories, printing and finishing services, event themes, mobile accessories, and contact information already present in the original content.

## Technologies

- HTML5
- CSS3
- Local image assets

## Database Status

A set of SQL files exists under `binyan.sql/`, including schema/data scripts for users, tasks, skills, and task applications. The current `nootbook.html` contains no PHP, JavaScript fetch/AJAX call, form submission handler, or database connection code. Therefore, the website is currently **static and not connected to the SQL database**.

The SQL files are preserved as a separate database artifact. Connecting them would require a backend implementation and a deliberate change of project scope; no connection or fabricated backend was added in this cleanup.

## Running Locally

Open `nootbook.html` in a browser, or serve the folder with any static web server. No PHP or database server is required for the current page.

## Portfolio Status

Suitable as a small front-end/static-web project after reviewing the contact information and image redistribution rights. It should not be described as a full-stack or database-connected application in its current state.
