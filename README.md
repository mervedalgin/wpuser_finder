
# WordPress Admin Username Finder

A tool that can find the admin username of WordPress




## INSTALL THIS PACKAGE

```bash
  pip install requests
```
## Start Command

```bash
  python3 wpuser_finder.py
```

## New Feature Added: Multiple User ID Scanner

The script now includes a new option "Scan Multiple User IDs" that:

1. **Scans multiple user IDs**: Instead of just checking the first user, it now scans user IDs from 1 to a specified maximum (default: 10)
2. **Individual API calls**: Makes separate API calls to `/wp-json/wp/v2/users/{id}` for each user ID
3. **Real-time feedback**: Shows live progress with ✓ for found users and ✗ for not found users
4. **Detailed information**: Displays both username (slug) and display name for each found user
5. **Summary report**: Provides a comprehensive summary at the end showing all found users

## Updated Menu Options:

- **Option 1**: Find Username (First User) - Original functionality
- **Option 2**: Scan Multiple User IDs - New feature
- **Option 3**: Exit

## Key Features of the New Scanner:

- **Customizable range**: Users can specify how many IDs to scan (e.g., 1-5, 1-10, 1-50)
- **Error handling**: Properly handles timeouts, connection errors, and HTTP errors
- **Progress indication**: Shows real-time scanning progress
- **Detailed output**: For each found user shows: ID, username, and display name
- **Summary section**: Clean summary showing all discovered users

