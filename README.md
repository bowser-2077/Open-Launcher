# Open Launcher

<p align="center">
  <img width="220" height="220" alt="logo" src="https://github.com/user-attachments/assets/675064f3-7dba-4079-a417-878e4a974f3f" />
</p>

### Open launcher
is a free steam alternative for open source games

## Features 

  - Simple login and register system, no email, no phone number, just an username and a password
  - Intergrated store, download, donations and report button
  - Easy to use library
  - In app account management

> [!WARNING]
> Game upload is fully supported but  
> upload system may change in the near future.  
> You can upload games by following the rules on the last section.

## Installation

Open Launcher provide an easy and fast install system  
Please follow the steps bellow to install Open Launcher on your system  

  - Step 1 : Download Open Launcher from [here](https://bowser-2077.github.io/openlauncher)
  - Step 2 : Launch the install system and follow the installer instructions.
  - Step 3 : You will have to launch Open Launcher with the desktop shortcut or the start menu.

> [!NOTE]
> To uninstall Open Launcher,
> Please locate the app in the control panel
> and press uninstall, thats it.


## Use from source

To use Open Launcher with the sourcecode, please follow these steps

  - Step 1 : Download the sourcecode (Open-Launcher-Main.zip)
  - Step 2 : Extract it to the location that you want to use
  - Step 3 : Double click on **main.py**

If the app dont launch, please paste this command into a cmd.

  ```bash
pip install Pyside6 requests supabase
  ```

> [!CAUTION]
> The official supabase ANON key is present on the sourcecode  
> This is normal. In order to make Open Launcher free and  
> Easy to use for everyone, you can connect your own version
> of Open Launcher with the rest  
> Of the community!

You can use your own supabase postgress SQL. This is how to setup the DB.  

You will need to execute these 2 commands to create the required DBs  

Games table creation :

```sql
create table games (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  author text not null,
  description text,
  image_url text,
  download_url text,
  donation_enabled boolean default false,
  donation_link text
);
```

Users table creation :

```sql
create table users (
    pseudo text primary key,
    password_hash text not null
);
```

And now, you will have to replace the default ANON key by yours on **api.py**


## Game Uploading Rules

1. **Original Content Only**  
   - You may only upload games that you own the rights to or have explicit permission to share.  
   - Do not upload pirated, stolen, or cracked content.  

2. **File Requirements**  
   - All game files must be virus-free and safe to run.  
   - Compressed archives (.zip, .rar, .7z) must include all required assets and executables.  
   - File names should be clear and avoid special characters.  

3. **Game Description**  
   - Provide an accurate title, version, and description of the game.  
   - Include installation instructions if necessary.  
   - Screenshots or a cover image are highly recommended.  

4. **Prohibited Content**  
   - Adult content is authorised BUT you will have to precise that this is a +18 game on the title.  
   - No hidden malware, miners, or backdoors.  
   - No copyrighted assets without permission (music, images, code, etc.).  

5. **Metadata and Tags**  
   - Use relevant name so players can easily find your game.  
   - Misleading titles, tags, or descriptions are not allowed.  

6. **Updates and Maintenance**  
   - Keep your game up to date (Old versions will be removed : contact me on discord for game removal : bowser_2077).  
   - Old versions should be marked clearly to avoid confusion.  

7. **Community Respect**  
   - Treat feedback and reviews respectfully.  
   - Do not spam or re-upload the same game multiple times.  

⚠️ **Violation of these rules may result in removal of your game and potential account suspension.**


## DRM/DMCA Infos

This is for games publishers only :  
If you need to contact me about a pirated game/software that you  
needo remove, please contact me via gmail : hostinfire@gmail.com or with discord bowser_2077

### Open Launcher is protected with MIT license



