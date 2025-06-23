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
) ON CONFLICT ("id") DO NOTHING;