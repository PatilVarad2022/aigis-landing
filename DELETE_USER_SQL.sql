-- ============================================
-- SQL Script to Delete User by Email
-- Use in Neon SQL Editor
-- ============================================

-- Step 1: Verify the user exists
SELECT id, username, email, is_superuser 
FROM auth_user 
WHERE email = 'lagadnilesh5@gmail.com';

-- Step 2: Find the profile (if exists)
SELECT up.id, up.user_id, up.full_name, up.phone, up.shield_limit_percent
FROM landing_userprofile up
INNER JOIN auth_user u ON up.user_id = u.id
WHERE u.email = 'lagadnilesh5@gmail.com';

-- Step 3: Delete UserProfile FIRST (if exists)
DELETE FROM landing_userprofile 
WHERE user_id IN (
    SELECT id FROM auth_user WHERE email = 'lagadnilesh5@gmail.com'
);

-- Step 4: Delete user sessions (if any)
DELETE FROM django_session 
WHERE expire_date >= (
    SELECT date_joined FROM auth_user WHERE email = 'lagadnilesh5@gmail.com'
);

-- Step 5: Clear user permissions
DELETE FROM auth_user_user_permissions 
WHERE user_id IN (
    SELECT id FROM auth_user WHERE email = 'lagadnilesh5@gmail.com'
);

-- Step 6: Clear user groups
DELETE FROM auth_user_groups 
WHERE user_id IN (
    SELECT id FROM auth_user WHERE email = 'lagadnilesh5@gmail.com'
);

-- Step 7: Now delete the User (safe after all relations cleared)
DELETE FROM auth_user 
WHERE email = 'lagadnilesh5@gmail.com';

-- Step 8: Verify deletion (should return 0 rows)
SELECT COUNT(*) as remaining_users 
FROM auth_user 
WHERE email = 'lagadnilesh5@gmail.com';

SELECT COUNT(*) as remaining_profiles
FROM landing_userprofile up
INNER JOIN auth_user u ON up.user_id = u.id
WHERE u.email = 'lagadnilesh5@gmail.com';

