
# ALLWEONE® AI Presentation Generator (Gamma Alternative)
⭐ Help us grow the ALLWEONE community by giving this repository a Star!

https://github.com/user-attachments/assets/a21dbd49-75b8-4822-bcec-a75b581d9c60

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Next.js](https://img.shields.io/badge/Next.js-000000?logo=next.js&logoColor=white)](https://nextjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

An open-source AI presentation generator inspired by gamma.app. Quickly create beautiful slides with AI and customize them. Part of the ALLWEONE AI platform.

[Online Demo](https://allweone.com/presentations) | [Video Tutorial](https://www.youtube.com/watch?v=UUePLJeFqVQ)

## 🌟 Key Features

- **AI Content Generation**: Generate complete presentations on any topic with a single click.
- **Customizable Slides**: Choose the number of slides, language, and page style.
- **Editable Outline**: Review and edit the outline after generation.
- **Multi-Theme Support**: Includes 9 built-in themes, with more coming soon.
- **Custom Themes**: Create and save your own themes from scratch.
- **Image Generation**: Select from different AI models to generate slide images.
- **Audience Style Selection**: Supports professional and casual presentation styles.
- **Real-Time Generation**: See the presentation content generated in real-time.
- **Fully Editable**: Modify text, fonts, and design elements.
- **Presentation Mode**: Present directly within the app.
- **Auto-Save**: Automatically saves your edited content.

## 🚀 Quick Start

### Prerequisites

- Node.js 18.x or later
- npm or yarn
- OpenAI API Key (for AI generation)
- Together AI API Key (for image generation)
- Google Client ID and Secret (for authentication)

### Installation Steps
0: Install Docker PostgreSQL
```
docker run --name postgresdb -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=welcome -d postgres
```

1. Install dependencies (from the current frontend directory):

   ```bash
   cp env_template .env
   npm install -g pnpm
   pnpm install
   ```

2. Set up the database:

   ```bash
   pnpm db:push
   ```

3. Insert a default user into the database (previous user authentication removed for testing):
```
INSERT INTO public."User" (
    "id",
    "name",
    "email",
    "password",
    "emailVerified",
    "image",
    "headline",
    "bio",
    "interests",
    "location",
    "website",
    "role",
    "hasAccess"
) VALUES (
    '01',
    'Admin User',
    'admin@example.com',
    'hashed_password_here',
    NOW(),
    NULL,
    'Administrator',
    'Default admin account',
    ARRAY['admin', 'manager'],
    'Global',
    'https://example.com',
    'ADMIN',
    true
);
```

4. Check the `.env` file:
```
DATABASE_URL="postgresql://postgres:welcome@localhost:5432/presentation_ai"
A2A_AGENT_OUTLINE_URL="http://localhost:10001"
A2A_AGENT_SLIDES_URL="http://localhost:10011"
# Backend for downloading slides as PPT
DOWNLOAD_SLIDES_URL="http://localhost:10021"  
```

5. Start the development server:

   ```bash
   pnpm dev
   ```

6. Open [http://localhost:3000](http://localhost:3000) in your browser to view the application.

## 💻 User Guide

### Creating a Presentation

1. Go to the dashboard.
2. Enter the presentation topic.
3. Choose the number of slides (recommended: 5-10).
4. Select your preferred language.
5. Choose a page style.
6. Click "Generate Outline."
7. Review and edit the AI-generated outline.
8. Select a theme for the presentation.
9. Choose an image generation model.
10. Select your presentation style (professional/casual).
11. Click "Generate Presentation."
12. Wait for the AI to create the slides in real-time.
13. Preview, edit, and refine the presentation as needed.
14. Present directly from the app or export the presentation.

### Customizing Themes

1. Click "Create New Theme."
2. Start from scratch or derive from an existing theme.
3. Customize colors, fonts, and layouts.
4. Save your theme for future use.

## 🧰 Tech Stack

This project is built using the following technologies:

- **Next.js**: React framework for server-rendered applications.
- **React**: UI library for building user interfaces.
- **Prisma**: Database ORM with PostgreSQL.
- **Tailwind CSS**: Utility-first CSS framework.
- **TypeScript**: Typed JavaScript.
- **OpenAI API**: For AI content generation.
- **Radix UI**: Headless UI components.
- **Plate Editor**: Rich text editor system for handling text, images, and slide components.
- **Authentication**: NextAuth.js for user authentication.
- **UploadThing**: File uploading.
- **DND Kit**: Drag-and-drop functionality.

## 🛠️ Project Structure

```
presentation/
├── .next/               # Next.js build output
├── node_modules/        # Dependencies
├── prisma/              # Database schemas
│   └── schema.prisma    # Prisma database model
├── src/                 # Source code
│   ├── app/             # Next.js application routes
│   ├── components/      # Reusable UI components
│   │   ├── auth/        # Authentication components
│   │   ├── presentation/  # Presentation-related components
│   │   │   ├── dashboard/   # Dashboard UI
│   │   │   ├── editor/      # Presentation editor
│   │   │   │   ├── custom-elements/  # Custom editor elements
│   │   │   │   ├── dnd/              # Drag-and-drop features
│   │   │   │   └── native-elements/  # Native editor elements
│   │   │   ├── outline/     # Presentation outline components
│   │   │   ├── theme/       # Theme-related components
│   │   │   └── utils/       # Presentation tools
│   │   ├── prose-mirror/  # ProseMirror editor components for outline
│   │   ├── text-editor/   # Text editor components
│   │   │   ├── hooks/       # Editor hooks
│   │   │   ├── lib/         # Editor library
│   │   │   ├── plate-ui/    # Plate editor UI components
│   │   │   └── plugins/     # Editor plugins
│   │   └── ui/           # Shared UI components
│   ├── hooks/           # Custom React hooks
│   ├── lib/             # Utility functions and shared code
│   ├── provider/        # Context providers
│   ├── server/          # Server-side code
│   ├── states/          # State management
│   ├── middleware.ts    # Next.js middleware
│   └── env.js           # Environment configuration
├── .env                 # Environment variables
├── .env.example         # Example environment variables
├── next.config.js       # Next.js configuration
├── package.json         # Project dependencies and scripts
├── tailwind.config.ts   # Tailwind CSS configuration
└── tsconfig.json        # TypeScript configuration
```

## 🤝 Contributing

We welcome contributions to the ALLWEONE Presentation Generator! Here’s how you can help:

1. Fork this repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

Built with ❤️ by the ALLWEONE™ Team 🇺🇸🇧🇷🇳🇵🇮🇳🇨🇳🇯🇵🇸🇬🇩🇪🏴🇺🇦🇰🇿🇷🇺🇦🇪🇸🇦🇰🇷🇹🇭🇮🇩🇲🇽🇬🇹🇫🇷🇮🇱🇻🇳🇵🇹🇮🇹🇨🇱🇨🇦🇵🇰🇸🇪🇱🇧

For any questions or support, please submit an issue on GitHub or contact us via Discord: https://discord.gg/wSVNudUBdY
